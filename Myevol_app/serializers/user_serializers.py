from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from collections import OrderedDict
from django.db.models import Count

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User.
    
    Expose les informations de base de l'utilisateur.
    """
    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    total_entries = serializers.ReadOnlyField()
    current_streak = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'short_name',
            'avatar_url', 'xp', 'total_entries', 'current_streak',
            'longest_streak', 'level', 'level_progress', 'date_joined',
            'last_login'
        ]
        read_only_fields = [
            'total_entries', 'current_streak', 'longest_streak',
            'level', 'level_progress', 'date_joined', 'last_login'
        ]
    
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur."""
        return obj.get_full_name()
    
    def get_short_name(self, obj):
        """Retourne le prénom ou le username si le prénom est vide."""
        return obj.get_short_name()
    
    def get_current_streak(self, obj):
        """Retourne la série actuelle de jours consécutifs avec entrées."""
        return obj.current_streak()
    
    def get_level(self, obj):
        """Retourne le niveau actuel de l'utilisateur."""
        return obj.level()
    
    def get_level_progress(self, obj):
        """Retourne la progression du niveau actuel en pourcentage."""
        return obj.level_progress()


class UserProfileSerializer(UserSerializer):
    """
    Serializer pour le profil complet d'un utilisateur.
    
    Étend UserSerializer avec des statistiques supplémentaires.
    """
    mood_average = serializers.SerializerMethodField()
    stats_summary = serializers.SerializerMethodField()
    activity_summary = serializers.SerializerMethodField()
    badges_count = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'mood_average', 'stats_summary', 'activity_summary',
            'badges_count'
        ]
    
    def get_mood_average(self, obj):
        """Retourne la moyenne d'humeur sur différentes périodes."""
        mood_7d = obj.mood_average(days=7)
        mood_30d = obj.mood_average(days=30)
        mood_all = obj.mood_average(days=None)
        
        return {
            'week': round(mood_7d, 1) if mood_7d is not None else None,
            'month': round(mood_30d, 1) if mood_30d is not None else None,
            'all_time': round(mood_all, 1) if mood_all is not None else None
        }
    
    def get_stats_summary(self, obj):
        """Retourne un résumé des statistiques de l'utilisateur."""
        return {
            'total_entries': obj.total_entries,
            'current_streak': obj.current_streak(),
            'longest_streak': obj.longest_streak,
            'level': obj.level(),
            'xp': obj.xp
        }
    
    def get_activity_summary(self, obj):
        """Retourne un résumé de l'activité récente de l'utilisateur."""
        today = timezone.now().date()
        entries_today = obj.entries_today()
        
        # Calculer les entrées des 7 derniers jours
        last_week = today - timedelta(days=7)
        entries_last_week = obj.entries.filter(
            created_at__date__gte=last_week
        ).count()
        
        # Calculer les entrées des 30 derniers jours
        last_month = today - timedelta(days=30)
        entries_last_month = obj.entries.filter(
            created_at__date__gte=last_month
        ).count()
        
        # Déterminer si l'utilisateur est actif
        is_active = entries_today > 0
        
        return {
            'entries_today': entries_today,
            'entries_last_week': entries_last_week,
            'entries_last_month': entries_last_month,
            'is_active_today': is_active,
            'days_since_last_entry': 0 if is_active else self._days_since_last_entry(obj)
        }
    
    def get_badges_count(self, obj):
        """Retourne le nombre de badges de l'utilisateur."""
        return obj.badges.count()
    
    def _days_since_last_entry(self, obj):
        """Calcule le nombre de jours depuis la dernière entrée."""
        today = timezone.now().date()
        last_entry = obj.entries.order_by('-created_at').first()
        
        if not last_entry:
            return None
            
        last_date = last_entry.created_at.date()
        return (today - last_date).days


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour mettre à jour les informations de l'utilisateur.
    
    Permet de modifier le profil sans toucher aux champs sensibles.
    """
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Mot de passe actuel (requis pour changer le mot de passe)"
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Nouveau mot de passe"
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'avatar_url', 'current_password', 'new_password'
        ]
    
    def validate(self, data):
        """Validation des données de mise à jour du profil."""
        # Si on essaie de changer le mot de passe
        if 'new_password' in data:
            # Le mot de passe actuel est obligatoire
            if not data.get('current_password'):
                raise serializers.ValidationError({
                    'current_password': "Le mot de passe actuel est requis pour changer le mot de passe."
                })
            
            # Vérifier que le mot de passe actuel est correct
            if not self.instance.check_password(data.get('current_password')):
                raise serializers.ValidationError({
                    'current_password': "Le mot de passe actuel est incorrect."
                })
        
        return data
    
    def update(self, instance, validated_data):
        """Mise à jour de l'utilisateur avec gestion du mot de passe."""
        # Gérer le changement de mot de passe séparément
        if 'new_password' in validated_data:
            instance.set_password(validated_data.pop('new_password'))
        
        # Supprimer le mot de passe actuel des données à mettre à jour
        validated_data.pop('current_password', None)
        
        # Mettre à jour les autres champs
        return super().update(instance, validated_data)


class UserStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques détaillées d'un utilisateur.
    
    Fournit des insights sur l'activité et les performances de l'utilisateur.
    """
    mood_stats = serializers.SerializerMethodField()
    streak_stats = serializers.SerializerMethodField()
    activity_stats = serializers.SerializerMethodField()
    category_distribution = serializers.SerializerMethodField()
    
    def get_mood_stats(self, user):
        """Statistiques détaillées sur les humeurs de l'utilisateur."""
        # Moyennes d'humeur sur différentes périodes
        mood_7d = user.mood_average(days=7)
        mood_30d = user.mood_average(days=30)
        mood_90d = user.mood_average(days=90)
        mood_all = user.mood_average(days=None)
        
        # Calcul de la tendance
        trend = 'stable'
        if mood_7d is not None and mood_30d is not None:
            diff = mood_7d - mood_30d
            if diff > 0.5:
                trend = 'up'
            elif diff < -0.5:
                trend = 'down'
        
        # Répartition des humeurs
        mood_distribution = list(user.entries.values('mood')
                                 .annotate(count=Count('id'))
                                 .order_by('mood'))
        
        return {
            'averages': {
                'week': round(mood_7d, 1) if mood_7d is not None else None,
                'month': round(mood_30d, 1) if mood_30d is not None else None,
                'quarter': round(mood_90d, 1) if mood_90d is not None else None,
                'all_time': round(mood_all, 1) if mood_all is not None else None
            },
            'trend': trend,
            'distribution': {
                str(item['mood']): item['count'] for item in mood_distribution if item['mood'] is not None
            }
        }
    
    def get_streak_stats(self, user):
        """Statistiques sur les séries d'entrées consécutives."""
        return {
            'current': user.current_streak(),
            'longest': user.longest_streak,
            'has_entry_today': user.entries_today() > 0
        }
    
    def get_activity_stats(self, user):
        """Statistiques sur l'activité générale de l'utilisateur."""
        today = timezone.now().date()
        
        # Entrées par jour de la semaine
        from django.db.models import Count
        from django.db.models.functions import ExtractWeekDay
        
        weekday_counts = list(user.entries
                              .annotate(weekday=ExtractWeekDay('created_at'))
                              .values('weekday')
                              .annotate(count=Count('id'))
                              .order_by('weekday'))
        
        # Convertir en format jour de la semaine (0=Lundi, 6=Dimanche)
        weekday_names = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        weekday_distribution = {}
        
        for day in range(7):
            # Rechercher le jour dans les résultats
            count_entry = next((item for item in weekday_counts if item['weekday'] == day + 1), None)
            weekday_distribution[weekday_names[day]] = count_entry['count'] if count_entry else 0
        
        # Calculer les entrées par mois (12 derniers mois)
        from django.db.models.functions import TruncMonth
        month_counts = list(user.entries
                           .filter(created_at__date__gte=today - timedelta(days=365))
                           .annotate(month=TruncMonth('created_at'))
                           .values('month')
                           .annotate(count=Count('id'))
                           .order_by('month'))
        
        # Formater les mois
        month_distribution = {
            item['month'].strftime('%B %Y'): item['count'] for item in month_counts
        }
        
        return {
            'total_entries': user.total_entries,
            'entries_today': user.entries_today(),
            'weekday_distribution': weekday_distribution,
            'month_distribution': month_distribution,
            'average_entries_per_day': round(user.total_entries / max(1, (today - user.date_joined.date()).days), 1)
        }
    
    def get_category_distribution(self, user):
        """Répartition des entrées par catégorie."""
        categories = user.entries_by_category()
        total = sum(categories.values())
        
        result = {}
        for category, count in categories.items():
            result[category] = {
                'count': count,
                'percentage': round((count / total) * 100, 1) if total > 0 else 0
            }
        
        # Trier par nombre d'entrées (décroissant)
        return OrderedDict(sorted(
            result.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        ))


