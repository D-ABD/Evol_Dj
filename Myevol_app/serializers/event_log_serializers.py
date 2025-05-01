from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from django.contrib.auth import get_user_model

from ..models.event_log_model import EventLog

User = get_user_model()

class EventLogSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle EventLog.
    
    Expose les événements du journal avec leurs métadonnées
    ainsi que des champs calculés pour l'UX comme temps écoulé et résumé.
    """
    temps_écoulé = serializers.SerializerMethodField()
    résumé = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username', default=None)
    user_id = serializers.ReadOnlyField(source='user.id', default=None)
    
    class Meta:
        model = EventLog
        fields = [
            'id', 'user', 'user_username', 'user_id', 'action', 'description',
            'created_at', 'metadata', 'severity', 'temps_écoulé', 'résumé'
        ]
        read_only_fields = ['id', 'created_at', 'temps_écoulé', 'résumé']
        
    def validate_severity(self, value):
        """
        Valide que la sévérité est conforme aux choix disponibles.
        """
        valid_severities = dict(EventLog.SEVERITY_CHOICES).keys()
        if value not in valid_severities:
            raise serializers.ValidationError(f"Sévérité invalide : {value}. Doit être dans {list(valid_severities)}.")
        return value
        
    
    def get_temps_écoulé(self, obj):
        """
        Calcule le temps écoulé depuis la création de l'événement.

        Returns:
            dict: Détail du temps écoulé en secondes, minutes, heures et jours.
        """
        now = timezone.now()
        delta = now - obj.created_at
        return {
            'total_seconds': int(delta.total_seconds()),
            'days': delta.days,
            'hours': int(delta.seconds / 3600),
            'minutes': int((delta.seconds % 3600) / 60),
            'seconds': delta.seconds % 60,
            'human_format': self._format_timedelta_human(delta)
        }
    
    def get_résumé(self, obj):
        """
        Génère un résumé concis de l'événement.

        Returns:
            str: Action + date formatée.
        """
        return f"{obj.action} ({obj.created_at.strftime('%d/%m/%Y %H:%M')})"
    
    def _format_timedelta_human(self, delta):
        """
        Convertit un timedelta en format lisible par l'humain.

        Args:
            delta (timedelta): Différence de temps.

        Returns:
            str: Description humanisée.
        """
        if delta.days > 0:
            return f"il y a {delta.days} jour{'s' if delta.days > 1 else ''}"
        hours = delta.seconds // 3600
        if hours > 0:
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        minutes = (delta.seconds % 3600) // 60
        if minutes > 0:
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        return "à l'instant"


class EventLogDetailSerializer(EventLogSerializer):
    """
    Serializer détaillé pour un événement unique.
    
    Ajoute des informations supplémentaires sur les métadonnées de l'événement.
    """
    has_metadata = serializers.BooleanField()
    formatted_metadata = serializers.SerializerMethodField()
    
    class Meta(EventLogSerializer.Meta):
        fields = EventLogSerializer.Meta.fields + ['has_metadata', 'formatted_metadata']
    
    def get_formatted_metadata(self, obj):
        """
        Formate les métadonnées selon le type d'action.

        Returns:
            dict | None: Métadonnées formatées pour affichage.
        """
        if not obj.metadata or not isinstance(obj.metadata, dict):
            return None

        if obj.action == 'attribution_badge' and 'badge_id' in obj.metadata:
            badge_id = obj.metadata.get('badge_id')
            badge_name = obj.metadata.get('badge_name', 'Badge inconnu')
            return {
                'formatted': f"Badge attribué : {badge_name} (ID: {badge_id})",
                'details': obj.metadata
            }

        if obj.action == 'defi_termine' and 'challenge_id' in obj.metadata:
            challenge_id = obj.metadata.get('challenge_id')
            return {
                'formatted': f"Défi complété (ID: {challenge_id})",
                'details': obj.metadata
            }

        return {
            'formatted': ', '.join([f"{k}: {v}" for k, v in obj.metadata.items()]),
            'details': obj.metadata
        }


class EventLogStatisticsSerializer(serializers.Serializer):
    """
    Serializer pour produire des statistiques sur les événements enregistrés.
    
    Donne des infos sur le volume, la répartition et les tendances des événements.
    """
    period_days = serializers.IntegerField(default=30)
    total_events = serializers.SerializerMethodField()
    events_by_action = serializers.SerializerMethodField()
    events_by_severity = serializers.SerializerMethodField()
    events_by_time = serializers.SerializerMethodField()
    most_recent = serializers.SerializerMethodField()
    
    def get_total_events(self, obj):
        """
        Retourne le nombre total d'événements sur la période demandée.
        """
        user = obj.get('user')
        period_days = obj.get('period_days', 30)
        since = timezone.now() - timedelta(days=period_days)
        query = EventLog.objects.filter(created_at__gte=since)

        if user:
            query = query.filter(user=user)

        return query.count()

    def get_events_by_action(self, obj):
        """
        Retourne la répartition des événements par action.
        """
        user = obj.get('user')
        period_days = obj.get('period_days', 30)
        return EventLog.get_action_counts(days=period_days, user=user)

    def get_events_by_severity(self, obj):
        """
        Retourne la répartition des événements par niveau de gravité.
        """
        user = obj.get('user')
        period_days = obj.get('period_days', 30)
        since = timezone.now() - timedelta(days=period_days)
        query = EventLog.objects.filter(created_at__gte=since)

        if user:
            query = query.filter(user=user)

        aggregated = query.values('severity').annotate(total=Count('id'))
        return {item['severity']: item['total'] for item in aggregated}

    def get_events_by_time(self, obj):
        """
        Retourne la répartition temporelle (24h, 7j, 30j).
        """
        user = obj.get('user')
        now = timezone.now()

        last_day = now - timedelta(days=1)
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        query = EventLog.objects
        if user:
            query = query.filter(user=user)

        return {
            'last_24h': query.filter(created_at__gte=last_day).count(),
            'last_7d': query.filter(created_at__gte=last_week).count(),
            'last_30d': query.filter(created_at__gte=last_month).count()
        }

    def get_most_recent(self, obj):
        """
        Retourne les 5 événements les plus récents.
        """
        user = obj.get('user')
        query = EventLog.objects
        if user:
            query = query.filter(user=user)

        recent = query.order_by('-created_at')[:5]
        return EventLogSerializer(recent, many=True).data


class UserEventLogSerializer(serializers.Serializer):
    """
    Serializer pour l'activité récente d'un utilisateur à partir des événements.
    """
    user_id = serializers.IntegerField(source='id')
    username = serializers.CharField()
    total_events = serializers.SerializerMethodField()
    recent_activity = serializers.SerializerMethodField()
    first_event = serializers.SerializerMethodField()
    last_event = serializers.SerializerMethodField()
    
    def get_total_events(self, user):
        """Retourne le nombre total d'événements liés à l'utilisateur."""
        return user.event_logs.count()
    
    def get_recent_activity(self, user):
        """Retourne les 5 derniers événements de l'utilisateur."""
        recent = user.event_logs.all().order_by('-created_at')[:5]
        return EventLogSerializer(recent, many=True).data
    
    def get_first_event(self, user):
        """Retourne le tout premier événement de l'utilisateur."""
        first = user.event_logs.all().order_by('created_at').first()
        if not first:
            return None
        return EventLogSerializer(first).data
    
    def get_last_event(self, user):
        """Retourne le dernier événement de l'utilisateur."""
        last = user.event_logs.all().order_by('-created_at').first()
        if not last:
            return None
        return EventLogSerializer(last).data
