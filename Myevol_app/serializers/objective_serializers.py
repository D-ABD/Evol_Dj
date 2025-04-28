from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.db.models import Count

from ..models.objective_model import Objective

User = get_user_model()


class ObjectiveSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Objective.
    
    Expose les objectifs définis par l'utilisateur avec leurs métadonnées
    et les champs calculés comme progress_percent, days_remaining, etc.
    """
    progress_percent = serializers.IntegerField(read_only=True)
    days_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    is_achieved = serializers.SerializerMethodField()
    is_due_today = serializers.SerializerMethodField()
    entries_done = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Objective
        fields = [
            'id', 'user', 'user_username', 'title', 'category', 'done',
            'target_date', 'target_value', 'created_at',
            'progress_percent', 'days_remaining', 'is_overdue',
            'is_achieved', 'is_due_today', 'entries_done', 'status'
        ]
        read_only_fields = ['created_at', 'progress_percent', 'days_remaining', 
                           'is_overdue', 'is_achieved', 'is_due_today', 'entries_done', 'status']
    
    def get_days_remaining(self, obj):
        """Retourne le nombre de jours restants avant la date cible."""
        return obj.days_remaining()
    
    def get_is_overdue(self, obj):
        """Vérifie si l'objectif est en retard."""
        return obj.is_overdue()
    
    def get_is_achieved(self, obj):
        """Vérifie si l'objectif est atteint."""
        return obj.is_achieved()
    
    def get_is_due_today(self, obj):
        """Vérifie si la date cible de l'objectif est aujourd'hui."""
        return obj.is_due_today()
    
    def get_entries_done(self, obj):
        """Compte le nombre d'entrées correspondant à la catégorie de cet objectif."""
        return obj.entries_done()
    
    def get_status(self, obj):
        """
        Retourne le statut textuel de l'objectif.
        
        Statuts possibles:
        - 'completed': objectif terminé
        - 'overdue': objectif en retard
        - 'due_today': échéance aujourd'hui
        - 'upcoming': à venir
        """
        if obj.done:
            return 'completed'
        if obj.is_overdue():
            return 'overdue'
        if obj.is_due_today():
            return 'due_today'
        return 'upcoming'
    
    def validate_target_date(self, value):
        """Vérifie que la date cible n'est pas dans le passé."""
        if value < timezone.now().date():
            raise serializers.ValidationError("La date cible ne peut pas être dans le passé.")
        return value
    
    def create(self, validated_data):
        """Création d'un objectif avec l'utilisateur courant."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class ObjectiveListSerializer(ObjectiveSerializer):
    """
    Serializer pour la liste des objectifs.
    
    Version allégée pour l'affichage dans une liste.
    """
    class Meta(ObjectiveSerializer.Meta):
        fields = [
            'id', 'title', 'category', 'done', 'target_date',
            'progress_percent', 'days_remaining', 'status'
        ]


class ObjectiveDetailSerializer(ObjectiveSerializer):
    """
    Serializer pour les détails d'un objectif.
    
    Version étendue pour l'affichage détaillé d'un objectif.
    """
    formatted_target_date = serializers.SerializerMethodField()
    time_until_due = serializers.SerializerMethodField()
    
    class Meta(ObjectiveSerializer.Meta):
        fields = ObjectiveSerializer.Meta.fields + ['formatted_target_date', 'time_until_due']
    
    def get_formatted_target_date(self, obj):
        """Formatte la date cible de façon lisible."""
        return obj.target_date.strftime("%d %B %Y")
    
    def get_time_until_due(self, obj):
        """
        Retourne le temps restant avant l'échéance sous forme lisible.
        Par exemple: "3 jours", "Aujourd'hui", "En retard de 2 jours"
        """
        days = obj.days_remaining()
        
        if days < 0:
            return f"En retard de {abs(days)} jour{'s' if abs(days) > 1 else ''}"
        elif days == 0:
            return "Aujourd'hui"
        elif days == 1:
            return "Demain"
        elif days < 7:
            return f"{days} jours"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} semaine{'s' if weeks > 1 else ''}"
        else:
            months = days // 30
            return f"{months} mois"


class ObjectiveCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer pour marquer un objectif comme complété.
    
    Utilisé uniquement pour mettre à jour le champ 'done'.
    """
    class Meta:
        model = Objective
        fields = ['done']


class ObjectiveStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques des objectifs.
    
    Fournit des statistiques globales sur les objectifs d'un utilisateur.
    """
    total = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    overdue = serializers.SerializerMethodField()
    by_category = serializers.SerializerMethodField()
    upcoming_today = serializers.SerializerMethodField()
    upcoming_week = serializers.SerializerMethodField()
    recent_completions = serializers.SerializerMethodField()
    
    def get_total(self, user):
        """Nombre total d'objectifs."""
        return user.objectives.count()

    def get_completed(self, user):
        """Nombre total d'objectifs complétés."""
        return user.objectives.filter(done=True).count()

    def get_completion_rate(self, user):
        """Taux de complétion en pourcentage."""
        total = self.get_total(user)
        if total == 0:
            return 0.0
        completed = self.get_completed(user)
        return round((completed / total) * 100, 1)

    def get_overdue(self, user):
        """Nombre d'objectifs en retard."""
        today = timezone.now().date()
        return user.objectives.filter(done=False, target_date__lt=today).count()

    def get_by_category(self, user):
        """Répartition des objectifs par catégorie."""
        categories = user.objectives.values('category').annotate(count=Count('category')).order_by('-count')
        return {cat['category']: cat['count'] for cat in categories}

    def get_upcoming_today(self, user):
        """Nombre d'objectifs dus aujourd'hui."""
        today = timezone.now().date()
        return user.objectives.filter(done=False, target_date=today).count()

    def get_upcoming_week(self, user):
        """Nombre d'objectifs dont l'échéance est dans les 7 prochains jours."""
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        return user.objectives.filter(done=False, target_date__gt=today, target_date__lte=end_of_week).count()

    def get_recent_completions(self, user):
        """Liste des objectifs récemment complétés (7 derniers jours)."""
        last_week = timezone.now().date() - timedelta(days=7)
        recent = user.objectives.filter(done=True, target_date__gte=last_week).order_by('-target_date')[:5]
        return ObjectiveListSerializer(recent, many=True).data


class ObjectiveUpcomingSerializer(serializers.Serializer):
    """
    Serializer pour les objectifs à venir.
    
    Regroupe les objectifs par échéance (aujourd'hui, cette semaine, ce mois).
    """
    today = serializers.SerializerMethodField()
    this_week = serializers.SerializerMethodField()
    this_month = serializers.SerializerMethodField()

    def get_queryset(self, user):
        """Base queryset filtré sur l'utilisateur et non terminé."""
        return Objective.objects.filter(user=user, done=False)

    def get_today(self, user):
        """Objectifs dus aujourd'hui."""
        today = timezone.now().date()
        return ObjectiveListSerializer(
            self.get_queryset(user).filter(target_date=today).order_by('title'), many=True
        ).data

    def get_this_week(self, user):
        """Objectifs dus cette semaine (hors aujourd'hui)."""
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        end_of_week = today + timedelta(days=7)
        return ObjectiveListSerializer(
            self.get_queryset(user).filter(target_date__gte=tomorrow, target_date__lte=end_of_week).order_by('target_date'), many=True
        ).data

    def get_this_month(self, user):
        """Objectifs dus ce mois-ci (hors cette semaine)."""
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        end_of_month = today + timedelta(days=30)
        return ObjectiveListSerializer(
            self.get_queryset(user).filter(target_date__gt=end_of_week, target_date__lte=end_of_month).order_by('target_date'), many=True
        ).data


class ObjectiveCategorySerializer(serializers.Serializer):
    """
    Serializer pour les suggestions de catégories d'objectifs.
    
    Retourne les catégories les plus utilisées par l'utilisateur.
    """
    categories = serializers.SerializerMethodField()

    def get_categories(self, user):
        """Liste des catégories les plus utilisées."""
        categories = Objective.objects.filter(user=user) \
            .values('category') \
            .annotate(count=Count('category')) \
            .order_by('-count')[:10]
        return [item['category'] for item in categories]
