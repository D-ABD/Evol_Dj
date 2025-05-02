from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from ..models.badge_model import Badge, BadgeTemplate

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_link', 'icon_display', 'date_obtenue', 'level', 'was_earned_today_display')
    list_filter = ('date_obtenue', 'level')
    search_fields = ('name', 'description', 'user__username')
    date_hierarchy = 'date_obtenue'
    raw_id_fields = ('user',)
    
    readonly_fields = ('date_obtenue',)
    
    fieldsets = (
        (None, {'fields': ('name', 'description', 'icon', 'user', 'level')}),
        ('Informations temporelles', {'fields': ('date_obtenue',)}),
    )

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
    
    def was_earned_today_display(self, obj):
        """Indique si le badge a été obtenu aujourd'hui."""
        return obj.was_earned_today()
    was_earned_today_display.short_description = "Aujourd'hui"
    was_earned_today_display.boolean = True

@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition', 'icon_display', 'level', 'color_theme_display')
    search_fields = ('name', 'description', 'condition')
    list_filter = ('level',)
    
    fieldsets = (
        (None, {'fields': ('name', 'description', 'icon', 'condition', 'level')}),
        ('Apparence', {'fields': ('color_theme', 'animation_url')}),
    )

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