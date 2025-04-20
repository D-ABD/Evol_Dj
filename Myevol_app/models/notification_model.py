from django.db import models
from django.utils.timezone import now
from django.conf import settings

User = settings.AUTH_USER_MODEL

# 🔔 Notification utilisateur
class Notification(models.Model):
    """
    Modèle représentant une notification pour un utilisateur.
    Permet d'informer l'utilisateur d'événements importants dans l'application.
    
    API Endpoints suggérés:
    - GET /api/notifications/ - Liste des notifications de l'utilisateur connecté
    - GET /api/notifications/unread/ - Liste des notifications non lues
    - POST /api/notifications/{id}/read/ - Marquer une notification comme lue
    - POST /api/notifications/read-all/ - Marquer toutes les notifications comme lues
    - POST /api/notifications/{id}/archive/ - Archiver une notification
    - GET /api/notifications/archived/ - Liste des notifications archivées
    - DELETE /api/notifications/{id}/ - Supprimer une notification
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "message": "🏅 Nouveau badge débloqué : Niveau 3 !",
        "notif_type": "badge",
        "type_display": "Badge débloqué",
        "is_read": false,
        "created_at": "2025-04-19T16:42:22Z",
        "archived": false
    }
    """

    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif'),
        ('statistique', 'Statistique'),
        ('info', 'Information'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()  # Contenu de la notification
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info')
    is_read = models.BooleanField(default=False)  # État de lecture
    read_at = models.DateTimeField(null=True, blank=True)  # Date de lecture
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)  # Champ pour archiver la notification
    scheduled_at = models.DateTimeField(null=True, blank=True)  # Pour les notifications programmées

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'archived']),
        ]
        
        """
        Filtres API recommandés:
        - is_read (boolean)
        - archived (boolean)
        - notif_type (exact, in)
        - created_at (date, range)
        
        Pagination:
        - Utiliser la pagination par défaut (généralement 10-20 par page)
        - Considérer une pagination par curseur pour les grandes quantités
        """

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
        
    @property
    def type_display(self):
        """
        Retourne la version lisible du type de notification.
        
        Returns:
            str: Label du type de notification
            
        Utilisation dans l'API:
            À inclure comme champ dans la sérialisation pour l'affichage
            dans l'interface utilisateur.
        """
        return dict(self.NOTIF_TYPES).get(self.notif_type, "Information")

    def archive(self):
        """
        Archive la notification (sans suppression).
        
        Utilisation dans l'API:
            Parfait pour un endpoint dédié avec une action personnalisée.
            
        Exemple dans une vue:
            @action(detail=True, methods=['post'])
            def archive(self, request, pk=None):
                notification = self.get_object()
                notification.archive()
                return Response(status=status.HTTP_204_NO_CONTENT)
        """
        if not self.archived:
            self.archived = True
            self.save(update_fields=['archived'])

    def mark_as_read(self):
        """
        Marque une seule notification comme lue si ce n'est pas déjà fait.
        Enregistre également la date de lecture.
        
        Utilisation dans l'API:
            Idéal pour un endpoint dédié qui marque une notification spécifique comme lue.
            
        Exemple dans une vue:
            @action(detail=True, methods=['post'])
            def mark_read(self, request, pk=None):
                notification = self.get_object()
                notification.mark_as_read()
                return Response(self.get_serializer(notification).data)
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues **et non archivées** d'un utilisateur comme lues.

        Args:
            user (User): L'utilisateur concerné.

        Returns:
            int: Nombre de notifications marquées comme lues.

        Utilisation dans l'API:
            Parfait pour un endpoint qui permet de marquer toutes les notifications comme lues,
            à condition qu'elles ne soient pas archivées.

        Exemple dans une vue:
            @action(detail=False, methods=['post'])
            def mark_all_read(self, request):
                count = Notification.mark_all_as_read(request.user)
                return Response({'marked_read': count})
        """
        unread = cls.objects.filter(user=user, is_read=False, archived=False)
        return unread.update(is_read=True, read_at=now())


    @classmethod
    def get_unread(cls, user):
        """
        Récupère toutes les notifications non lues et non archivées d'un utilisateur.

        Args:
            user: L'utilisateur dont on veut récupérer les notifications

        Returns:
            QuerySet: Ensemble des notifications non lues et non archivées
            
        Utilisation dans l'API:
            Utile pour afficher un compteur de notifications ou une liste des
            notifications non lues.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def unread(self, request):
                notifications = Notification.get_unread(request.user)
                page = self.paginate_queryset(notifications)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = self.get_serializer(notifications, many=True)
                return Response(serializer.data)
        """
        return cls.objects.filter(user=user, is_read=False, archived=False)

    @classmethod
    def get_inbox(cls, user):
        """
        Récupère toutes les notifications non archivées d'un utilisateur.

        Args:
            user: L'utilisateur dont on veut récupérer les notifications

        Returns:
            QuerySet: Ensemble des notifications non archivées
            
        Utilisation dans l'API:
            Cette méthode est idéale pour l'endpoint principal des notifications
            qui affiche la "boîte de réception" de l'utilisateur.
        """
        return cls.objects.filter(user=user, is_read=False, archived=False)

    @classmethod
    def get_archived(cls, user):
        """
        Récupère toutes les notifications archivées d'un utilisateur.

        Args:
            user: L'utilisateur dont on veut récupérer les notifications archivées

        Returns:
            QuerySet: Ensemble des notifications archivées
            
        Utilisation dans l'API:
            Parfait pour un endpoint qui affiche les notifications archivées,
            généralement accessible via un onglet "Archivées" dans l'interface.
        """
        return cls.objects.filter(user=user, archived=True)
        
    @classmethod
    def create_notification(cls, user, message, notif_type='info', scheduled_at=None):
        """
        Crée une nouvelle notification pour un utilisateur.
        
        Args:
            user (User): Destinataire de la notification
            message (str): Contenu de la notification
            notif_type (str): Type de notification (badge, objectif, etc.)
            scheduled_at (datetime, optional): Date programmée pour afficher la notification
            
        Returns:
            Notification: L'objet notification créé
            
        Utilisation dans l'API:
            Cette méthode facilite la création de notifications depuis les vues API.
            
        Exemple dans une vue:
            @action(detail=True, methods=['post'])
            def complete(self, request, pk=None):
                objective = self.get_object()
                # Logique de complétion...
                Notification.create_notification(
                    request.user,
                    f"🎯 Objectif atteint : {objective.title}",
                    notif_type="objectif"
                )
                return Response(...)
        """
        return cls.objects.create(
            user=user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )
        
    @classmethod
    def get_notification_count(cls, user):
        """
        Retourne un dictionnaire avec le nombre de notifications par état.
        
        Args:
            user (User): L'utilisateur concerné
            
        Returns:
            dict: Statistiques des notifications
                {
                    'unread': 5,   # Nombre de notifications non lues
                    'total': 42,   # Nombre total de notifications (non archivées)
                    'archived': 10  # Nombre de notifications archivées
                }
                
        Utilisation dans l'API:
            Parfait pour afficher des badges de compteur dans l'interface.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def counts(self, request):
                return Response(Notification.get_notification_count(request.user))
        """
        return {
            'unread': cls.objects.filter(user=user, is_read=False, archived=False).count(),
            'total': cls.objects.filter(user=user, archived=False).count(),
            'archived': cls.objects.filter(user=user, archived=True).count()
        }