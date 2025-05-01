#  models/userPreference_model.py
import logging
import re
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Initialisation du logger
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL

# Constants for notification types
NOTIFICATION_TYPES = ['badge', 'objectif', 'info', 'statistique']

class UserPreference(models.Model):
    """
    Modèle pour stocker les préférences personnalisées de chaque utilisateur.
    Permet de contrôler les notifications et l'apparence de l'application.
    Chaque utilisateur a exactement une instance de ce modèle (relation one-to-one).
    """
    
    # Relation one-to-one avec l'utilisateur
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="preferences", 
        help_text="Utilisateur auquel ces préférences appartiennent"
    )

    # Préférences de notifications par type
    notif_badge = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications pour les badges débloqués"
    )
    notif_objectif = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications liées aux objectifs"
    )
    notif_info = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications informatives générales"
    )
    notif_statistique = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications de statistiques"
    )

    # Préférences d'apparence
    dark_mode = models.BooleanField(
        default=False,
        help_text="Active ou désactive le mode sombre pour l'interface"
    )
    accent_color = models.CharField(
        max_length=20, 
        default="#6C63FF", 
        help_text="Couleur principale utilisée dans l'interface. Format hexadécimal (#RRGGBB)"
    )
    font_choice = models.CharField(
        max_length=50, 
        default="Roboto", 
        help_text="Police de caractères préférée pour l'interface"
    )
    enable_animations = models.BooleanField(
        default=True, 
        help_text="Active ou désactive les animations dans l'application"
    )

    class Meta:
        verbose_name = "Préférence utilisateur"
        verbose_name_plural = "Préférences utilisateur"
        ordering = ["user"]

    def __str__(self):
        """
        Représentation textuelle de l'objet de préférences.
        
        Returns:
            str: Chaîne indiquant à quel utilisateur appartiennent ces préférences
        """
        return f"Préférences de {self.user.username}"

    def __repr__(self):
        """
        Retourne une représentation de l'objet utilisateur sous forme de chaîne de caractères.
        
        Utilisé principalement dans les logs et les interfaces interactives.
        
        Returns:
            str: Représentation de l'objet UserPreference
        """
        return f"<UserPreference user={self.user.username}>"

    def get_absolute_url(self):
        """
        Retourne l'URL absolue des préférences de l'utilisateur.
        
        Utilisé pour accéder aux préférences de l'utilisateur via son URL dédiée.
        
        Returns:
            str: URL pour accéder aux préférences de l'utilisateur
        """
        return f"/users/{self.user.id}/preferences/"

    def to_dict(self):
        """
        Renvoie les préférences sous forme de dictionnaire.
        Pratique pour l'affichage ou l'utilisation dans une API.
        
        Returns:
            dict: Préférences utilisateur structurées
            
        Utilisation dans l'API:
            Cette méthode peut servir de base pour la sérialisation,
            mais privilégiez les sérialiseurs DRF pour plus de contrôle.
            
        Exemple dans un sérialiseur:
            class UserPreferenceSerializer(serializers.ModelSerializer):
                class Meta:
                    model = UserPreference
                    exclude = ['user']  # L'utilisateur est implicite
        """
        return {
            "dark_mode": self.dark_mode,
            "accent_color": self.accent_color,
            "font_choice": self.font_choice,
            "enable_animations": self.enable_animations,
            "notifications": {
                "badge": self.notif_badge,
                "objectif": self.notif_objectif,
                "info": self.notif_info,
                "statistique": self.notif_statistique,
            }
        }

    def get_appearance_settings(self):
        """
        Récupère uniquement les paramètres d'apparence.
        
        Returns:
            dict: Paramètres d'apparence de l'interface
            
        Utilisation dans l'API:
            Utile pour un endpoint dédié à l'apparence ou pour
            la récupération rapide des préférences visuelles au chargement.
        """
        logger.info(f"Récupération des paramètres d'apparence pour l'utilisateur {self.user.username}")
        return {
            "dark_mode": self.dark_mode,
            "accent_color": self.accent_color,
            "font_choice": self.font_choice,
            "enable_animations": self.enable_animations
        }

    def get_notification_settings(self):
        """
        Récupère uniquement les paramètres de notification.
        
        Returns:
            dict: Préférences de notifications par type
            
        Utilisation dans l'API:
            Idéal pour vérifier rapidement si un type de notification
            est activé avant d'en envoyer une.
        """
        logger.info(f"Récupération des paramètres de notification pour l'utilisateur {self.user.username}")
        return {
            "badge": self.notif_badge,
            "objectif": self.notif_objectif,
            "info": self.notif_info,
            "statistique": self.notif_statistique
        }

    def reset_to_defaults(self):
        """
        Réinitialise toutes les préférences aux valeurs par défaut.
        
        Utilisation dans l'API:
            Parfait pour un endpoint permettant à l'utilisateur de
            réinitialiser toutes ses préférences d'un coup.
        """
        logger.info(f"Réinitialisation des préférences aux valeurs par défaut pour l'utilisateur {self.user.username}")
        self.dark_mode = False
        self.accent_color = "#6C63FF"
        self.font_choice = "Roboto"
        self.enable_animations = True
        self.notif_badge = True
        self.notif_objectif = True
        self.notif_info = True
        self.notif_statistique = True
        self.save()

    @classmethod
    def get_or_create_for_user(cls, user):
        """
        Récupère les préférences d'un utilisateur ou les crée si elles n'existent pas.
        
        Args:
            user: L'utilisateur pour lequel récupérer/créer les préférences
            
        Returns:
            UserPreference: Instance de préférences
            
        Utilisation dans l'API:
            Très utile dans les vues pour s'assurer que l'utilisateur
            a toujours des préférences définies.
        """
        prefs, created = cls.objects.get_or_create(
            user=user,
            defaults={
                "dark_mode": False,
                "accent_color": "#6C63FF",
                "font_choice": "Roboto",
                "enable_animations": True,
                "notif_badge": True,
                "notif_objectif": True,
                "notif_info": True,
                "notif_statistique": True
            }
        )
        if created:
            logger.info(f"Préférences par défaut créées pour l'utilisateur {user.username}")
        else:
            logger.info(f"Préférences récupérées pour l'utilisateur {user.username}")
        return prefs

    def should_send_notification(self, notif_type):
        """
        Vérifie si un type spécifique de notification est activé.
        
        Args:
            notif_type (str): Type de notification ('badge', 'objectif', etc.)
            
        Returns:
            bool: True si ce type de notification est activé
            
        Utilisation dans l'API:
            Idéal pour les services de notification pour vérifier
            les préférences de l'utilisateur avant d'envoyer une notification.
            
        Exemple:
            if user.preferences.should_send_notification('badge'):
                send_badge_notification(user, badge)
        """
        mapping = {
            'badge': self.notif_badge,
            'objectif': self.notif_objectif,
            'info': self.notif_info,
            'statistique': self.notif_statistique
        }
        result = mapping.get(notif_type, False)
        logger.debug(f"Vérification de la notification '{notif_type}' pour l'utilisateur {self.user.username}: {result}")
        return result
    
    
