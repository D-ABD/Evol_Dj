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


# ===== 🏅 Gestion des badges =====
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_link', 'icon_display', 'date_obtenue', 'level', 'is_new')
    list_filter = ('name', 'date_obtenue', 'level')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    date_hierarchy = 'date_obtenue'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur personnalisé"""
        if obj.user:
            url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"

    
    def icon_display(self, obj):
        """Affiche l'icône du badge"""
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    icon_display.short_description = "Icône"
    
    def is_new(self, obj):
        """Indique si le badge a été obtenu aujourd'hui"""
        return obj.was_earned_today()
    is_new.boolean = True
    is_new.short_description = "Nouveau"


@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_display', 'level', 'condition', 'badges_count')
    list_filter = ('level',)
    search_fields = ('name', 'description', 'condition')
    
    def icon_display(self, obj):
        """Affiche l'icône du template de badge"""
        return format_html('<span style="font-size: 1.5em; color: {};">{}</span>', 
                           obj.color_theme, obj.icon)
    icon_display.short_description = "Icône"
    
    def badges_count(self, obj):
        """Nombre de badges attribués de ce type"""
        return Badge.objects.filter(name=obj.name).count()
    badges_count.short_description = "Badges attribués"
