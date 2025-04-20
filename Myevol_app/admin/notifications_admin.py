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


# ===== 🔔 Gestion des notifications =====
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'notif_type_display', 'message_preview', 'is_read', 'archived', 'created_at')
    list_filter = ('notif_type', 'is_read', 'archived', 'created_at')
    search_fields = ('message', 'user__username', 'user__email')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    actions = ['mark_as_read', 'mark_as_unread', 'archive_notifications']
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def notif_type_display(self, obj):
        """Affiche le type de notification avec une couleur distinctive"""
        colors = {
            'badge': '#9C27B0',
            'objectif': '#4CAF50',
            'statistique': '#2196F3',
            'info': '#607D8B'
        }
        return format_html('<span style="color: {};">{}</span>', 
                          colors.get(obj.notif_type, 'black'), obj.type_display)
    notif_type_display.short_description = "Type"
    
    def message_preview(self, obj):
        """Affiche un aperçu du message"""
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = "Message"
    
    def mark_as_read(self, request, queryset):
        """Action pour marquer les notifications comme lues"""
        updated = queryset.update(is_read=True, read_at=now())
        self.message_user(request, f"{updated} notification(s) marquée(s) comme lue(s).")
    mark_as_read.short_description = "Marquer comme lues"
    
    def mark_as_unread(self, request, queryset):
        """Action pour marquer les notifications comme non lues"""
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f"{updated} notification(s) marquée(s) comme non lue(s).")
    mark_as_unread.short_description = "Marquer comme non lues"
    
    def archive_notifications(self, request, queryset):
        """Action pour archiver les notifications"""
        updated = queryset.update(archived=True)
        self.message_user(request, f"{updated} notification(s) archivée(s).")
    archive_notifications.short_description = "Archiver les notifications"

