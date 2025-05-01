from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from Myevol_app.models.badge_model import Badge
from Myevol_app.serializers.badge_serializers import BadgeSerializer
from Myevol_app.permissions import IsOwnerOrAdmin

@extend_schema(
    summary="Lister, créer et consulter les badges obtenus par l'utilisateur connecté",
    description="""
    Cette route permet à l'utilisateur connecté de :
    - **Lister** ses badges débloqués (`GET /api/badges/`)
    - **Voir les détails** d'un badge spécifique (`GET /api/badges/{id}/`)
    - **Créer** un badge (normalement réservé aux processus internes) (`POST /api/badges/`)

    **⚙️ Filtres disponibles** :
    - Recherche par `name` : `?search=<mot-clé>`
    - Tri par `date_obtenue` (par défaut décroissant) : `?ordering=date_obtenue` ou `?ordering=-date_obtenue`

    **🔐 Permissions** :
    - Authentification requise (`Token`)
    - Seul l'utilisateur propriétaire ou un admin peut accéder aux données.

    **📋 Exemple de réponse (GET /api/badges/)** :
    ```json
    [
      {
        "id": 1,
        "name": "Premier pas",
        "description": "Félicitations pour votre première entrée !",
        "date_obtenue": "2025-04-28T14:00:00Z"
      }
    ]
    ```
    """,
    tags=["Badges"],
    parameters=[
        OpenApiParameter(name="search", description="Recherche par nom de badge", required=False, type=str),
        OpenApiParameter(name="ordering", description="Ordre de tri (ex: -date_obtenue)", required=False, type=str),
    ],
    responses={
        200: OpenApiResponse(description="Liste des badges obtenus"),
        403: OpenApiResponse(description="Non autorisé"),
        401: OpenApiResponse(description="Authentification requise"),
    }
)
class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-date_obtenue']
    search_fields = ['name']

    def get_queryset(self):
        return Badge.objects.filter(user=self.request.user)
  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from Myevol_app.models.badge_model import BadgeTemplate
from Myevol_app.serializers.badge_serializers import BadgeTemplateSerializer

@extend_schema(
    summary="Lister et consulter les modèles de badges disponibles",
    description="""
    Cette route permet de :
    - **Lister** tous les modèles de badges existants (`GET /api/badge-templates/`)
    - **Voir** un modèle de badge spécifique (`GET /api/badge-templates/{id}/`)

    **⚙️ Filtres disponibles** :
    - Recherche par `name` ou `description` : `?search=<mot-clé>`
    - Tri par `name` (ordre alphabétique par défaut)

    **🔐 Permissions** :
    - Accessible à tous, même sans être connecté (`AllowAny`).

    **📋 Exemple de réponse (GET /api/badge-templates/)** :
    ```json
    [
      {
        "id": 1,
        "name": "Explorateur",
        "description": "Débloqué après 10 entrées."
      }
    ]
    ```
    """,
    tags=["Modèles de Badges"],
    parameters=[
        OpenApiParameter(name="search", description="Recherche par nom ou description de badge", required=False, type=str),
        OpenApiParameter(name="ordering", description="Ordre de tri (ex: name)", required=False, type=str),
    ],
    responses={
        200: OpenApiResponse(description="Liste des modèles de badges"),
    }
)
class BadgeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BadgeTemplateSerializer
    queryset = BadgeTemplate.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['name']
    search_fields = ['name', 'description']
