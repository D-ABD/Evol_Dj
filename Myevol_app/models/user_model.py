# MyEvol_app/models/user_model.py

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

from ..services.badge_service import update_user_badges
from ..services.streak_service import update_user_streak

from ..services.userpreference_service import create_or_update_preferences
from ..services.user_stats_service import (
    compute_mood_average,
    compute_current_streak,
   
)

# Initialisation du logger
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


def cache_result(timeout=60):
    """
    Décorateur qui met en cache le résultat de la fonction pendant un délai donné.
    Cette méthode est utilisée pour les statistiques comme la répartition des entrées par catégorie.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{self.__class__.__name__}_entries_by_category_{args}_{kwargs}"
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
    Modèle d'utilisateur personnalisé.
    Étend le modèle utilisateur standard avec des fonctionnalités supplémentaires
    pour l'application de suivi personnel.
    """
    email = models.EmailField(
        unique=True,
        help_text="L'email de l'utilisateur, utilisé pour l'authentification."
    )
    longest_streak = models.PositiveIntegerField(
        default=0, editable=False, help_text="La plus longue série d'entrées consécutives."
    )
    avatar_url = models.URLField(
        blank=True, null=True, help_text="URL de l'image de l'avatar de l'utilisateur."
    )
    xp = models.PositiveIntegerField(
        default=0, help_text="Le nombre total de points d'expérience cumulés par l'utilisateur."
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Retourne le nom complet de l'utilisateur.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Retourne le prénom ou le username si le prénom est vide.
        """
        return self.first_name or self.username

    def to_dict(self):
        """
        Représentation de l'utilisateur sous forme de dictionnaire (utile pour les API).
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.get_full_name(),
            "entries": self.total_entries(),
            "current_streak": self.current_streak(),
            "mood_average": self.mood_average(),
            "level": self.level(),
            "level_progress": self.level_progress(),
        }

    @property
    def total_entries(self):
        """
        Retourne le nombre total d'entrées de journal de l'utilisateur.
        """
        return self.entries.count()

    @property
    def mood_average(self, days=7, reference_date=None):
        """
        Calcule la moyenne d'humeur sur les X derniers jours.
        Délégué à user_stats_service.
        """
        return compute_mood_average(self, days, reference_date)

    @property
    def current_streak(self, reference_date=None):
        """
        Calcule la série actuelle de jours consécutifs avec au moins une entrée.
        Utilise le service user_stats.
        """
        return compute_current_streak(self, reference_date)

    @cache_result(timeout=300)  # Cache pendant 5 minutes
    def entries_by_category(self, days=None):
        """
        Renvoie une répartition des entrées par catégorie.
        Délégué à user_stats_service.
        """
        entries = self.entries.all()
        if days:
            entries = entries.filter(created_at__gte=now() - timedelta(days=days))
        return dict(entries.select_related('category').values('category').annotate(count=Count('id')).values_list('category', 'count'))

    def level(self):
        """
        Calcule le niveau actuel de l'utilisateur basé sur le nombre d'entrées.
        Utilise le service `get_user_progress` pour récupérer les données du niveau.
        """
        from ..services.user_stats_service import get_user_progress
        progress = get_user_progress(self.total_entries)
        return progress['level']

    def level_progress(self):
        """
        Retourne la progression du niveau actuel en pourcentage.
        Utilise le service `get_user_progress` pour récupérer la progression.
        """
        from ..services.user_stats_service import get_user_progress
        progress = get_user_progress(self.total_entries)
        return progress['progress']

    def update_badges(self):
        """
        Met à jour les badges débloqués pour l'utilisateur.
        Géré par le service `badge_service`.
        """
        try:
            update_user_badges(self)
            logger.info(f"Badges mis à jour pour l'utilisateur {self.username} (ID: {self.id})")
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des badges pour {self.username} (ID: {self.id}): {e}")

    def update_streaks(self):
        """
        Met à jour la plus longue série d'entrées consécutives.
        Géré par le service `streak_service`.
        """
        update_user_streak(self)
        logger.info(f"Série d'entrées consécutives mise à jour pour l'utilisateur {self.username} (ID: {self.id})")

    def create_default_preferences(self):
        """
        Crée les préférences utilisateur par défaut si elles n'existent pas.
        Utilise le service 'create_or_update_preferences' pour gérer les préférences.
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
        logger.info(f"Préférences par défaut créées pour l'utilisateur {self.username} (ID: {self.id})")
        return preferences

    def add_xp(self, amount):
        """
        Ajoute des points d'expérience à l'utilisateur.
        """
        if amount < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")
        self.xp += amount
        self.save(update_fields=['xp'])
        logger.info(f"{amount} points d'expérience ajoutés à l'utilisateur {self.username} (ID: {self.id}). Total XP: {self.xp}")

    def clean(self):
        """
        Validation avant enregistrement de l'utilisateur.
        """
        if self.xp < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")
        logger.debug(f"Validation avant enregistrement de l'utilisateur {self.username} (ID: {self.id})")

    def save(self, *args, **kwargs):
        """
        Méthode de sauvegarde personnalisée pour mettre à jour les streaks et badges avant l'enregistrement.
        """
        if self.is_new:
            self.create_default_preferences()
            logger.info(f"Nouvel utilisateur {self.username} (ID: {self.id}) créé avec des préférences par défaut.")
        super(User, self).save(*args, **kwargs)

    @property
    def is_new(self):
        """
        Vérifie si l'utilisateur est nouveau (non encore sauvegardé).
        """
        return self.pk is None

    def get_absolute_url(self):
        """
        Retourne l'URL absolue de l'utilisateur.
        """
        return f"/users/{self.id}/"
        
    def __repr__(self):
        """
        Retourne une représentation de l'objet utilisateur sous forme de chaîne de caractères.
        """
        return f"<User username={self.username}>"

# Invalidation du cache lors de modifications d'entrée
@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def invalidate_cache(sender, instance, **kwargs):
    """
    Fonction pour invalider le cache des résultats liés aux entrées de l'utilisateur
    lorsque des entrées sont ajoutées ou supprimées.
    """
    cache_key = f"{sender.__name__}_entries_by_category_{instance.pk}"
    cache.delete(cache_key)
    logger.info(f"Cache invalidé pour l'utilisateur {instance.username} (ID: {instance.id})")


# ------------------------------------
# Signaux dans signals/user_signals.py
# ------------------------------------
"""""
    @receiver(post_save, sender=User)
    def handle_user_creation(sender, instance, created, **kwargs):
        Signal appelé après la création d'un utilisateur pour :
        - Créer ses préférences par défaut
        - Mettre à jour ses badges
        - Mettre à jour sa série d'entrées consécutives (streak)
        
        Ce signal est déclenché uniquement lors de la création d'un nouvel utilisateur.
    """