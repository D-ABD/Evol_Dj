from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import now

from ..models.notification_model import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'message_preview', 'notif_type_display', 'is_read_display', 'archived_display', 'created_at', 'scheduled_status')
    list_filter = ('notif_type', 'is_read', 'archived', 'created_at')
    search_fields = ('message', 'user__username', 'user__email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'mark_as_unread', 'archive_notifications', 'unarchive_notifications']
    
    readonly_fields = ('created_at', 'read_at', 'time_since_created')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'notif_type')
        }),
        ('État', {
            'fields': ('is_read', 'read_at', 'archived')
        }),
        ('Planification', {
            'fields': ('scheduled_at',)
        }),
        ('Informations temporelles', {
            'fields': ('created_at', 'time_since_created'),
            'classes': ('collapse',)
        }),
    )

    def user_link(self, obj):
        """Lien vers l'utilisateur concerné."""
        url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"

    def message_preview(self, obj):
        """Affiche un extrait du message."""
        max_length = 50
        if len(obj.message) > max_length:
            return format_html('{}...', obj.message[:max_length])
        return obj.message
    message_preview.short_description = "Message"

    def notif_type_display(self, obj):
        """Affiche le type de notification joliment."""
        colors = {
            'badge': '#28a745',      # Vert
            'objectif': '#007bff',   # Bleu
            'statistique': '#6f42c1', # Violet
            'info': '#6c757d'        # Gris
        }
        backgrounds = {
            'badge': '#d4edda',      # Vert clair
            'objectif': '#cce5ff',   # Bleu clair
            'statistique': '#e2d9f3', # Violet clair
            'info': '#e9ecef'        # Gris clair
        }
        
        color = colors.get(obj.notif_type, '#343a40')
        bg = backgrounds.get(obj.notif_type, '#f8f9fa')
        
        icon = {
            'badge': '🏆',
            'objectif': '🎯',
            'statistique': '📊',
            'info': 'ℹ️'
        }.get(obj.notif_type, '📫')
        
        return format_html(
            '<span style="padding: 3px 8px; border-radius: 3px; background-color: {}; color: {};">{} {}</span>',
            bg, color, icon, obj.type_display
        )
    notif_type_display.short_description = "Type"

    def is_read_display(self, obj):
        """Affiche lu/non lu avec des couleurs."""
        if obj.is_read:
            return format_html('<span style="color:#28a745;">✔ Lu</span>')
        return format_html('<span style="color:#dc3545; font-weight:bold;">✖ Non lu</span>')
    is_read_display.short_description = "Lu ?"
    is_read_display.admin_order_field = 'is_read'

    def archived_display(self, obj):
        """Affiche archivé/non archivé avec des couleurs."""
        if obj.archived:
            return format_html('<span style="color:#6c757d;">🗄️ Archivé</span>')
        return format_html('<span style="color:#007bff;">📬 Actif</span>')
    archived_display.short_description = "Archivé ?"
    archived_display.admin_order_field = 'archived'
    
    def scheduled_status(self, obj):
        """Affiche le statut de planification."""
        if not obj.scheduled_at:
            return format_html('<span style="color:#28a745;">Immédiate</span>')
        
        current_time = now()
        if obj.scheduled_at > current_time:
            return format_html(
                '<span style="color:#fd7e14;">Planifiée pour {}</span>',
                obj.scheduled_at.strftime('%d/%m/%Y %H:%M')
            )
        else:
            return format_html('<span style="color:#28a745;">Envoyée</span>')
    scheduled_status.short_description = "Planification"
    
    def time_since_created(self, obj):
        """Affiche le temps écoulé depuis la création."""
        from django.utils.timesince import timesince
        return f"{timesince(obj.created_at)} ago"
    time_since_created.short_description = "Âge"
    
    def mark_as_read(self, request, queryset):
        """Action pour marquer les notifications sélectionnées comme lues."""
        updated = 0
        for notification in queryset.filter(is_read=False):
            notification.mark_as_read()
            updated += 1
        self.message_user(request, f"{updated} notification(s) marquée(s) comme lue(s).")
    mark_as_read.short_description = "Marquer comme lu"
    
    def mark_as_unread(self, request, queryset):
        """Action pour marquer les notifications comme non lues."""
        count = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f"{count} notification(s) marquée(s) comme non lue(s).")
    mark_as_unread.short_description = "Marquer comme non lu"
    
    def archive_notifications(self, request, queryset):
        """Action pour archiver les notifications sélectionnées."""
        count = queryset.update(archived=True)
        self.message_user(request, f"{count} notification(s) archivée(s).")
    archive_notifications.short_description = "Archiver les notifications"
    
    def unarchive_notifications(self, request, queryset):
        """Action pour désarchiver les notifications sélectionnées."""
        count = queryset.update(archived=False)
        self.message_user(request, f"{count} notification(s) désarchivée(s).")
    unarchive_notifications.short_description = "Désarchiver les notifications"
    
    def get_queryset(self, request):
        """Exclut le champ temporaire de l'interface d'administration."""
        qs = super().get_queryset(request)
        return qs.filter(temporary_field=False)