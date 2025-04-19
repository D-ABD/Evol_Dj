from datetime import timedelta
from django.db import models
from django.utils.timezone import now

from django.conf import settings
User = settings.AUTH_USER_MODEL


class UserPreference(models.Model):
    """
    Modèle pour stocker les préférences personnalisées de chaque utilisateur.
    Permet de contrôler les notifications et l'apparence de l'application.
    Chaque utilisateur a exactement une instance de ce modèle (relation one-to-one).
    
    API Endpoints suggérés:
    - GET /api/preferences/ - Récupérer les préférences de l'utilisateur courant
    - PUT/PATCH /api/preferences/ - Mettre à jour les préférences
    - POST /api/preferences/reset/ - Réinitialiser les préférences aux valeurs par défaut
    - GET /api/preferences/appearance/ - Récupérer uniquement les paramètres d'apparence
    - GET /api/preferences/notifications/ - Récupérer uniquement les paramètres de notification
    
    Exemple de sérialisation JSON:
    {
        "appearance": {
            "dark_mode": false,
            "accent_color": "#6C63FF",
            "font_choice": "Roboto",
            "enable_animations": true
        },
        "notifications": {
            "badge": true,
            "objectif": true,
            "info": true,
            "statistique": true
        }
    }
    """

    # Relation one-to-one avec l'utilisateur (un utilisateur a exactement une préférence)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")

    # Préférences de notifications par type
    notif_badge = models.BooleanField(default=True)        # Notifications pour les badges débloqués
    notif_objectif = models.BooleanField(default=True)     # Notifications liées aux objectifs
    notif_info = models.BooleanField(default=True)         # Notifications informatives générales
    notif_statistique = models.BooleanField(default=True)  # Notifications de statistiques

    # Préférences d'apparence
    dark_mode = models.BooleanField(default=False)                    # Mode sombre activé ou désactivé
    accent_color = models.CharField(max_length=20, default="#6C63FF")  # Couleur principale pour personnaliser l'interface
    font_choice = models.CharField(max_length=50, default="Roboto")     # Police de caractères préférée
    enable_animations = models.BooleanField(default=True)              # Option pour activer/désactiver les animations

    class Meta:
        verbose_name = "Préférence utilisateur"
        verbose_name_plural = "Préférences utilisateur"
        ordering = ["user"]
        
        """
        Permissions API:
        - Un utilisateur ne peut accéder et modifier que ses propres préférences
        - Adapter les préférences lors des requêtes en fonction de l'utilisateur authentifié
        """

    def __str__(self):
        """
        Représentation textuelle de l'objet de préférences.
        
        Returns:
            str: Chaîne indiquant à quel utilisateur appartiennent ces préférences
        """
        return f"Préférences de {self.user.username}"

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
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def appearance(self, request):
                prefs = request.user.preferences
                return Response(prefs.get_appearance_settings())
        """
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
            
        Exemple d'utilisation dans une autre partie du code:
            if user.preferences.get_notification_settings()['badge']:
                # Envoyer une notification de badge
        """
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
            
        Exemple dans une vue:
            @action(detail=False, methods=['post'])
            def reset(self, request):
                prefs = request.user.preferences
                prefs.reset_to_defaults()
                return Response(self.get_serializer(prefs).data)
        """
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
            
        Exemple dans une vue:
            def get_object(self):
                return UserPreference.get_or_create_for_user(self.request.user)
        """
        prefs, created = cls.objects.get_or_create(
            user=user,
            defaults={
                # Valeurs par défaut définies ici pour être sûr
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
        return mapping.get(notif_type, False)
    