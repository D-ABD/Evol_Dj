from ..utils.levels import get_user_level, LEVEL_THRESHOLDS, get_user_progress

from datetime import timedelta
from collections import defaultdict

from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.db.models import Avg, Count

from django.conf import settings
User = settings.AUTH_USER_MODEL



# 🏅 Badge obtenu
class Badge(models.Model):
    """
    Modèle représentant un badge obtenu par un utilisateur.
    Les badges sont des récompenses pour des accomplissements spécifiques.
    
    API Endpoints suggérés:
    - GET /api/badges/ - Liste des badges de l'utilisateur courant
    - GET /api/users/{id}/badges/ - Liste des badges d'un utilisateur spécifique
    - GET /api/badges/recent/ - Badges récemment obtenus
    
    Exemple de sérialisation JSON:
    {
        "id": 1,
        "name": "Niveau 3",
        "description": "Tu as atteint le niveau 3 💪",
        "icon": "🥈",
        "date_obtenue": "2025-04-20",
        "level": 3
    }
    """
    name = models.CharField(max_length=100)  # Nom du badge
    description = models.TextField()         # Description du badge
    icon = models.CharField(max_length=100)  # Icône (chemin ou identifiant)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    date_obtenue = models.DateField(auto_now_add=True)  # Date d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['-date_obtenue']
        unique_together = ('name', 'user')  # Un utilisateur ne peut avoir qu'un badge avec le même nom
        
        """
        Filtres API recommandés:
        - name (exact, contains)
        - date_obtenue (range, gte, lte)
        - level (exact, gte, lte)
        """

    def __str__(self):
        """Représentation en chaîne de caractères du badge"""
        return f"{self.name} ({self.user.username})"

    def was_earned_today(self, reference_date=None):
        """
        Vérifie si le badge a été obtenu aujourd'hui.

        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)

        Returns:
            bool: True si le badge a été obtenu aujourd'hui, False sinon
            
        Utilisation dans l'API:
            Ce champ peut être exposé comme booléen calculé 'is_new' dans la sérialisation
            pour permettre à l'interface d'afficher un indicateur visuel pour les nouveaux badges.
        """
        if reference_date is None:
            reference_date = now().date()
        return self.date_obtenue == reference_date

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour créer automatiquement 
        une notification lorsqu'un badge est attribué.
        
        Note pour l'API:
        Lors de la création d'un badge via l'API, une notification sera également générée.
        Il n'est pas nécessaire de créer explicitement une notification dans la vue API.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # ⏱ Import local pour éviter les imports circulaires
            from .notification_model import Notification
            from .event_log_model import EventLog

            # Crée une notification pour informer l'utilisateur
            Notification.objects.create(
                user=self.user,
                message=f"🏅 Nouveau badge débloqué : {self.name}",
                notif_type="badge"
            )

            # Enregistre l'événement dans les logs du système
            EventLog.objects.create(
                user=self.user,
                action="attribution_badge",
                description=f"Badge '{self.name}' attribué à {self.user.username}"
            )


