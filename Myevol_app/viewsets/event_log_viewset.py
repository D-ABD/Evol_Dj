# Myevol_app/api_viewsets/event_log_viewset.py

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from Myevol_app.models.event_log_model import EventLog
from Myevol_app.paginations import MyEvolPagination
from Myevol_app.serializers.event_log_serializers import (
    EventLogSerializer,
    EventLogDetailSerializer,
    EventLogStatisticsSerializer
)
from Myevol_app.permissions import IsOwnerOrAdmin

@extend_schema(
    summary="Lister et consulter les événements du système",
    description="Permet de consulter les logs des utilisateurs et du système."
)
class EventLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les logs d'événements.
    - Admins : peuvent voir tous les logs
    - Utilisateurs : ne voient que leurs propres logs
    """
    serializer_class = EventLogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = MyEvolPagination 
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-created_at']
    search_fields = ['action', 'description', 'severity']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return EventLog.objects.all()
        return EventLog.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventLogDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Statistiques sur les événements",
        description="Statistiques globales ou utilisateur sur les événements (volumes, répartitions, etc.).",
        responses={200: EventLogStatisticsSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='statistics')
    def statistics(self, request):

        """
        Retourne des statistiques agrégées sur les événements.
        """
        period_days = int(request.query_params.get('days', 30))
        period_days = max(1, min(period_days, 365))  # entre 1 et 365 jours
        user = request.user if not request.user.is_staff else None
        stats_data = {
            'period_days': period_days,
            'user': user
        }
        serializer = EventLogStatisticsSerializer(stats_data)
        return Response(serializer.data)
