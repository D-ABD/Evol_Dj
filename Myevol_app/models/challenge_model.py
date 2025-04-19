from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from .notification_model import Notification

from django.conf import settings
User = settings.AUTH_USER_MODEL



# 🎯 Modèle principal de défi
class Challenge(models.Model):
    """
    Modèle représentant un défi temporaire proposé aux utilisateurs.
    Les défis encouragent l'engagement en fixant des objectifs à atteindre dans une période donnée.
    
    API Endpoints suggérés:
    - GET /api/challenges/ - Liste tous les défis (avec filtres actifs/inactifs)
    - GET /api/challenges/{id}/ - Détails d'un défi spécifique
    - GET /api/challenges/active/ - Liste uniquement les défis actuellement actifs
    - GET /api/challenges/{id}/participants/ - Liste les utilisateurs participant à un défi
    
    Exemple de sérialisation JSON:
    {
        "id": 1,
        "title": "Marathon d'entrées",
        "description": "Créez 15 entrées en 7 jours !",
        "start_date": "2025-04-15",
        "end_date": "2025-04-22",
        "target_entries": 15,
        "is_active": true,
        "days_remaining": 3,
        "participants_count": 24
    }
    """
    title = models.CharField(max_length=255)  # Titre du défi
    description = models.TextField()          # Description détaillée
    start_date = models.DateField()           # Date de début du défi
    end_date = models.DateField()             # Date de fin du défi
    target_entries = models.PositiveIntegerField(default=5)  # Objectif d'entrées à atteindre

    class Meta:
        """
        Filtres API recommandés:
        - title (exact, contains)
        - start_date, end_date (gte, lte, range)
        - is_active (boolean calculé)
        """
        ordering = ['-end_date']  # Tri par défaut: défis se terminant bientôt en premier
        verbose_name = "Défi"
        verbose_name_plural = "Défis"

    def __str__(self):
        return f"{self.title} ({self.start_date} → {self.end_date})"

    def is_active(self):
        """
        Vérifie si le défi est actuellement actif.

        Returns:
            bool: True si actif aujourd'hui, sinon False.
            
        Utilisation dans l'API:
            Ce champ devrait être inclus comme champ calculé (SerializerMethodField)
            dans la sérialisation pour permettre de filtrer facilement les défis actifs.
            
        Exemple d'implémentation dans un sérialiseur:
            @property
            def is_active(self):
                return self.instance.is_active()
        """
        today = now().date()
        return self.start_date <= today <= self.end_date
        
    def days_remaining(self):
        """
        Calcule le nombre de jours restants avant la fin du défi.
        
        Returns:
            int: Nombre de jours jusqu'à la fin, ou 0 si le défi est terminé
            
        Utilisation dans l'API:
            Utile comme champ calculé pour l'affichage dans l'interface utilisateur.
        """
        today = now().date()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days

    def is_completed(self, user):
        """
        Vérifie si l'utilisateur a atteint l'objectif d'entrées pendant la période du défi.

        Args:
            user (User): L'utilisateur à évaluer

        Returns:
            bool: True si l'objectif est atteint
            
        Utilisation dans l'API:
            Cette méthode peut être utilisée pour créer un champ calculé 'is_completed'
            dans la sérialisation des défis, personnalisée pour chaque utilisateur.
            
        Exemple d'implémentation dans un sérialiseur:
            def get_is_completed(self, obj):
                user = self.context['request'].user
                return obj.is_completed(user)
        """
        return user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count() >= self.target_entries
        
    def get_progress(self, user):
        """
        Calcule la progression de l'utilisateur vers l'accomplissement du défi.
        
        Args:
            user (User): L'utilisateur dont on calcule la progression
            
        Returns:
            dict: Dictionnaire contenant les informations de progression
                {
                    'percent': 60,  # Pourcentage de progression (0-100)
                    'current': 9,   # Nombre actuel d'entrées
                    'target': 15,   # Objectif à atteindre
                    'completed': False  # Si l'objectif est atteint
                }
                
        Utilisation dans l'API:
            Idéal pour un endpoint /api/challenges/{id}/progress/
            ou comme champ calculé dans la sérialisation des défis.
        """
        current = user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count()
        
        completed = current >= self.target_entries
        percent = min(100, int((current / self.target_entries) * 100))
        
        return {
            'percent': percent,
            'current': current,
            'target': self.target_entries,
            'completed': completed
        }


# 🔁 Modèle de progression utilisateur pour chaque défi
class ChallengeProgress(models.Model):
    """
    Suivi de la progression d'un utilisateur sur un défi.
    Évite les doublons et garde trace de la date de complétion.
    
    API Endpoints suggérés:
    - GET /api/users/me/challenges/ - Liste les défis de l'utilisateur courant avec progression
    - GET /api/challenges/{id}/progress/ - Progression de l'utilisateur sur un défi spécifique
    - PATCH /api/challenges/{id}/join/ - Rejoindre un défi (crée une entrée de progression)
    
    Exemple de sérialisation JSON:
    {
        "id": 5,
        "challenge": {
            "id": 1,
            "title": "Marathon d'entrées",
            "description": "Créez 15 entrées en 7 jours !"
        },
        "completed": true,
        "completed_at": "2025-04-18T14:32:51Z",
        "progress": {
            "percent": 100,
            "current": 15,
            "target": 15
        }
    }
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="challenges")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="progresses")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')  # Un seul lien par utilisateur/défi
        
        """
        Filtres API recommandés:
        - challenge (exact)
        - completed (boolean)
        - completed_at (date, gte, lte)
        """

    def __str__(self):
        return f"{self.user.username} → {self.challenge.title} ({'✅' if self.completed else '⏳'})"
        
    def get_progress(self):
        """
        Calcule la progression actuelle pour cet utilisateur sur ce défi.
        
        Returns:
            dict: Informations de progression (similaire à Challenge.get_progress)
            
        Utilisation dans l'API:
            Cette méthode peut servir à enrichir la sérialisation du modèle.
        """
        return self.challenge.get_progress(self.user)


# 🔎 Vérification globale de tous les défis actifs pour un utilisateur
def check_challenges(user):
    """
    Vérifie tous les défis actifs pour l'utilisateur.
    Si l'utilisateur a complété un défi, il est marqué comme tel,
    une notification est envoyée.

    Args:
        user (User): L'utilisateur à vérifier
        
    Utilisation dans l'API:
        Cette fonction devrait être appelée après toute création d'entrée de journal
        via un signal post_save ou directement dans la vue API qui gère la création d'entrées.
        
    Exemple d'utilisation dans une vue API:
        @action(detail=False, methods=['post'])
        def create_entry(self, request):
            # ... logique de création d'entrée ...
            check_challenges(request.user)
            return Response(...)
    """
    today = now().date()

    # Parcourt tous les défis actifs
    for challenge in Challenge.objects.filter(start_date__lte=today, end_date__gte=today):
        progress, _ = ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)

        if not progress.completed and challenge.is_completed(user):
            # Mise à jour de la progression
            progress.completed = True
            progress.completed_at = now()
            progress.save()

            # Notification à l'utilisateur
            Notification.objects.create(
                user=user,
                message=f"🎯 Tu as terminé le défi : {challenge.title} !",
                notif_type="objectif"
            )