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


# ===== 🎯 Gestion des objectifs =====
@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_link', 'category', 'target_date', 'done_status', 'progress_display')
    list_filter = ('done', 'category', 'target_date')
    search_fields = ('title', 'user__username', 'user__email', 'category')
    date_hierarchy = 'target_date'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def done_status(self, obj):
        """Affiche l'état de complétion de l'objectif"""
        if obj.done:
            return format_html('<span style="color: green;">✓ Terminé</span>')
        elif obj.is_overdue():
            return format_html('<span style="color: red;">⚠ En retard</span>')
        else:
            return format_html('<span style="color: orange;">⏳ En cours</span>')
    done_status.short_description = "État"
    
    def progress_display(self, obj):
        """Affiche la progression de l'objectif sous forme de barre"""
        progress = obj.progress()
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px;">'
            '<div style="width: {}%; background-color: {}; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            progress, '#4CAF50' if progress == 100 else '#2196F3', progress)
    progress_display.short_description = "Progression"


