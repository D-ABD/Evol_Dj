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


# ===== 🎯 Gestion des défis =====
class ChallengeProgressInline(admin.TabularInline):
    model = ChallengeProgress
    extra = 0
    readonly_fields = ('user', 'completed', 'completed_at')
    fields = ('user', 'completed', 'completed_at')
    can_delete = False
    max_num = 20
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'target_entries', 'is_active_now', 'days_left', 'participants_count')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    inlines = [ChallengeProgressInline]
    
    def is_active_now(self, obj):
        """Vérifie si le défi est actuellement actif"""
        return obj.is_active()
    is_active_now.boolean = True
    is_active_now.short_description = "Actif"
    
    def days_left(self, obj):
        """Jours restants avant la fin du défi"""
        days = obj.days_remaining()
        if days <= 0:
            return "Terminé"
        return f"{days} jour{'s' if days > 1 else ''}"
    days_left.short_description = "Jours restants"
    
    def participants_count(self, obj):
        """Nombre d'utilisateurs participant au défi"""
        return obj.progresses.count()
    participants_count.short_description = "Participants"


@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge_link', 'completed', 'completed_at', 'progress_percent')
    list_filter = ('completed', 'completed_at', 'challenge')
    search_fields = ('user__username', 'user__email', 'challenge__title')
    date_hierarchy = 'completed_at'
    raw_id_fields = ('user', 'challenge')
    
    def challenge_link(self, obj):
        """Affiche un lien vers l'admin du défi"""
        url = reverse("admin:core_challenge_change", args=[obj.challenge.id])
        return format_html('<a href="{}">{}</a>', url, obj.challenge.title)
    challenge_link.short_description = "Défi"
    
    def progress_percent(self, obj):
        """Affiche le pourcentage de progression"""
        progress = obj.get_progress()
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px;">'
            '<div style="width: {}%; background-color: #4CAF50; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            progress['percent'], progress['percent'])
    progress_percent.short_description = "Progression"


