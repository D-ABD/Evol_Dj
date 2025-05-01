from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..models.userPreference_model import UserPreference
from ..serializers.userPreference_serializers import (
    UserPreferenceCreateSerializer,
    UserPreferenceUpdateSerializer,
    AppearancePreferenceSerializer,
    NotificationPreferenceSerializer,
    NotificationToggleSerializer,
    PreferenceResetSerializer
)

class UserPreferenceViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin):
    """
    API pour gérer les préférences utilisateur.

    Endpoints disponibles:
    - GET /api/preferences/ : Récupérer toutes les préférences
    - PATCH /api/preferences/ : Mettre à jour une ou plusieurs préférences
    - GET /api/preferences/appearance/ : Récupérer uniquement les préférences d'apparence
    - GET /api/preferences/notifications/ : Récupérer uniquement les préférences de notifications
    - POST /api/preferences/toggle-notification/ : Activer/désactiver un type de notification
    - POST /api/preferences/reset/ : Réinitialiser toutes les préférences aux valeurs par défaut
    """

    serializer_class = UserPreferenceUpdateSerializer

    def get_object(self):
        """Retourne les préférences de l'utilisateur connecté."""
        return UserPreference.get_or_create_for_user(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/preferences/
        Récupère toutes les préférences de l'utilisateur.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /api/preferences/
        Met à jour une ou plusieurs préférences utilisateur.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def appearance(self, request):
        """
        GET /api/preferences/appearance/
        Récupère uniquement les préférences d'apparence de l'utilisateur.
        """
        instance = self.get_object()
        serializer = AppearancePreferenceSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        """
        GET /api/preferences/notifications/
        Récupère uniquement les préférences de notification de l'utilisateur.
        """
        instance = self.get_object()
        serializer = NotificationPreferenceSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def toggle_notification(self, request):
        """
        POST /api/preferences/toggle-notification/
        Active ou désactive un type spécifique de notification.

        Payload attendu :
        {
            "notif_type": "badge",
            "enabled": true
        }
        """
        instance = self.get_object()
        serializer = NotificationToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response({"detail": "Notification mise à jour."})

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """
        POST /api/preferences/reset/
        Réinitialise toutes les préférences utilisateur aux valeurs par défaut.

        Payload attendu :
        {
            "confirm": true
        }
        """
        instance = self.get_object()
        serializer = PreferenceResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response({"detail": "Préférences réinitialisées."})

    @extend_schema(
        summary="Voir les préférences par défaut",
        description="Retourne les valeurs par défaut des préférences utilisateur sans modifier les préférences actuelles."
    )
    @action(detail=False, methods=['get'], url_path='defaults')
    def defaults(self, request):
        """
        GET /api/preferences/defaults/
        Affiche les préférences par défaut définies dans le modèle.
        """
        return Response({
            "dark_mode": False,
            "accent_color": "#6C63FF",
            "font_choice": "Roboto",
            "enable_animations": True,
            "notif_badge": True,
            "notif_objectif": True,
            "notif_info": True,
            "notif_statistique": True,
        })
