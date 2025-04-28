from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from ..models.badge_model import Badge, BadgeTemplate

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_link', 'icon_display', 'date_obtenue', 'level')
    list_filter = ('date_obtenue', 'level')
    search_fields = ('name', 'description', 'user__username')
    date_hierarchy = 'date_obtenue'
    raw_id_fields = ('user',)

    def user_link(self, obj):
        """Affiche un lien cliquable vers l'utilisateur."""
        if obj.user:
            url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = "Utilisateur"

    def icon_display(self, obj):
        """Affiche l'icône du badge."""
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    icon_display.short_description = "Icône"

@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition', 'icon_display', 'level', 'color_theme_display')
    search_fields = ('name', 'description', 'condition')

    def icon_display(self, obj):
        """Affiche l'icône du modèle de badge."""
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    icon_display.short_description = "Icône"

    def color_theme_display(self, obj):
        """Affiche une pastille de couleur pour le thème."""
        return format_html(
            '<div style="width:20px; height:20px; background:{}; border-radius:50%;"></div>',
            obj.color_theme
        )
    color_theme_display.short_description = "Thème"
