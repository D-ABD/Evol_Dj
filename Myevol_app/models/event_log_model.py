from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError


class EventLog(models.Model):
    """
    Modèle pour enregistrer les événements et actions importantes dans l'application.
    Permet de tracer l'activité des utilisateurs et les événements système
    pour l'audit, le débogage ou l'analyse des comportements utilisateurs.
    
    API Endpoints suggérés:
    - GET /api/logs/ - Liste des événements (admin seulement)
    - GET /api/users/{id}/logs/ - Événements d'un utilisateur spécifique
    - GET /api/logs/actions/ - Liste des types d'actions disponibles
    - GET /api/logs/statistics/ - Statistiques agrégées des événements
    
    Exemple de sérialisation JSON:
    {
        "id": 421,
        "user": {
            "id": 8,
            "username": "john_doe"
        },
        "action": "attribution_badge",
        "description": "Badge 'Niveau 3' attribué à john_doe",
        "created_at": "2025-04-19T14:30:25Z"
    }
    """

    # Lien vers l'utilisateur concerné (optionnel pour les événements système)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # ou SET_NULL si on veut garder les logs après suppression
        related_name="event_logs",
        null=True,
        blank=True,  # Permet les logs système sans utilisateur associé
    )

    # Type d'action effectuée (ex: "connexion", "création_entrée", "attribution_badge", etc.)
    action = models.CharField(max_length=255)

    # Détails supplémentaires sur l'événement
    description = models.TextField(blank=True)

    # Horodatage automatique de l'événement
    created_at = models.DateTimeField(auto_now_add=True)

    # Données additionnelles au format JSON (optionnel pour stocker des métadonnées flexibles)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        
        """
        Filtres API recommandés:
        - user (exact)
        - action (exact, contains, in)
        - created_at (date, datetime, range, gte, lte)
        - description (contains)
        
        Sécurité API:
        - Limiter l'accès aux logs aux utilisateurs avec permissions admin
        - Pour les utilisateurs standards, ne montrer que leurs propres logs
        - Pagination obligatoire (max 50-100 items par page)
        """
        
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        """
        Représentation textuelle du log d'événement.
        Ex: "2025-04-19 14:30 - attribution_badge"
        """
        return f"{self.created_at:%Y-%m-%d %H:%M} - {self.action}"
    
    @classmethod
    def log_action(cls, action, description="", user=None, **metadata):
        """
        Méthode utilitaire pour créer facilement un log d'événement.
        
        Args:
            action (str): Type d'action (ex: "connexion", "création_entrée")
            description (str): Description détaillée de l'événement
            user (User, optional): Utilisateur concerné (None pour événement système)
            **metadata: Données supplémentaires à stocker au format JSON
        
        Returns:
            EventLog: L'objet EventLog créé
            
        Utilisation dans l'API:
            Cette méthode simplifie l'enregistrement d'événements dans les vues API.
            
        Exemple:
            @action(detail=True, methods=['post'])
            def complete_challenge(self, request, pk=None):
                challenge = self.get_object()
                # Logique de complétion...
                EventLog.log_action(
                    "challenge_completed",
                    f"Défi '{challenge.title}' complété",
                    user=request.user,
                    challenge_id=challenge.id,
                    time_spent_days=(now().date() - challenge.start_date).days
                )
                return Response(...)
        """
        return cls.objects.create(
            action=action,
            description=description,
            user=user,
            metadata=metadata or None
        )
    
    @classmethod
    def get_action_counts(cls, days=30, user=None):
        """
        Retourne des statistiques sur le nombre d'événements par type d'action.
        
        Args:
            days (int): Nombre de jours à considérer
            user (User, optional): Limiter aux événements d'un utilisateur spécifique
            
        Returns:
            dict: Dictionnaire {action: count} avec les totaux par action
            
        Utilisation dans l'API:
            Parfait pour un endpoint de statistiques ou de tableau de bord.
            
        Exemple API:
            @action(detail=False, methods=['get'])
            def statistics(self, request):
                stats = EventLog.get_action_counts(
                    days=int(request.query_params.get('days', 30)),
                    user=request.user if not request.user.is_staff else None
                )
                return Response(stats)
        """
        from django.db.models import Count
        
        # Filtre de base sur la période
        since = now() - timedelta(days=days)
        query = cls.objects.filter(created_at__gte=since)
        
        # Filtre optionnel par utilisateur
        if user:
            query = query.filter(user=user)
            
        # Agrégation par action
        return dict(
            query.values('action')
                .annotate(count=Count('id'))
                .values_list('action', 'count')
        )