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
    
    API Endpoints suggérés:
    - GET /api/badges/templates/ - Liste tous les templates de badges
    - GET /api/badges/templates/{id}/ - Détails d'un template spécifique
    - GET /api/badges/templates/categories/ - Templates groupés par catégorie
    - GET /api/badges/templates/{id}/progress/ - Progression de l'utilisateur vers ce badge
    """
    name = models.CharField(max_length=100, unique=True)  # Nom unique du badge
    description = models.TextField()                      # Description du badge
    icon = models.CharField(max_length=100)               # Icône (chemin ou identifiant)
    condition = models.CharField(max_length=255)          # Description de la condition d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)

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
                thresholds = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]
                return total >= thresholds[level_number - 1]
            except (ValueError, IndexError):
                return False

        return False  # Par défaut, on ne débloque pas
    
    def get_progress(self, user):
        """
        Calcule le pourcentage de progression d'un utilisateur vers l'obtention de ce badge.
        
        Args:
            user (User): L'utilisateur dont on veut calculer la progression
            
        Returns:
            dict: Dictionnaire contenant le pourcentage et des informations sur la progression
                {
                    'percent': 70,  # Pourcentage de progression (0-100)
                    'current': 7,   # Valeur actuelle (ex: nombre d'entrées)
                    'target': 10,   # Valeur cible
                    'unlocked': False  # Si le badge est déverrouillé
                }
        
        Utilisation dans l'API:
            Idéal pour un endpoint /api/badges/templates/{id}/progress/
            ou comme champ calculé dans la sérialisation des templates de badge.
        """
        # Si le badge est déjà débloqué, retourner 100%
        if user.badges.filter(name=self.name).exists():
            return {'percent': 100, 'unlocked': True}
            
        total = user.total_entries()
        
        # Logique spécifique par type de badge
        if self.name == "Première entrée":
            return {
                'percent': 100 if total >= 1 else 0,
                'current': min(total, 1),
                'target': 1,
                'unlocked': total >= 1
            }
            
        elif self.name.startswith("Niveau"):
            try:
                level_number = int(self.name.split(" ")[1])
                thresholds = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]
                target = thresholds[level_number - 1]
                previous = thresholds[level_number - 2] if level_number > 1 else 0
                
                # Calcul du pourcentage entre le seuil précédent et le seuil actuel
                if total >= target:
                    percent = 100
                else:
                    percent = ((total - previous) / (target - previous)) * 100
                    percent = max(0, min(99, percent))  # Limite entre 0 et 99%
                
                return {
                    'percent': int(percent),
                    'current': total,
                    'target': target,
                    'unlocked': total >= target
                }
            except (ValueError, IndexError):
                return {'percent': 0, 'unlocked': False}
                
        # Cas par défaut: soit 0% soit 100%
        return {
            'percent': 100 if self.check_unlock(user) else 0,
            'unlocked': self.check_unlock(user)
        }