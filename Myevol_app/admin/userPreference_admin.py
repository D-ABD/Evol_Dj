from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from ..models.userPreference_model import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'dark_mode_display', 'accent_color_display', 'font_choice_display', 'animations_enabled', 'notif_status_display')
    list_filter = ('dark_mode', 'enable_animations', 'notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique')
    search_fields = ('user__username', 'user__email', 'font_choice')
    ordering = ('user__username',)
    actions = ['enable_all_notifications', 'disable_all_notifications', 'reset_to_defaults']
    
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Apparence', {
            'fields': ('dark_mode', 'accent_color_preview', 'accent_color', 'font_choice', 'enable_animations'),
            'description': 'Paramètres d\'apparence et d\'interface utilisateur'
        }),
        ('Notifications', {
            'fields': ('notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique'),
            'description': 'Configuration des préférences de notification'
        }),
    )
    
    readonly_fields = ('accent_color_preview',)

    def user_link(self, obj):
        """Lien cliquable vers l'utilisateur."""
        url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    user_link.admin_order_field = 'user__username'

    def dark_mode_display(self, obj):
        """Affiche si dark mode activé ou non avec style."""
        if obj.dark_mode:
            return format_html(
                '<span style="background:#343a40; color:white; padding:3px 8px; border-radius:4px;">'
                '<span style="margin-right:5px;">🌑</span> Activé</span>'
            )
        else:
            return format_html(
                '<span style="background:#f8f9fa; color:#212529; padding:3px 8px; border-radius:4px;">'
                '<span style="margin-right:5px;">☀️</span> Désactivé</span>'
            )
    dark_mode_display.short_description = "Mode Sombre"
    dark_mode_display.boolean = True

    def accent_color_display(self, obj):
        """Affiche la couleur d'accent avec son code hex."""
        return format_html(
            '<div style="display:flex; align-items:center;">'
            '<div style="width:20px; height:20px; background:{}; border-radius:50%; border:1px solid #ddd; margin-right:8px;"></div>'
            '<code>{}</code>'
            '</div>',
            obj.accent_color, obj.accent_color
        )
    accent_color_display.short_description = "Couleur Accent"
    
    def accent_color_preview(self, obj):
        """Aperçu plus grand de la couleur d'accent avec exemples."""
        return format_html(
            '<div style="display:flex; flex-direction:column; gap:10px;">'
            '<div style="display:flex; align-items:center;">'
            '<div style="width:50px; height:50px; background:{}; border-radius:5px; margin-right:15px;"></div>'
            '<code style="font-size:16px;">{}</code>'
            '</div>'
            '<div style="display:flex; gap:10px;">'
            '<div style="padding:8px 15px; background:{}; color:white; border-radius:5px;">Bouton</div>'
            '<div style="padding:8px 15px; border:2px solid {}; color:{}; border-radius:5px;">Contour</div>'
            '<div style="padding:8px 15px; background:#f8f9fa; color:{}; border-radius:5px;">Texte</div>'
            '</div>'
            '</div>',
            obj.accent_color, obj.accent_color, 
            obj.accent_color, obj.accent_color, obj.accent_color, obj.accent_color
        )
    accent_color_preview.short_description = "Aperçu de la couleur"

    def font_choice_display(self, obj):
        """Affiche la police avec un exemple du rendu."""
        return format_html(
            '<span style="font-family:\'{}\', sans-serif; font-size:14px;">Exemple de texte avec {}</span>',
            obj.font_choice, obj.font_choice
        )
    font_choice_display.short_description = "Police"

    def animations_enabled(self, obj):
        """Affiche si les animations sont activées avec style."""
        if obj.enable_animations:
            return format_html('<span style="color:#28a745;">✓ Activées</span>')
        return format_html('<span style="color:#dc3545;">✗ Désactivées</span>')
    animations_enabled.short_description = "Animations"
    animations_enabled.boolean = True

    def notif_status_display(self, obj):
        """Affiche l'état des notifications avec compteur et icônes."""
        active = sum([
            obj.notif_badge,
            obj.notif_objectif, 
            obj.notif_info, 
            obj.notif_statistique
        ])
        total = 4
        status = f"{active}/{total}"
        
        if active == 0:
            color = "#dc3545"  # Rouge
            icon = "🔕"
        elif active < total:
            color = "#fd7e14"  # Orange
            icon = "🔔"
        else:
            color = "#28a745"  # Vert
            icon = "🔔"
            
        details = []
        if obj.notif_badge:
            details.append("🏆 Badge")
        if obj.notif_objectif:
            details.append("🎯 Objectif")
        if obj.notif_info:
            details.append("ℹ️ Info")
        if obj.notif_statistique:
            details.append("📊 Stat")
            
        details_str = ", ".join(details) if details else "Aucune notification active"
        
        return format_html(
            '<div>'
            '<span style="color:{}; margin-right:5px;">{} {}</span>'
            '<div style="font-size:12px; color:#6c757d; margin-top:3px;">{}</div>'
            '</div>',
            color, icon, status, details_str
        )
    notif_status_display.short_description = "Notifications"
    
    def enable_all_notifications(self, request, queryset):
        """Action pour activer toutes les notifications."""
        updated = queryset.update(
            notif_badge=True,
            notif_objectif=True,
            notif_info=True,
            notif_statistique=True
        )
        self.message_user(request, f"{updated} préférence(s) mise(s) à jour - Toutes les notifications activées.")
    enable_all_notifications.short_description = "Activer toutes les notifications"
    
    def disable_all_notifications(self, request, queryset):
        """Action pour désactiver toutes les notifications."""
        updated = queryset.update(
            notif_badge=False,
            notif_objectif=False,
            notif_info=False,
            notif_statistique=False
        )
        self.message_user(request, f"{updated} préférence(s) mise(s) à jour - Toutes les notifications désactivées.")
    disable_all_notifications.short_description = "Désactiver toutes les notifications"
    
    def reset_to_defaults(self, request, queryset):
        """Action pour réinitialiser aux valeurs par défaut."""
        count = 0
        for pref in queryset:
            pref.reset_to_defaults()
            count += 1
        self.message_user(request, f"{count} préférence(s) réinitialisée(s) aux valeurs par défaut.")
    reset_to_defaults.short_description = "Réinitialiser aux valeurs par défaut"