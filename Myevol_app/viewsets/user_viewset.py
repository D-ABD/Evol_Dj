from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..models.user_model import User
from ..serializers.user_serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserStatsSerializer,
    UserXpSerializer,
    UserPreferencesSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les utilisateurs, leur profil, préférences et statistiques.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Pour les endpoints "me", on veut l'utilisateur connecté
        if self.action in ['me', 'update_me', 'change_password', 'stats', 'add_xp', 'get_preferences', 'update_preferences']:
            return self.request.user
        return super().get_object()

    @extend_schema(
        summary="Récupérer mon profil",
        responses={200: UserProfileSerializer},
        tags=['Users']
    )
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        user = self.get_object()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="Mettre à jour mon profil",
        request=UserUpdateSerializer,
        responses={200: UserProfileSerializer},
        tags=['Users']
    )
    @me.mapping.patch
    def update_me(self, request):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_serializer = UserProfileSerializer(user)
        return Response(updated_serializer.data)

    @extend_schema(
        summary="Modifier mon mot de passe",
        request=UserUpdateSerializer,
        responses={200: None},
        tags=['Users']
    )
    @action(detail=False, methods=['post'], url_path='me/change-password')
    def change_password(self, request):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Mot de passe modifié avec succès."
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Voir mes statistiques",
        responses={200: UserStatsSerializer},
        tags=['Users']
    )
    @action(detail=False, methods=['get'], url_path='me/stats')
    def stats(self, request):
        user = self.get_object()
        serializer = UserStatsSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="Ajouter des XP",
        request=UserXpSerializer,
        responses={200: UserXpSerializer},
        tags=['Users']
    )
    @action(detail=False, methods=['post'], url_path='me/add-xp')
    def add_xp(self, request):
        user = self.get_object()
        serializer = UserXpSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result)

    @extend_schema(
        summary="Récupérer mes préférences",
        responses={200: UserPreferencesSerializer},
        tags=['Users']
    )
    @action(detail=False, methods=['get'], url_path='me/preferences')
    def get_preferences(self, request):
        user = self.get_object()
        serializer = UserPreferencesSerializer(instance=user)
        return Response(serializer.data)

    @extend_schema(
        summary="Modifier mes préférences",
        request=UserPreferencesSerializer,
        responses={200: UserPreferencesSerializer},
        tags=['Users']
    )
    @get_preferences.mapping.patch
    def update_preferences(self, request):
        user = self.get_object()
        serializer = UserPreferencesSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
