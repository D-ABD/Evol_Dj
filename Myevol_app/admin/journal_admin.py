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


# ===== 📝 Gestion du journal =====
class JournalMediaInline(admin.TabularInline):
    model = JournalMedia
    extra = 0
    fields = ('file', 'type', 'created_at', 'preview')
    readonly_fields = ('created_at', 'preview')
    
    def preview(self, obj):
        """Affiche un aperçu du média"""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 300px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'display_date', 'mood_with_emoji', 'category', 'content_preview')
    list_filter = ('mood', 'category', 'created_at')
    search_fields = ('content', 'user__username', 'user__email', 'category')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    inlines = [JournalMediaInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def display_date(self, obj):
        """Affiche la date de création formatée"""
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    display_date.short_description = "Date"
    
    def mood_with_emoji(self, obj):
        """Affiche l'humeur avec son emoji correspondant"""
        return format_html('{} <span style="font-size: 1.2em;">{}</span>', 
                           obj.mood, obj.get_mood_emoji())
    mood_with_emoji.short_description = "Humeur"
    
    def content_preview(self, obj):
        """Affiche un aperçu du contenu"""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = "Contenu"


@admin.register(JournalMedia)
class JournalMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry_link', 'type', 'file_size_display', 'created_at', 'preview')
    list_filter = ('type', 'created_at')
    search_fields = ('entry__content', 'entry__user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'preview')
    
    def entry_link(self, obj):
        """Affiche un lien vers l'admin de l'entrée"""
        url = reverse("admin:core_journalentry_change", args=[obj.entry.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.entry))
    entry_link.short_description = "Entrée"
    
    def file_size_display(self, obj):
        """Affiche la taille du fichier en format lisible"""
        size = obj.file_size()
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    file_size_display.short_description = "Taille"
    
    def preview(self, obj):
        """Affiche un aperçu du média"""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 400px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"

