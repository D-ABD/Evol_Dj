from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
import json

from ..models.event_log_model import EventLog

@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_display', 'action', 'severity_display', 'metadata_preview', 'description_short')
    list_filter = ('severity', 'action', 'created_at')
    search_fields = ('action', 'description', 'user__username', 'metadata')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'formatted_metadata', 'time_since')
    
    fieldsets = (
        (None, {
            'fields': ('action', 'severity', 'user', 'created_at', 'time_since')
        }),
        ('Détails', {
            'fields': ('description',)
        }),
        ('Métadonnées', {
            'fields': ('metadata', 'formatted_metadata'),
            'classes': ('collapse',)
        })
    )

    def user_display(self, obj):
        """Affiche l'utilisateur ou 'Système' avec lien si disponible."""
        if obj.user:
            url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return format_html('<i>Système</i>')
    user_display.short_description = "Utilisateur"

    def severity_display(self, obj):
        """Couleur selon la gravité."""
        colors = {
            'INFO': '#007bff',
            'WARN': '#ffc107',
            'ERROR': '#dc3545',
            'CRITICAL': '#721c24'
        }
        background = {
            'INFO': '#e6f2ff',
            'WARN': '#fff3cd',
            'ERROR': '#f8d7da',
            'CRITICAL': '#f5c6cb'
        }
        color = colors.get(obj.severity, 'black')
        bg = background.get(obj.severity, 'white')
        return format_html(
            '<span style="padding: 3px 6px; border-radius: 3px; background-color: {}; color: {};">{}</span>',
            bg, color, obj.get_severity_display()
        )
    severity_display.short_description = "Gravité"

    def metadata_preview(self, obj):
        """Montre rapidement s'il y a des métadonnées."""
        if not obj.metadata:
            return format_html('<span style="color:gray;">✖ Non</span>')
        keys = list(obj.metadata.keys()) if obj.metadata else []
        return format_html('<span style="color:green;">✔ {}</span>', ', '.join(keys)[:30])
    metadata_preview.short_description = "Métadonnées"
    
    def description_short(self, obj):
        """Affiche une version courte de la description."""
        if not obj.description:
            return "-"
        max_length = 50
        if len(obj.description) > max_length:
            return obj.description[:max_length] + "..."
        return obj.description
    description_short.short_description = "Description"
    
    def formatted_metadata(self, obj):
        """Affiche les métadonnées formatées JSON pour une meilleure lisibilité."""
        if not obj.metadata:
            return "-"
        pretty_json = json.dumps(obj.metadata, indent=2)
        return format_html('<pre style="background-color: #f6f8fa; padding: 10px; border-radius: 5px;">{}</pre>', pretty_json)
    formatted_metadata.short_description = "Métadonnées (formatées)"
    
    def time_since(self, obj):
        """Affiche le temps écoulé depuis l'événement."""
        from django.utils.timezone import now
        from django.utils.timesince import timesince
        return f"{timesince(obj.created_at)} ago"
    time_since.short_description = "Temps écoulé"
    
    def has_add_permission(self, request):
        """Désactive l'ajout manuel d'événements via l'admin."""
        return False