class UserPreferencesSerializer(serializers.Serializer):
    """
    Serializer pour les préférences de l'utilisateur.
    
    Permet de récupérer et mettre à jour les préférences utilisateur.
    """
    dark_mode = serializers.BooleanField(default=False)
    accent_color = serializers.CharField(default="#6C63FF")
    font_choice = serializers.CharField(default="Roboto")
    enable_animations = serializers.BooleanField(default=True)
    notif_badge = serializers.BooleanField(default=True)
    notif_objectif = serializers.BooleanField(default=True)
    notif_info = serializers.BooleanField(default=True)
    notif_statistique = serializers.BooleanField(default=True)
    
    def to_representation(self, instance):
        """
        Récupère les préférences de l'utilisateur ou retourne des valeurs par défaut si elles sont absentes.
        """
        prefs = getattr(instance, 'userpreferences', None)
        if prefs is None:
            return {
                'dark_mode': False,
                'accent_color': "#6C63FF",
                'font_choice': "Roboto",
                'enable_animations': True,
                'notif_badge': True,
                'notif_objectif': True,
                'notif_info': True,
                'notif_statistique': True
            }
        
        return {
            'dark_mode': prefs.dark_mode,
            'accent_color': prefs.accent_color,
            'font_choice': prefs.font_choice,
            'enable_animations': prefs.enable_animations,
            'notif_badge': prefs.notif_badge,
            'notif_objectif': prefs.notif_objectif,
            'notif_info': prefs.notif_info,
            'notif_statistique': prefs.notif_statistique
        }

    
    def update(self, instance, validated_data):
        """
        Mise à jour des préférences de l'utilisateur.
        """
        from ..services.userpreference_service import create_or_update_preferences

        updated_prefs = create_or_update_preferences(instance, validated_data)

        # Recharge les préférences à jour sur l'utilisateur pour que to_representation fonctionne correctement
        instance.userpreferences = updated_prefs
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur.
    
    Gère la création d'un compte utilisateur avec validation.
    """
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
    
    def validate(self, data):
        """Validation des données d'inscription."""
        # Vérifier que les mots de passe correspondent
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': "Les mots de passe ne correspondent pas."
            })
        
        return data
    
    def create(self, validated_data):
        """Création d'un nouvel utilisateur."""
        # Supprimer password_confirm
        validated_data.pop('password_confirm')
        
        # Récupérer le mot de passe
        password = validated_data.pop('password')
        
        # Créer l'utilisateur
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserXpSerializer(serializers.Serializer):
    """
    Serializer pour gérer les points d'expérience d'un utilisateur.
    
    Permet d'ajouter des XP à un utilisateur.
    """
    amount = serializers.IntegerField(min_value=1, required=True)
    
    def validate_amount(self, value):
        """Validation du montant d'XP à ajouter."""
        if value <= 0:
            raise serializers.ValidationError("Le montant d'XP doit être positif.")
        return value
    
    def save(self, **kwargs):
        """Ajoute des XP à l'utilisateur."""
        user = self.context.get('user')
        amount = self.validated_data['amount']
        
        user.add_xp(amount)
        
        return {
            'success': True,
            'user': user.username,
            'amount_added': amount,
            'new_total': user.xp,
            'level': user.level(),
            'level_progress': user.level_progress()
        }