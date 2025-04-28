from django.contrib import admin
from django.utils.html import format_html

from ..models.notification_model import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'notif_type_display', 'is_read_display', 'archived_display', 'created_at')
    list_filter = ('notif_type', 'is_read', 'archived')
    search_fields = ('message', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def message_preview(self, obj):
        """Affiche un extrait du message."""
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = "Message"

    def notif_type_display(self, obj):
        """Affiche le type de notification joliment."""
        color = {
            'badge': 'green',
            'objectif': 'blue',
            'statistique': 'purple',
            'info': 'gray'
        }.get(obj.notif_type, 'black')
        return format_html('<strong style="color:{};">{}</strong>', color, obj.type_display)
    notif_type_display.short_description = "Type"

    def is_read_display(self, obj):
        """Affiche lu/non lu avec des couleurs."""
        if obj.is_read:
            return format_html('<span style="color:green;">✔ Lu</span>')
        return format_html('<span style="color:red;">✖ Non lu</span>')
    is_read_display.short_description = "Lu ?"

    def archived_display(self, obj):
        """Affiche archivé/non archivé avec des couleurs."""
        if obj.archived:
            return format_html('<span style="color:gray;">🗄️ Archivé</span>')
        return format_html('<span style="color:blue;">📬 Actif</span>')
    archived_display.short_description = "Archivé ?"
