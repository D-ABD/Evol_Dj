from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
import re

from ..models.userPreference_model import UserPreference, NOTIFICATION_TYPES

User = get_user_model()


class UserPreferenceCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création des préférences utilisateur.
    Utilisé lors de la création initiale des préférences pour un nouvel utilisateur.
    """
    class Meta:
        model = UserPreference
        fields = [
            'user', 'dark_mode', 'accent_color', 'font_choice', 'enable_animations',
            'notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique'
        ]

    def validate_accent_color(self, value):
        """Valide que la couleur d'accentuation est un code hexadécimal valide."""
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise serializers.ValidationError(
                "La couleur doit être au format hexadécimal (#RRGGBB ou #RGB)."
            )
        return value

    def validate_user(self, user):
        """
        Permet de bypass la contrainte d'unicité pour pouvoir mettre à jour si ça existe déjà.
        """
        return user

    def create(self, validated_data):
        """Créer ou mettre à jour les préférences d'un utilisateur."""
        user = validated_data.pop('user')
        preferences = UserPreference.get_or_create_for_user(user)

        for attr, value in validated_data.items():
            setattr(preferences, attr, value)

        preferences.save()
        return preferences


class UserPreferenceUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour des préférences utilisateur.
    
    Permet de mettre à jour les préférences d'apparence et de notification.
    """
    class Meta:
        model = UserPreference
        fields = [
            'dark_mode', 'accent_color', 'font_choice', 'enable_animations',
            'notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique'
        ]
    
    def validate_accent_color(self, value):
        """Valide que la couleur d'accentuation est un code hexadécimal valide."""
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise serializers.ValidationError(
                "La couleur doit être au format hexadécimal (#RRGGBB ou #RGB)."
            )
        return value
    
    def update(self, instance, validated_data):
        """Mise à jour des préférences utilisateur."""
        # Mise à jour et journalisation
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class AppearancePreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer pour les préférences d'apparence.
    
    Version simplifiée qui ne contient que les préférences visuelles.
    """
    class Meta:
        model = UserPreference
        fields = ['dark_mode', 'accent_color', 'font_choice', 'enable_animations']
    
    def validate_accent_color(self, value):
        """Valide que la couleur d'accentuation est un code hexadécimal valide."""
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise serializers.ValidationError(
                "La couleur doit être au format hexadécimal (#RRGGBB ou #RGB)."
            )
        return value
    
    def to_representation(self, instance):
        """
        Utilise la méthode du modèle pour récupérer les paramètres d'apparence.
        """
        return instance.get_appearance_settings()


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer pour les préférences de notification.
    
    Version simplifiée qui ne contient que les préférences de notification.
    """
    class Meta:
        model = UserPreference
        fields = ['notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique']
    
    def to_representation(self, instance):
        """
        Utilise la méthode du modèle pour récupérer les paramètres de notification.
        """
        return instance.get_notification_settings()


class NotificationToggleSerializer(serializers.Serializer):
    """
    Serializer pour activer/désactiver un type de notification spécifique.
    
    Permet de basculer l'état d'un seul type de notification.
    """
    notif_type = serializers.ChoiceField(
        choices=[(t, t) for t in NOTIFICATION_TYPES],
        help_text="Type de notification à modifier"
    )
    enabled = serializers.BooleanField(
        help_text="True pour activer, False pour désactiver"
    )
    
    def validate_notif_type(self, value):
        """Valide que le type de notification est supporté."""
        if value not in NOTIFICATION_TYPES:
            raise serializers.ValidationError(
                f"Type de notification non reconnu. Valeurs possibles: {', '.join(NOTIFICATION_TYPES)}"
            )
        return value
    
    def update(self, instance, validated_data):
        """Met à jour le type de notification spécifié."""
        notif_type = validated_data['notif_type']
        enabled = validated_data['enabled']
        
        field_name = f"notif_{notif_type}"
        setattr(instance, field_name, enabled)
        instance.save(update_fields=[field_name])
        
        return instance


class PreferenceResetSerializer(serializers.Serializer):
    """
    Serializer pour réinitialiser les préférences aux valeurs par défaut.
    
    Ne contient aucun champ, juste une méthode pour réinitialiser les préférences.
    """
    confirm = serializers.BooleanField(
        write_only=True,
        help_text="Doit être True pour confirmer la réinitialisation"
    )
    
    def validate_confirm(self, value):
        """Valide que la confirmation est True."""
        if not value:
            raise serializers.ValidationError(
                "Vous devez confirmer la réinitialisation en envoyant 'confirm: true'."
            )
        return value
    
    def update(self, instance, validated_data):
        """Réinitialise toutes les préférences aux valeurs par défaut."""
        instance.reset_to_defaults()
        return instance