# 🧩 BadgeTemplate : tous les badges définissables
class BadgeTemplate(models.Model):
    """
        Modèle définissant les différents badges disponibles dans l'application.
        Contient les critères d'attribution des badges aux utilisateurs.
        
        Chaque template définit un type de badge qui peut être débloqué selon des conditions
        spécifiques (nombre d'entrées, régularité, humeur, etc.). Le modèle inclut 
        également des éléments visuels pour enrichir l'expérience utilisateur.
        
        API Endpoints suggérés:
        - GET /api/badges/templates/ - Liste tous les templates de badges
        - GET /api/badges/templates/{id}/ - Détails d'un template spécifique
        - GET /api/badges/templates/categories/ - Templates groupés par catégorie
        - GET /api/badges/templates/{id}/progress/ - Progression de l'utilisateur vers ce badge
        
        Exemple de sérialisation JSON:
        {
            "id": 3,
            "name": "Régulier",
            "description": "Tu as écrit chaque jour pendant 5 jours ✍️",
            "icon": "📅",
            "condition": "5 jours consécutifs avec entrées",
            "level": 1,
            "color_theme": "#4CAF50",
            "animation_url": "https://cdn.myevol.app/animations/regular.json",
            "progress": {
                "percent": 80,
                "current": 4,
                "target": 5,
                "unlocked": false
            }
        }
    
    """

    name = models.CharField(max_length=100, unique=True)  # Nom unique du badge
    description = models.TextField()                      # Description du badge
    icon = models.CharField(max_length=100)               # Icône (chemin ou identifiant)
    condition = models.CharField(max_length=255)          # Description de la condition d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)


    animation_url = models.URLField(
        blank=True,
        null=True,
        help_text="Lien vers une animation Lottie ou GIF pour enrichir l'affichage du badge"
    )
    color_theme = models.CharField(default="#FFD700", max_length=20)  # couleur du badge
    class Meta:
        verbose_name = "Modèle de badge"
        verbose_name_plural = "Modèles de badges"
        
        """
        Filtres API recommandés:
        - name (exact, contains)
        - condition (contains)
        - level (exact, gte, lte)
        """

    def __str__(self):
        """Représentation en chaîne de caractères du template de badge"""
        return self.name

    def check_unlock(self, user):
        """
        Vérifie si un utilisateur remplit les conditions pour débloquer ce badge.

        Cette méthode contient la logique détaillée pour chaque type de badge.

        Args:
            user (User): L'utilisateur à vérifier

        Returns:
            bool: True si l'utilisateur remplit les conditions, False sinon
            
        Utilisation dans l'API:
            Cette méthode est idéale pour le calcul de la progression vers les badges:
            
            1. Pour les endpoints /api/badges/progress/ qui montrent tous les badges
               et la progression de l'utilisateur vers leur obtention
            
            2. Pour calculer le pourcentage de progression pour des badges complexes,
               comme les badges de séquence (jours consécutifs)
               
        Exemples d'utilisation:
            # Vérifier si l'utilisateur peut débloquer ce badge
            can_unlock = badge_template.check_unlock(request.user)
            
            # Dans un sérialiseur avec un champ calculé
            @property
            def is_unlocked(self):
                return self.instance.check_unlock(self.context['request'].user)
        """
        total = user.total_entries()
        mood_avg = user.mood_average(7)

        # Dictionnaire des conditions
        conditions = {
            "Première entrée": total >= 1,
            "Régulier": user.has_entries_every_day(5),
            "Discipline": user.has_entries_every_day(10),
            "Résilience": user.has_entries_every_day(15),
            "Légende du Journal": user.has_entries_every_day(30),
            "Ambassadeur d'humeur": mood_avg is not None and mood_avg >= 9,
            "Productivité": user.entries_today() >= 3,
            "Objectif rempli !": user.all_objectives_achieved(),
            "Persévérance": total >= 100,
        }

        # Condition personnalisée
        if self.name in conditions:
            return conditions[self.name]

        # Cas spécial pour les badges de niveau (ex: "Niveau 3")
        if self.name.startswith("Niveau"):
            try:
                level_number = int(self.name.split(" ")[1])
                return get_user_level(total) >= level_number
            except (ValueError, IndexError):
                return False

        return False  # Par défaut, on ne débloque pas
    
    def get_progress(self, user):
        """
        Calcule la progression d'un utilisateur vers l'obtention de ce badge.

        Args:
            user (User): L'utilisateur concerné

        Returns:
            dict: Contient les informations de progression vers le badge :
                {
                    'percent': Pourcentage de progression (int),
                    'current': Valeur actuelle (ex. nombre d'entrées),
                    'target': Seuil à atteindre pour débloquer le badge,
                    'unlocked': Booléen indiquant si le badge est déjà débloqué
                }

        Utilisé dans l'API pour visualiser les barres de progression.
        """
        total = user.total_entries()  # Entrées du journal

        # ✅ Cas 1 : Badge déjà débloqué → progression complète, mais on garde target cohérent
        if user.badges.filter(name=self.name).exists():
            try:
                if self.name.startswith("Niveau"):
                    level_number = int(self.name.split(" ")[1])
                    progress_data = get_user_progress(total)
                    return {
                        'percent': 100,
                        'unlocked': True,
                        'current': total,
                        'target': progress_data["next_threshold"]
                    }
            except Exception:
                pass  # Si problème dans la logique, on retombe sur le fallback plus bas

            return {
                'percent': 100,
                'unlocked': True,
                'current': total,
                'target': total
            }

        # ✅ Cas 2 : Badge "Première entrée"
        if self.name == "Première entrée":
            return {
                'percent': 100 if total >= 1 else 0,
                'current': min(total, 1),
                'target': 1,
                'unlocked': total >= 1
            }

        # ✅ Cas 3 : Badge de type "Niveau X"
        elif self.name.startswith("Niveau"):
            try:
                level_number = int(self.name.split(" ")[1])
                progress_data = get_user_progress(total)
                return {
                    'percent': 100 if progress_data["level"] >= level_number else progress_data["progress"],
                    'current': total,
                    'target': progress_data["next_threshold"],
                    'unlocked': progress_data["level"] >= level_number
                }
            except (ValueError, IndexError, KeyError):
                return {
                    'percent': 0,
                    'unlocked': False,
                    'current': total,
                    'target': 0
                }

        # ✅ Cas 4 : Tous les autres badges personnalisés
        return {
            'percent': 100 if self.check_unlock(user) else 0,
            'unlocked': self.check_unlock(user),
            'current': total,
            'target': 1
        }
