from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from Myevol_app.models.objective_model import Objective
from Myevol_app.paginations import MyEvolPagination
from Myevol_app.serializers.objective_serializers import (
    ObjectiveSerializer,
    ObjectiveListSerializer,
    ObjectiveDetailSerializer,
    ObjectiveCompleteSerializer,
    ObjectiveStatsSerializer,
    ObjectiveUpcomingSerializer,
    ObjectiveCategorySerializer
)
from Myevol_app.permissions import IsOwnerOrAdmin


@extend_schema(
    summary="Gérer les objectifs de l'utilisateur connecté",
    description="Créer, lister, modifier, supprimer et analyser ses objectifs personnels.",
    tags=["Objectifs"]
)
class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal pour gérer les objectifs.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = MyEvolPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['target_date']
    search_fields = ['title', 'category']

    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ObjectiveListSerializer
        elif self.action == 'retrieve':
            return ObjectiveDetailSerializer
        elif self.action == 'complete':
            return ObjectiveCompleteSerializer
        return ObjectiveSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Statistiques globales sur les objectifs",
        description="Retourne un résumé statistique : complétés, taux de réussite, par catégorie, etc.",
        responses={200: ObjectiveStatsSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='stats')
    def stats(self, request):
        serializer = ObjectiveStatsSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Lister les objectifs dont l'échéance approche",
        description="Retourne les objectifs à terminer aujourd'hui, cette semaine, ce mois-ci.",
        responses={200: ObjectiveUpcomingSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='upcoming')
    def upcoming(self, request):
        serializer = ObjectiveUpcomingSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Suggérer les catégories d'objectifs les plus utilisées",
        description="Retourne les 10 catégories les plus fréquentes.",
        responses={200: ObjectiveCategorySerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='categories')
    def categories(self, request):
        serializer = ObjectiveCategorySerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Marquer un objectif comme complété",
        description="Permet de marquer explicitement un objectif comme accompli.",
        responses={200: OpenApiResponse(description="Objectif marqué comme accompli")}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='complete')
    def complete(self, request, pk=None):
        objective = self.get_object()
        objective.done = True
        objective.save()
        return Response({'success': True, 'message': 'Objectif marqué comme accompli.'}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
