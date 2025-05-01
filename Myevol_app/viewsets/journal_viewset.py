# Myevol_app/api_viewsets/journal_entry_viewset.py

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from rest_framework.response import Response
from Myevol_app.models.journal_model import JournalEntry
from Myevol_app.paginations import MyEvolPagination
from Myevol_app.serializers.journal_serializers import (
    JournalEntrySerializer,
    JournalEntryDetailSerializer,
    JournalEntryCreateSerializer,
    JournalEntryCalendarSerializer,
    JournalStatsSerializer
)
from Myevol_app.permissions import IsOwnerOrAdmin


@extend_schema(
    summary="Gérer les entrées de journal de l'utilisateur connecté",
    description="""
    Ce ViewSet permet de :
    - Créer une nouvelle entrée (`POST`)
    - Voir ses entrées (`GET`)
    - Modifier ou supprimer ses propres entrées (`PUT`, `PATCH`, `DELETE`)
    
    Des actions personnalisées sont disponibles :
    - `/calendar/` : vue calendrier
    - `/stats/` : statistiques journalières
    """,
    tags=["Journal"],
)
class JournalEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les entrées de journal de l'utilisateur.
    """
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = MyEvolPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-created_at']
    search_fields = ['content', 'category']

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JournalEntryDetailSerializer
        elif self.action == 'create':
            return JournalEntryCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Récupérer des statistiques sur les entrées de journal",
        description="Renvoie diverses statistiques : humeur, catégories, série d'entrées, etc.",
        responses={200: JournalStatsSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='stats')
    def stats(self, request):
        user = request.user
        serializer = JournalStatsSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="Récupérer les entrées au format calendrier",
        description="Retourne les entrées groupées par jour avec humeur moyenne et catégories.",
        responses={200: JournalEntryCalendarSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='calendar')
    def calendar(self, request):
        user = request.user
        entries = JournalEntry.objects.filter(user=user).order_by('created_at')
        serializer = JournalEntryCalendarSerializer(entries, many=True)
        return Response(serializer.data)
