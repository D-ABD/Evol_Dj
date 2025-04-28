from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.db.models import Avg, Count

from ..models.journal_model import JournalEntry, JournalMedia

User = get_user_model()

class JournalMediaSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle JournalMedia.
    
    Expose les fichiers multimédias associés aux entrées de journal.
    """
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = JournalMedia
        fields = [
            'id', 'entry', 'file', 'type', 'created_at', 
            'file_url', 'file_size', 'file_type_display'
        ]
        read_only_fields = ['created_at', 'file_url', 'file_size', 'file_type_display']
    
    def get_file_url(self, obj):
        """Retourne l'URL complète du fichier média."""
        return obj.file_url()
    
    def get_file_size(self, obj):
        """Retourne la taille du fichier média en octets."""
        return obj.file_size()
    
    def validate(self, data):
        """Valide que le type du fichier correspond bien à son contenu."""
        instance = JournalMedia(**data)
        try:
            instance.validate_file_type()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return data


class JournalEntrySerializer(serializers.ModelSerializer):
    """
    Serializer de base pour le modèle JournalEntry.
    
    Expose les entrées de journal de manière enrichie avec humeur, média et délai.
    """
    mood_emoji = serializers.SerializerMethodField()
    media = JournalMediaSerializer(many=True, read_only=True)
    user_username = serializers.ReadOnlyField(source='user.username')
    time_since_creation = serializers.SerializerMethodField()
    
    class Meta:
        model = JournalEntry
        fields = [
            'id', 'user', 'user_username', 'content', 'mood', 'mood_emoji',
            'category', 'created_at', 'updated_at', 'media', 'time_since_creation'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user_username', 'mood_emoji']
    
    def get_mood_emoji(self, obj):
        """Retourne l'emoji correspondant à la note d'humeur."""
        return obj.get_mood_emoji()
    
    def get_time_since_creation(self, obj):
        """Retourne une description relative du temps écoulé depuis la création."""
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
    
    def validate_content(self, value):
        """Valide que le contenu est d'une longueur suffisante."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Le contenu doit comporter au moins 5 caractères.")
        return value
    
    def create(self, validated_data):
        """Crée une entrée de journal pour l'utilisateur courant."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class JournalEntryDetailSerializer(JournalEntrySerializer):
    """
    Serializer détaillé pour une entrée de journal.
    
    Ajoute des informations comme l'éditabilité et le nombre d'entrées du jour.
    """
    is_editable = serializers.SerializerMethodField()
    day_entries_count = serializers.SerializerMethodField()
    
    class Meta(JournalEntrySerializer.Meta):
        fields = JournalEntrySerializer.Meta.fields + ['is_editable', 'day_entries_count']
    
    def get_is_editable(self, obj):
        """Détermine si l'entrée est encore modifiable (24h après création)."""
        now = timezone.now()
        edit_window = timedelta(hours=24)
        return now - obj.created_at <= edit_window
    
    def get_day_entries_count(self, obj):
        """Retourne combien d'entrées ont été créées le même jour par l'utilisateur."""
        created_date = obj.created_at.date()
        return JournalEntry.objects.filter(
            user=obj.user,
            created_at__date=created_date
        ).count()


# ✅ JournalEntryCreateSerializer : valide bien content (min 5 caractères)
class JournalEntryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer une entrée de journal avec fichiers médias.
    """
    media_files = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    media_types = serializers.ListField(
        child=serializers.ChoiceField(choices=JournalMedia._meta.get_field('type').choices),
        required=False, write_only=True
    )
    
    class Meta:
        model = JournalEntry
        fields = ['content', 'mood', 'category', 'media_files', 'media_types']
    
    def validate(self, data):
        """Valide la correspondance entre fichiers et types associés."""
        media_files = data.get('media_files', [])
        media_types = data.get('media_types', [])
        
        if len(media_files) != len(media_types):
            raise serializers.ValidationError(
                "Le nombre de fichiers et de types de médias doit correspondre."
            )
        return data
    
    def validate_content(self, value):
        """Valide que le contenu est d'une longueur suffisante."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Le contenu doit comporter au moins 5 caractères.")
        return value

    def create(self, validated_data):
        """Crée une entrée et ses médias associés."""
        media_files = validated_data.pop('media_files', [])
        media_types = validated_data.pop('media_types', [])
        
        request = self.context.get('request')
        validated_data['user'] = request.user
        entry = JournalEntry.objects.create(**validated_data)
        
        for file, type in zip(media_files, media_types):
            JournalMedia.objects.create(entry=entry, file=file, type=type)
        
        return entry
    
    def validate(self, data):
        """Valide la correspondance entre fichiers et types associés."""
        media_files = data.get('media_files', [])
        media_types = data.get('media_types', [])
        
        if len(media_files) != len(media_types):
            raise serializers.ValidationError(
                "Le nombre de fichiers et de types de médias doit correspondre."
            )
        return data
    
    def create(self, validated_data):
        """Crée une entrée et ses médias associés."""
        media_files = validated_data.pop('media_files', [])
        media_types = validated_data.pop('media_types', [])
        
        request = self.context.get('request')
        validated_data['user'] = request.user
        entry = JournalEntry.objects.create(**validated_data)
        
        for file, type in zip(media_files, media_types):
            JournalMedia.objects.create(entry=entry, file=file, type=type)
        
        return entry


class JournalEntryCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer pour affichage des entrées sous forme de calendrier.
    
    Fournit des métriques condensées (nombre, humeur, catégories).
    """
    day = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True)
    mood_avg = serializers.FloatField(read_only=True)
    categories = serializers.ListField(read_only=True)

    class Meta:
        model = JournalEntry
        fields = ['day', 'count', 'mood_avg', 'categories']
    
    def get_day(self, obj):
        """Retourne la date sans l'heure à partir de created_at."""
        return obj.created_at.date()

class JournalStatsSerializer(serializers.Serializer):
    """
    Serializer pour générer des statistiques sur les entrées de journal d'un utilisateur.
    """
    total_entries = serializers.SerializerMethodField()
    entries_per_category = serializers.SerializerMethodField()
    mood_distribution = serializers.SerializerMethodField()
    monthly_entries = serializers.SerializerMethodField()
    average_mood = serializers.SerializerMethodField()
    entries_streak = serializers.SerializerMethodField()
    
    def get_total_entries(self, user):
        """Retourne le nombre total d'entrées."""
        return user.entries.count()
    
    def get_entries_per_category(self, user):
        """Retourne la répartition des entrées par catégorie."""
        categories = user.entries.values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {cat['category']: cat['count'] for cat in categories}
    
    def get_mood_distribution(self, user):
        """Retourne la distribution des notes d'humeur."""
        moods = user.entries.values('mood').annotate(
            count=Count('id')
        ).order_by('mood')
        
        distribution = {str(i): 0 for i in range(1, 11)}
        for mood in moods:
            distribution[str(mood['mood'])] = mood['count']
        
        return distribution
    
    def get_monthly_entries(self, user):
        """Retourne la distribution des entrées par mois sur 1 an."""
        today = timezone.now().date()
        start_date = today - timedelta(days=365)
        
        entries = user.entries.filter(
            created_at__date__gte=start_date
        ).extra({'month': "to_char(created_at, 'YYYY-MM')"}).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        months = {}
        for i in range(12):
            month_date = today - timedelta(days=30 * i)
            month_key = month_date.strftime('%Y-%m')
            months[month_key] = 0
        
        for entry in entries:
            months[entry['month']] = entry['count']
        
        return months
    
    def get_average_mood(self, user):
        """Retourne l'humeur moyenne actuelle et son évolution."""
        result = {'overall': 0, 'last_week': 0, 'last_month': 0, 'trend': 'stable'}
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        two_months_ago = today - timedelta(days=60)
        
        overall = user.entries.aggregate(avg=Avg('mood'))
        last_week = user.entries.filter(created_at__date__gte=week_ago).aggregate(avg=Avg('mood'))
        last_month = user.entries.filter(created_at__date__gte=month_ago).aggregate(avg=Avg('mood'))
        previous_month = user.entries.filter(
            created_at__date__gte=two_months_ago,
            created_at__date__lt=month_ago
        ).aggregate(avg=Avg('mood'))
        
        result['overall'] = round(overall['avg'] or 0, 1)
        result['last_week'] = round(last_week['avg'] or 0, 1)
        result['last_month'] = round(last_month['avg'] or 0, 1)
        
        if previous_month['avg'] and last_month['avg']:
            diff = last_month['avg'] - previous_month['avg']
            if diff > 0.5:
                result['trend'] = 'up'
            elif diff < -0.5:
                result['trend'] = 'down'
        
        return result
    
    # ✅ Correction dans get_entries_streak
    def get_entries_streak(self, user):
        """Retourne la série actuelle et maximale de jours avec au moins une entrée."""
        today = timezone.now().date()
        dates_with_entries = user.entries.values('created_at__date').distinct().order_by('created_at__date')
        
        if not dates_with_entries:
            return {'current': 0, 'max': 0, 'dates': []}
        
        dates = [entry['created_at__date'] for entry in dates_with_entries]
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        current_active = dates[-1] in (today, today - timedelta(days=1))
        
        return {
            'current': current_streak if current_active else 0,
            'max': max_streak,
            'current_active': current_active,
            'last_entry_date': dates[-1].isoformat()
        }


class CategorySuggestionSerializer(serializers.Serializer):
    """
    Serializer pour retourner des suggestions de catégories.
    """
    categories = serializers.SerializerMethodField()
    
    def get_categories(self, user):
        """Retourne les catégories les plus utilisées par l'utilisateur."""
        return JournalEntry.get_category_suggestions(user)
