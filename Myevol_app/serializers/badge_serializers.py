from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count
from collections import defaultdict

from ..models.badge_model import Badge, BadgeTemplate

User = get_user_model()


class BadgeSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Badge.
    
    Expose les badges attribués à un utilisateur avec leurs métadonnées
    et les champs calculés comme was_earned_today, is_recent, etc.
    """
    was_earned_today = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    days_since_earned = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'icon', 'date_obtenue', 'level',
            'was_earned_today', 'is_recent', 'days_since_earned',
            'user_id', 'user_username'
        ]
        read_only_fields = ['date_obtenue']
    
    def get_was_earned_today(self, obj):
        """Retourne True si le badge a été obtenu aujourd'hui."""
        return obj.was_earned_today()
    
    def get_is_recent(self, obj):
        """Retourne True si le badge a été obtenu dans les 7 derniers jours."""
        today = timezone.now().date()
        delta = today - obj.date_obtenue
        return delta.days <= 7
    
    def get_days_since_earned(self, obj):
        """Retourne le nombre de jours écoulés depuis l'obtention du badge."""
        today = timezone.now().date()
        delta = today - obj.date_obtenue
        return delta.days


class BadgeTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle BadgeTemplate.
    
    Expose les modèles de badges disponibles dans le système.
    """
    level_number = serializers.SerializerMethodField()
    
    class Meta:
        model = BadgeTemplate
        fields = [
            'id', 'name', 'description', 'icon', 'condition', 
            'level', 'animation_url', 'color_theme', 'level_number'
        ]
        read_only_fields = ['id']

    
    def get_level_number(self, obj):
        """
        Extrait le numéro de niveau à partir du nom du badge
        si c'est un badge de type 'Niveau X'.
        """
        return obj.extract_level_number()

    def validate_color_theme(self, value):
        """
        Valide que la couleur est bien au format hexadécimal #RRGGBB.
        """
        import re
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
            raise serializers.ValidationError("La couleur doit être au format HEX (#RRGGBB).")
        return value

class BadgeTemplateWithProgressSerializer(BadgeTemplateSerializer):
    """
    Extension du serializer BadgeTemplate incluant la progression
    de l'utilisateur vers l'obtention du badge.
    """
    progress = serializers.SerializerMethodField()
    can_unlock = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    
    class Meta(BadgeTemplateSerializer.Meta):
        fields = BadgeTemplateSerializer.Meta.fields + ['progress', 'can_unlock', 'is_unlocked']
    
    def get_progress(self, obj):
        """
        Retourne les informations de progression vers ce badge.
        La progression est calculée pour l'utilisateur spécifié ou l'utilisateur courant.
        """
        user = self._get_user()
        if user and user.is_authenticated:
            return obj.get_progress(user)
        return {"percent": 0, "unlocked": False, "current": 0, "target": 0}
    
    def get_can_unlock(self, obj):
        """
        Retourne True si l'utilisateur peut débloquer ce badge.
        """
        user = self._get_user()
        if user and user.is_authenticated:
            return obj.check_unlock(user)
        return False
    
    def get_is_unlocked(self, obj):
        """
        Retourne True si l'utilisateur a déjà débloqué ce badge.
        """
        user = self._get_user()
        if user and user.is_authenticated:
            return user.badges.filter(name=obj.name).exists()
        return False
    
    def _get_user(self):
        """
        Récupère l'utilisateur à partir du contexte.
        Supporte soit l'utilisateur de la requête, soit un utilisateur spécifié.
        """
        # Vérifier d'abord si un utilisateur spécifique a été fourni dans le contexte
        user_id = self.context.get('user_id')
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
                
        # Sinon, utiliser l'utilisateur de la requête
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user
            
        return None


class UserBadgeStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques de badges d'un utilisateur.
    
    Fournit des informations sur les badges obtenus et disponibles pour un utilisateur,
    y compris les statistiques récentes et la progression globale.
    """
    total_badges = serializers.SerializerMethodField()
    recent_badges = serializers.SerializerMethodField()
    unlocked_percentage = serializers.SerializerMethodField()
    badges_by_category = serializers.SerializerMethodField()
    next_available_badges = serializers.SerializerMethodField()
    
    def get_total_badges(self, user):
        """Nombre total de badges obtenus par l'utilisateur."""
        return user.badges.count()
    
    def get_recent_badges(self, user):
        """Badges obtenus au cours des 7 derniers jours."""
        today = timezone.now().date()
        week_ago = today - timezone.timedelta(days=7)
        recent = user.badges.filter(date_obtenue__gte=week_ago)
        return BadgeSerializer(recent, many=True).data
    
    def get_unlocked_percentage(self, user):
        """Pourcentage de badges débloqués sur le total disponible."""
        total_templates = BadgeTemplate.objects.count()
        if total_templates == 0:
            return 0
        return round((user.badges.count() / total_templates) * 100, 1)
    
    def get_badges_by_category(self, user):
        """Badges groupés par catégorie/type."""
        # On utilise le préfixe du nom comme catégorie pour cet exemple
        # Dans une implémentation réelle, vous pourriez ajouter un champ 'category' au modèle
        badges = user.badges.all()
        categories = defaultdict(list)
        
        for badge in badges:
            if badge.name.startswith("Niveau"):
                categories["Niveaux"].append(BadgeSerializer(badge).data)
            elif "entrée" in badge.name.lower():
                categories["Progression"].append(BadgeSerializer(badge).data)
            else:
                categories["Accomplissements"].append(BadgeSerializer(badge).data)
                
        return dict(categories)
    
    def get_next_available_badges(self, user):
        """Liste des prochains badges que l'utilisateur peut débloquer."""
        # On récupère les templates que l'utilisateur n'a pas encore débloqués
        unlocked_names = user.badges.values_list('name', flat=True)
        available_templates = BadgeTemplate.objects.exclude(name__in=unlocked_names)
        
        # On vérifie lesquels peuvent être débloqués
        next_badges = []
        for template in available_templates:
            if template.check_unlock(user):
                next_badges.append(template)
        
        return BadgeTemplateWithProgressSerializer(
            next_badges, 
            many=True, 
            context={'request': self.context.get('request')}
        ).data