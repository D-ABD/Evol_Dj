from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models.challenge_model import Challenge, ChallengeProgress

User = get_user_model()


class ChallengeSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Challenge.
    
    Expose les défis avec leurs métadonnées et les champs calculés
    comme is_active, days_remaining et participants_count.
    """
    is_active = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'start_date', 'end_date',
                  'is_active', 'days_remaining', 'participants_count']
        read_only_fields = ['id', 'is_active', 'days_remaining', 'participants_count']

    def validate_start_date(self, value):
        """
        Valide que la date de début n'est pas dans le passé.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("La date de début ne peut pas être dans le passé.")
        return value

    def validate(self, data):
        """
        Valide que start_date < end_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("La date de début doit être avant la date de fin.")
        return data


class ChallengeProgressSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ChallengeProgress.
    
    Expose la progression d'un utilisateur sur un défi spécifique.
    """
    progress = serializers.SerializerMethodField()
    challenge_title = serializers.ReadOnlyField(source='challenge.title')
    challenge_description = serializers.ReadOnlyField(source='challenge.description')
    days_remaining = serializers.ReadOnlyField(source='challenge.days_remaining')
    start_date = serializers.ReadOnlyField(source='challenge.start_date')
    end_date = serializers.ReadOnlyField(source='challenge.end_date')
    
    class Meta:
        model = ChallengeProgress
        fields = [
            'id', 'user', 'challenge', 'completed', 'completed_at',
            'progress', 'challenge_title', 'challenge_description',
            'days_remaining', 'start_date', 'end_date'
        ]
        read_only_fields = ['completed', 'completed_at', 'progress']
    
    def get_progress(self, obj):
        """
        Récupère la progression actuelle de l'utilisateur sur ce défi.
        """
        return obj.get_progress()


class ChallengeDetailSerializer(ChallengeSerializer):
    """
    Serializer étendu pour les détails d'un défi.
    
    Inclut la progression de l'utilisateur courant si disponible.
    """
    user_progress = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()
    
    class Meta(ChallengeSerializer.Meta):
        fields = ChallengeSerializer.Meta.fields + ['user_progress', 'joined']
    
    def get_user_progress(self, obj):
        """
        Retourne la progression de l'utilisateur courant sur ce défi.
        """
        user = self._get_user()
        if not user or not user.is_authenticated:
            return None
        return obj.get_progress(user)
    
    def get_joined(self, obj):
        """
        Retourne True si l'utilisateur courant participe à ce défi.
        """
        user = self._get_user()
        if not user or not user.is_authenticated:
            return False
        return ChallengeProgress.objects.filter(user=user, challenge=obj).exists()
    
    def _get_user(self):
        """
        Récupère l'utilisateur à partir du contexte.
        """
        user_id = self.context.get('user_id')
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
        
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user
        return None


class UserChallengeStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques des défis d'un utilisateur.
    
    Fournit des informations sur les défis actifs, complétés et disponibles
    pour un utilisateur donné.
    """
    total_challenges_joined = serializers.SerializerMethodField()
    active_challenges = serializers.SerializerMethodField()
    completed_challenges = serializers.SerializerMethodField()
    available_challenges = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    
    def get_total_challenges_joined(self, user):
        """Nombre total de défis rejoints par l'utilisateur."""
        return user.challenges.count()
    
    def get_active_challenges(self, user):
        """Liste des défis actifs de l'utilisateur (rejoints mais non complétés)."""
        today = timezone.now().date()
        progresses = user.challenges.filter(
            challenge__end_date__gte=today,
            completed=False
        ).select_related('challenge')
        return ChallengeProgressSerializer(progresses, many=True).data
    
    def get_completed_challenges(self, user):
        """Liste des défis complétés par l'utilisateur."""
        progresses = user.challenges.filter(completed=True).select_related('challenge')
        return ChallengeProgressSerializer(progresses, many=True).data
    
    def get_available_challenges(self, user):
        """Liste des défis disponibles non rejoints par l'utilisateur."""
        today = timezone.now().date()
        joined_ids = user.challenges.values_list('challenge_id', flat=True)
        available = Challenge.objects.filter(end_date__gte=today).exclude(id__in=joined_ids)
        return ChallengeSerializer(available, many=True).data
    
    def get_completion_rate(self, user):
        """Taux de complétion des défis (défis complétés / défis rejoints)."""
        total = user.challenges.count()
        if total == 0:
            return 0
        completed = user.challenges.filter(completed=True).count()
        return round((completed / total) * 100, 1)


class ParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer pour les participants d'un défi.
    
    Expose les informations de base sur l'utilisateur et sa progression sur le défi.
    """
    username = serializers.ReadOnlyField(source='user.username')
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = ChallengeProgress
        fields = ['id', 'user', 'username', 'completed', 'completed_at', 'progress']
    
    def get_progress(self, obj):
        """Récupère la progression actuelle du participant sur le défi."""
        return obj.get_progress()
