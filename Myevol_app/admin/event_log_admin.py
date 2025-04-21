from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 📝 Gestion des logs d'événements =====
@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_link', 'action', 'description_preview', 'has_metadata')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'user__email', 'action', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'user', 'action', 'description', 'metadata_formatted')
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        if obj.user:
            url = reverse("admin:auth_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = "Utilisateur"
    
    def description_preview(self, obj):
        """Affiche un aperçu de la description"""
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description
    description_preview.short_description = "Description"
    
    def has_metadata(self, obj):
        """Indique si le log contient des métadonnées"""
        return obj.metadata is not None and bool(obj.metadata)
    has_metadata.boolean = True
    has_metadata.short_description = "Métadonnées"
    
    def metadata_formatted(self, obj):
        """Affiche les métadonnées formatées en JSON"""
        if not obj.metadata:
            return "-"
        import json
        return format_html('<pre>{}</pre>', json.dumps(obj.metadata, indent=2))
    metadata_formatted.short_description = "Métadonnées"



