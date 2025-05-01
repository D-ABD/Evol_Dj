# Myevol_app/api_viewsets/quote_viewset.py

from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from rest_framework.response import Response
from Myevol_app.models.quote_model import Quote
from Myevol_app.paginations import MyEvolPagination
from Myevol_app.serializers.quote_serializers import (
    QuoteSerializer,
    QuoteDetailSerializer,
    RandomQuoteSerializer,
    DailyQuoteSerializer,
    AuthorListSerializer,
    MoodTagSerializer,
    QuoteSearchSerializer
)

@extend_schema(
    summary="Accès public aux citations inspirantes.",
    description="Permet de consulter, chercher et récupérer des citations librement (sans authentification)."
)
class QuoteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet public pour accéder aux citations inspirantes.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [AllowAny]
    pagination_class = MyEvolPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['author']
    search_fields = ['text', 'author', 'mood_tag']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuoteDetailSerializer
        return QuoteSerializer

    @extend_schema(
        summary="Obtenir une citation aléatoire",
        description="Retourne une citation tirée au hasard, avec un filtre mood_tag optionnel.",
        responses={200: RandomQuoteSerializer}
    )
    @action(detail=False, methods=['get'], url_path='random')
    def random(self, request):
        mood_tag = request.query_params.get('mood_tag')
        serializer = RandomQuoteSerializer(instance={'mood_tag': mood_tag})
        return Response(serializer.data)

    @extend_schema(
        summary="Obtenir la citation du jour",
        description="Retourne la citation quotidienne, potentiellement adaptée à l'utilisateur.",
        responses={200: DailyQuoteSerializer}
    )
    @action(detail=False, methods=['get'], url_path='daily')
    def daily(self, request):
        serializer = DailyQuoteSerializer(instance={}, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Lister les auteurs de citations",
        description="Retourne la liste des auteurs disponibles avec le nombre de citations par auteur.",
        responses={200: AuthorListSerializer}
    )
    @action(detail=False, methods=['get'], url_path='authors')
    def authors(self, request):
        serializer = AuthorListSerializer(instance={})
        return Response(serializer.data)

    @extend_schema(
        summary="Lister les tags d'humeur disponibles",
        description="Retourne la liste des tags d'humeur associés aux citations.",
        responses={200: MoodTagSerializer}
    )
    @action(detail=False, methods=['get'], url_path='mood-tags')
    def mood_tags(self, request):
        serializer = MoodTagSerializer(instance={})
        return Response(serializer.data)

    @extend_schema(
        summary="Rechercher des citations",
        description="Recherche de citations selon texte, auteur, ou mood_tag.",
        responses={200: QuoteSearchSerializer}
    )
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        params = {
            'query': request.query_params.get('query', ''),
            'author': request.query_params.get('author', ''),
            'mood_tag': request.query_params.get('mood_tag', '')
        }
        serializer = QuoteSearchSerializer(instance=params)
        return Response(serializer.data)