# ------------------------------------
# Signaux dans signals/userPreference_signals.py
# ------------------------------------
"""
    - `handle_user_preferences`: Crée les préférences par défaut pour l'utilisateur si elles n'existent pas. 
      Ce service est appelé pour s'assurer que chaque utilisateur a bien des préférences créées à la première connexion. 
      Si les préférences existent déjà, elles sont mises à jour avec les nouvelles informations.

    - `get_or_create_for_user`: Récupère ou crée les préférences d'un utilisateur dans le service `userpreference_service`. 
      Ce service vérifie si l'utilisateur a déjà des préférences associées à son compte, sinon, il les crée avec des valeurs par défaut.

    Les signaux dans ce fichier gèrent les actions automatiques lors de la création ou mise à jour des préférences utilisateur, notamment :
    - La mise à jour des badges et des streaks de l'utilisateur chaque fois que ses préférences sont modifiées (`handle_user_preference_update`).
    - La création de préférences par défaut si elles n'existent pas lors de la création du modèle `UserPreference` (`create_default_preferences`).
    - L'envoi de notifications de mise à jour des préférences à l'utilisateur (`send_notification_on_preference_change`).
    - La validation des préférences avant leur enregistrement pour garantir la conformité des données (`validate_preferences`).

    Ces signaux permettent d'automatiser la gestion des préférences et d'intégrer facilement la logique de gestion des notifications et des actions utilisateur via des services.
"""
def clean(self):
    """Validation des préférences utilisateur avant sauvegarde."""
    super().clean()
    if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", self.accent_color):
        raise ValidationError({'accent_color': "La couleur doit être un code HEX valide (ex: #FFFFFF)."})
