from django.contrib import admin
from django.utils.html import format_html

from ..models.userPreference_model import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'dark_mode_display', 'accent_color_display', 'animations_enabled', 'notif_settings_summary')
    list_filter = ('dark_mode', 'enable_animations')
    search_fields = ('user__username',)
    ordering = ('user',)

    def user_link(self, obj):
        """Lien cliquable vers l'utilisateur."""
        return obj.user.username
    user_link.short_description = "Utilisateur"

    def dark_mode_display(self, obj):
        """Affiche si dark mode activé ou non."""
        return format_html(
            '<span style="color:{};">{}</span>',
            'green' if obj.dark_mode else 'gray',
            '🌑 Activé' if obj.dark_mode else '☀️ Désactivé'
        )
    dark_mode_display.short_description = "Mode Sombre"

    def accent_color_display(self, obj):
        """Affiche la couleur d'accent."""
        return format_html(
            '<div style="width:20px; height:20px; background:{}; border-radius:50%;"></div>',
            obj.accent_color
        )
    accent_color_display.short_description = "Couleur Accent"

    def animations_enabled(self, obj):
        """Affiche si les animations sont activées."""
        return "Oui" if obj.enable_animations else "Non"
    animations_enabled.short_description = "Animations"

    def notif_settings_summary(self, obj):
        """Résumé rapide des notifications activées."""
        active_notifs = []
        if obj.notif_badge:
            active_notifs.append("Badge")
        if obj.notif_objectif:
            active_notifs.append("Objectif")
        if obj.notif_info:
            active_notifs.append("Info")
        if obj.notif_statistique:
            active_notifs.append("Statistique")
        return ", ".join(active_notifs) if active_notifs else "Aucune activée"
    notif_settings_summary.short_description = "Notifications Actives"
