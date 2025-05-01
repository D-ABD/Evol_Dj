# Myevol_app/api_viewsets/stats_viewset.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from rest_framework.response import Response
from Myevol_app.models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat
from Myevol_app.serializers.stats_serializers import (
    DailyStatSerializer,
    WeeklyStatSerializer,
    MonthlyStatSerializer,
    AnnualStatSerializer,
    StatsOverviewSerializer,
    StatsCategoryAnalysisSerializer
)
from Myevol_app.paginations import MyEvolPagination

@extend_schema(
    summary="API d'accès aux statistiques d'utilisation.",
    description="Permet d'obtenir les statistiques journalières, hebdomadaires, mensuelles, annuelles, ainsi qu'un aperçu global."
)
class StatsViewSet(viewsets.ViewSet):
    """
    API centralisée pour accéder aux différentes statistiques d'un utilisateur.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Résumé global des statistiques",
        description="Récupère un aperçu rapide (jour, semaine, mois, année, tendances)."
    )
    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        serializer = StatsOverviewSerializer()
        return Response(serializer.to_representation(request.user))

    @extend_schema(
        summary="Analyse des catégories",
        description="Analyse de la répartition des entrées par catégorie pour une période choisie."
    )
    @action(detail=False, methods=['get'], url_path='categories')
    def categories(self, request):
        period = request.query_params.get('period', 'month')
        serializer = StatsCategoryAnalysisSerializer(instance={'user': request.user, 'period': period})
        return Response(serializer.to_representation({'user': request.user, 'period': period}))

    @extend_schema(
        summary="Liste des statistiques journalières",
        description="Statistiques détaillées par jour."
    )
    @action(detail=False, methods=['get'], url_path='daily')
    def daily(self, request):
        queryset = DailyStat.objects.filter(user=request.user).order_by('-date')
        paginator = MyEvolPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = DailyStatSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Liste des statistiques hebdomadaires",
        description="Statistiques détaillées par semaine."
    )
    @action(detail=False, methods=['get'], url_path='weekly')
    def weekly(self, request):
        queryset = WeeklyStat.objects.filter(user=request.user).order_by('-week_start')
        paginator = MyEvolPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = WeeklyStatSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Liste des statistiques mensuelles",
        description="Statistiques détaillées par mois."
    )
    @action(detail=False, methods=['get'], url_path='monthly')
    def monthly(self, request):
        queryset = MonthlyStat.objects.filter(user=request.user).order_by('-month_start')
        paginator = MyEvolPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = MonthlyStatSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Liste des statistiques annuelles",
        description="Statistiques détaillées par année."
    )
    @action(detail=False, methods=['get'], url_path='annual')
    def annual(self, request):
        queryset = AnnualStat.objects.filter(user=request.user).order_by('-year_start')
        paginator = MyEvolPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = AnnualStatSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
