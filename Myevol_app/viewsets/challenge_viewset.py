# Myevol_app/api_viewsets/challenge_viewset.py

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from Myevol_app.models.challenge_model import Challenge, ChallengeProgress
from Myevol_app.serializers.challenge_serializers import (
    ChallengeSerializer,
    ChallengeDetailSerializer,
    ChallengeProgressSerializer,
    ParticipantSerializer
)
from django.utils.timezone import now

@extend_schema(
    summary="Lister, récupérer et gérer les défis proposés.",
    description="Permet de voir tous les défis disponibles."
)
class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour accéder aux défis.
    Accessible sans authentification pour voir les défis.
    """
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-end_date']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChallengeDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Lister les défis actifs",
        description="Retourne uniquement les défis en cours (start_date <= today <= end_date)."
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='active')
    def active_challenges(self, request):
        today = now().date()
        active_challenges = self.queryset.filter(start_date__lte=today, end_date__gte=today)
        serializer = self.get_serializer(active_challenges, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Lister les participants d'un défi",
        description="Retourne les utilisateurs inscrits à un défi donné."
    )
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='participants')
    def participants(self, request, pk=None):
        challenge = self.get_object()
        progresses = ChallengeProgress.objects.filter(challenge=challenge)
        serializer = ParticipantSerializer(progresses, many=True)
        return Response(serializer.data)

# Myevol_app/api_viewsets/challenge_progress_viewset.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from Myevol_app.models.challenge_model import ChallengeProgress
from Myevol_app.serializers.challenge_serializers import ChallengeProgressSerializer
from Myevol_app.permissions import IsOwnerOrAdmin

@extend_schema(
    summary="Suivre la progression sur les défis.",
    description="Permet de voir sa progression sur les défis auxquels on a participé."
)
class ChallengeProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChallengeProgressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return ChallengeProgress.objects.filter(user=self.request.user)
