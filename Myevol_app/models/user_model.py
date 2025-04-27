from datetime import timedelta
import logging
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils.timezone import now
from collections import defaultdict
from functools import wraps
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..services.levels_services import get_user_progress

from ..services.badge_service import update_user_badges
from ..services.streak_service import update_user_streak
from ..services.userpreference_service import create_or_update_preferences
from ..services.user_stats_service import compute_mood_average, compute_current_streak

logger = logging.getLogger(__name__)

def cache_result(timeout=60):
    """
    Décorateur pour mettre en cache le résultat d'une méthode d'instance 
    pendant une durée donnée (en secondes).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"user_{self.pk}_entries_by_category_{args}_{kwargs}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(self, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur.
    Étend AbstractUser avec des champs et méthodes spécifiques à l'app MyEvol.
    """

    email = models.EmailField(unique=True, help_text="Adresse e-mail de l'utilisateur.")
    longest_streak = models.PositiveIntegerField(default=0, editable=False, help_text="Plus longue série de jours consécutifs.")
    avatar_url = models.URLField(blank=True, null=True, help_text="URL de l'avatar de l'utilisateur.")
    xp = models.PositiveIntegerField(default=0, help_text="Points d'expérience accumulés.")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        """Retourne le nom d'utilisateur (username)."""
        return self.username

    def get_full_name(self):
        """Retourne le nom complet (prénom + nom)."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Retourne le prénom ou le username si le prénom est vide."""
        return self.first_name or self.username

    def to_dict(self):
        """
        Représentation de l'utilisateur sous forme de dictionnaire 
        (utile pour les API ou le frontend).
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.get_full_name(),
            "entries": self.total_entries,
            "current_streak": self.current_streak(),
            "mood_average": self.mood_average(),
            "level": self.level(),
            "level_progress": self.level_progress(),
        }

    @property
    def total_entries(self):
        """Retourne le nombre total d'entrées de journal de l'utilisateur."""
        return self.entries.count()

    def mood_average(self, days=7, category=None):
        from Myevol_app.models.user_model import compute_mood_average
        return compute_mood_average(self, days, category)


    def current_streak(self, reference_date=None):
        return compute_current_streak(self, reference_date)


    @cache_result(timeout=300)
    def entries_by_category(self, days=None):
        """
        Calcule la répartition des entrées de journal par catégorie 
        (sur les X derniers jours si précisé).
        """
        entries = self.entries.all()
        if days:
            entries = entries.filter(created_at__gte=now() - timedelta(days=days))
        return dict(
            entries.select_related('category')
            .values('category')
            .annotate(count=Count('id'))
            .values_list('category', 'count')
        )

    def level(self):
        """
        Retourne le niveau actuel de l'utilisateur basé sur le nombre d'entrées.
        """
        progress = get_user_progress(self.total_entries)
        return progress['level']

    def level_progress(self):
        """
        Retourne la progression du niveau actuel en pourcentage.
        """
        progress = get_user_progress(self.total_entries)
        return progress['progress']

    def update_badges(self):
        """
        Met à jour les badges de l'utilisateur via le badge_service.
        """
        try:
            update_user_badges(self)
            logger.info(f"Badges mis à jour pour {self.username} (ID: {self.id})")
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des badges pour {self.username} : {e}")

    def update_streaks(self):
        """
        Met à jour la plus longue série d'entrées consécutives.
        """
        update_user_streak(self)
        logger.info(f"Série d'entrées mise à jour pour {self.username} (ID: {self.id})")

    def create_default_preferences(self):
        """
        Crée des préférences par défaut pour l'utilisateur.
        """
        preferences_data = {
            "dark_mode": False,
            "accent_color": "#6C63FF",
            "font_choice": "Roboto",
            "enable_animations": True,
            "notif_badge": True,
            "notif_objectif": True,
            "notif_info": True,
            "notif_statistique": True
        }
        preferences = create_or_update_preferences(self, preferences_data)
        logger.info(f"Préférences par défaut créées pour {self.username}")
        return preferences

    def add_xp(self, amount):
        """
        Ajoute des points d'expérience à l'utilisateur.
        """
        if amount < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")
        self.xp += amount
        self.save(update_fields=['xp'])
        logger.info(f"{amount} XP ajoutés à {self.username} — Total XP : {self.xp}")

    def clean(self):
        """Validation du modèle : XP ne peut pas être négatif."""
        if self.xp < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")

    def save(self, *args, **kwargs):
        """
        Sauvegarde personnalisée : crée les préférences par défaut à la création.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.create_default_preferences()
            logger.info(f"Nouvel utilisateur {self.username} créé avec préférences.")

    @property
    def is_new(self):
        """Retourne True si l'utilisateur n'a pas encore été sauvegardé (nouveau)."""
        return self.pk is None

    def get_absolute_url(self):
        """Retourne l'URL publique de l'utilisateur."""
        return f"/users/{self.id}/"

    def __repr__(self):
        """Représentation lisible de l'utilisateur."""
        return f"<User username={self.username}>"

    def has_entries_every_day(self, days):
        """
        Vérifie si l'utilisateur a fait au moins une entrée par jour 
        durant les X derniers jours.
        """
        from ..models.journal_model import JournalEntry
        start_date = now().date() - timedelta(days=days - 1)
        entries = self.entries.filter(created_at__date__gte=start_date)
        active_days = entries.values_list("created_at__date", flat=True).distinct()
        return len(active_days) >= days

    def entries_today(self):
        """Retourne le nombre d'entrées créées aujourd'hui."""
        return self.entries.filter(created_at__date=now().date()).count()

    def all_objectives_achieved(self):
        """
        Vérifie si tous les objectifs de l'utilisateur sont complétés.
        """
        from ..models.objective_model import Objective
        return not Objective.objects.filter(user=self, done=False).exists()

    @receiver(post_save, sender='Myevol_app.User')
    @receiver(post_delete, sender='Myevol_app.User')
    def invalidate_cache(sender, instance, **kwargs):
        """
        Invalide le cache des statistiques par catégorie lors d'une sauvegarde
        ou suppression de l'utilisateur.
        """
        cache_key = f"user_{instance.pk}_entries_by_category_()_{{}}"
        cache.delete(cache_key)
        logger.info(f"Cache invalidé pour {instance.username} (ID: {instance.id})")
