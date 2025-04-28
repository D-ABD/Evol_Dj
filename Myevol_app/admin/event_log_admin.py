from django.contrib import admin
from django.utils.html import format_html

from ..models.event_log_model import EventLog

@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_display', 'action', 'severity_display', 'metadata_preview')
    list_filter = ('severity', 'created_at')
    search_fields = ('action', 'description', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def user_display(self, obj):
        """Affiche l'utilisateur ou 'Système'."""
        if obj.user:
            return obj.user.username
        return format_html('<i>Système</i>')
    user_display.short_description = "Utilisateur"

    def severity_display(self, obj):
        """Couleur selon la gravité."""
        color = {
            'INFO': 'blue',
            'WARN': 'orange',
            'ERROR': 'red',
            'CRITICAL': 'darkred'
        }.get(obj.severity, 'black')
        return format_html('<strong style="color:{};">{}</strong>', color, obj.get_severity_display())
    severity_display.short_description = "Gravité"

    def metadata_preview(self, obj):
        """Montre rapidement s'il y a des métadonnées."""
        if obj.metadata:
            return format_html('<span style="color:green;">✔ Oui</span>')
        return format_html('<span style="color:gray;">✖ Non</span>')
    metadata_preview.short_description = "Métadonnées"
