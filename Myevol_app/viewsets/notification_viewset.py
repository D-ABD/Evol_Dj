# Myevol_app/api_viewsets/notification_viewset.py

from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from Myevol_app.models.notification_model import Notification
from Myevol_app.paginations import MyEvolPagination
from Myevol_app.serializers.notification_serializers import (
    NotificationSerializer,
    NotificationListSerializer,
    NotificationCreateSerializer,
    NotificationUpdateSerializer,
    NotificationCountSerializer,
    NotificationBulkActionSerializer
)
from Myevol_app.permissions import IsOwnerOrAdmin


@extend_schema(
    summary="Gérer les notifications de l'utilisateur connecté",
    description="""
    Permet de :
    - lister les notifications (`GET`)
    - en créer (`POST`)
    - les mettre à jour (`PATCH`)
    - compter et filtrer (`/count/`, `/unread/`, `/bulk/`)
    """,
    tags=["Notifications"]
)
class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les notifications utilisateur.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = MyEvolPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-created_at']
    search_fields = ['message', 'notif_type']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, archived=False)

    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'create':
            return NotificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Compter les notifications par statut et type",
        description="Retourne un résumé rapide du nombre total, non lues, aujourd'hui, par type.",
        responses={200: NotificationCountSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='count')
    def count(self, request):
        serializer = NotificationCountSerializer(instance=request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Actions de masse sur les notifications",
        description="Permet d'archiver ou de marquer comme lues plusieurs notifications à la fois.",
        request=NotificationBulkActionSerializer,
        responses={200: OpenApiResponse(description="Résultat de l'action de masse")}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='bulk')
    def bulk_action(self, request):
        serializer = NotificationBulkActionSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Lister uniquement les notifications non lues",
        description="Retourne toutes les notifications non lues pour l'utilisateur connecté.",
        responses={200: NotificationListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='unread')
    def unread(self, request):
        unread_notifications = self.get_queryset().filter(is_read=False)
        serializer = NotificationListSerializer(unread_notifications, many=True)
        return Response(serializer.data)
