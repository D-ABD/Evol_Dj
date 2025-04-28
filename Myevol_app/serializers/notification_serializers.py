from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models.notification_model import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Notification.
    Expose les notifications avec temps écoulé et type affiché.
    """
    type_display = serializers.CharField(read_only=True)
    time_since_created = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_username', 'message', 'notif_type', 'type_display',
            'is_read', 'read_at', 'created_at', 'archived', 'scheduled_at',
            'time_since_created'
        ]
        read_only_fields = ['created_at', 'read_at', 'type_display']

    def get_time_since_created(self, obj):
        """Retourne le temps écoulé depuis la création de la notification sous forme lisible."""
        now = timezone.now()
        delta = now - obj.created_at

        if delta.days > 0:
            if delta.days == 1:
                return "hier"
            if delta.days < 7:
                return f"il y a {delta.days} jours"
            if delta.days < 30:
                weeks = delta.days // 7
                return f"il y a {weeks} semaine{'s' if weeks > 1 else ''}"
            if delta.days < 365:
                months = delta.days // 30
                return f"il y a {months} mois"
            years = delta.days // 365
            return f"il y a {years} an{'s' if years > 1 else ''}"

        hours = delta.seconds // 3600
        if hours > 0:
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"

        minutes = (delta.seconds % 3600) // 60
        if minutes > 0:
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"

        return "à l'instant"


class NotificationListSerializer(NotificationSerializer):
    """
    Serializer simplifié pour afficher une liste de notifications.
    """
    class Meta(NotificationSerializer.Meta):
        fields = [
            'id', 'message', 'notif_type', 'type_display', 
            'is_read', 'created_at', 'time_since_created'
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'une notification par un utilisateur.
    """
    class Meta:
        model = Notification
        fields = ['message', 'notif_type', 'scheduled_at']

    def create(self, validated_data):
        """Créé une notification associée à l'utilisateur courant."""
        request = self.context.get('request')
        user = request.user if request else None
        if not user:
            raise serializers.ValidationError("L'utilisateur est requis pour créer une notification.")

        return Notification.create_notification(
            user=user,
            message=validated_data['message'],
            notif_type=validated_data.get('notif_type', 'info'),
            scheduled_at=validated_data.get('scheduled_at')
        )


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour mettre à jour l'état d'une notification (lue/archivée).
    """
    mark_as_read = serializers.BooleanField(required=False, write_only=True)
    archive = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Notification
        fields = ['is_read', 'archived', 'mark_as_read', 'archive']
        read_only_fields = ['read_at']

    def update(self, instance, validated_data):
        """Met à jour l'instance selon les actions demandées."""
        if validated_data.pop('mark_as_read', False):
            instance.mark_as_read()

        if validated_data.pop('archive', False):
            instance.archive()

        return super().update(instance, validated_data)


class NotificationCountSerializer(serializers.Serializer):
    """
    Serializer pour compter les notifications par statut et type.
    """
    total = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    today = serializers.SerializerMethodField()
    by_type = serializers.SerializerMethodField()

    def get_total(self, user):
        return user.notifications.filter(archived=False).count()

    def get_unread(self, user):
        return user.notifications.filter(is_read=False, archived=False).count()

    def get_today(self, user):
        today = timezone.now().date()
        return user.notifications.filter(created_at__date=today, archived=False).count()

    def get_by_type(self, user):
        result = {}
        for notif_type, _ in Notification.NOTIF_TYPES:
            notifications = user.notifications.filter(notif_type=notif_type, archived=False)
            result[notif_type] = {
                'total': notifications.count(),
                'unread': notifications.filter(is_read=False).count()
            }
        return result


class NotificationBulkActionSerializer(serializers.Serializer):
    """
    Serializer pour effectuer des actions de masse sur les notifications.
    """
    action = serializers.ChoiceField(
        choices=['mark_all_read', 'archive_all', 'archive_read'],
        help_text="Action à effectuer"
    )
    notif_type = serializers.ChoiceField(
        choices=[choice[0] for choice in Notification.NOTIF_TYPES] + ['all'],
        default='all',
        help_text="Type de notification concerné"
    )

    def save(self, **kwargs):
        """Applique l'action en masse sur les notifications de l'utilisateur."""
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("L'utilisateur est requis pour cette action.")

        action = self.validated_data['action']
        notif_type = self.validated_data['notif_type']

        queryset = user.notifications.all()
        if notif_type != 'all':
            queryset = queryset.filter(notif_type=notif_type)

        if action == 'mark_all_read':
            count = queryset.filter(is_read=False).update(is_read=True, read_at=timezone.now())
            message = f"{count} notifications marquées comme lues"
        elif action == 'archive_all':
            count = queryset.filter(archived=False).update(archived=True)
            message = f"{count} notifications archivées"
        elif action == 'archive_read':
            count = queryset.filter(is_read=True, archived=False).update(archived=True)
            message = f"{count} notifications lues archivées"
        else:
            raise serializers.ValidationError("Action inconnue.")

        return {'success': True, 'count': count, 'message': message}
