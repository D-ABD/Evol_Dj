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




# ===== 👤 Gestion des utilisateurs et préférences =====
class UserPreferenceInline(admin.StackedInline):
    model = UserPreference
    can_delete = False
    fieldsets = (
        ('Notifications', {
            'fields': (('notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique'),)
        }),
        ('Apparence', {
            'fields': (('dark_mode', 'accent_color'), ('font_choice', 'enable_animations'))
        }),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'date_joined', 'level_display', 'entries_count', 'streak_display')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login', 'entries_count', 'current_streak', 'mood_avg', 'badges_count')
    inlines = [UserPreferenceInline]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'avatar_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Statistiques', {'fields': ('entries_count', 'current_streak', 'longest_streak', 'xp', 'mood_avg', 'badges_count')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    def full_name(self, obj):
        """Retourne le nom complet de l'utilisateur"""
        return obj.get_full_name() or "-"
    full_name.short_description = "Nom complet"
    
    def entries_count(self, obj):
        """Nombre total d'entrées de journal"""
        return obj.total_entries()
    entries_count.short_description = "Entrées"
    
    def current_streak(self, obj):
        """Série actuelle de jours consécutifs"""
        return obj.current_streak()
    current_streak.short_description = "Série actuelle"
    
    def mood_avg(self, obj):
        """Moyenne d'humeur sur les 7 derniers jours"""
        avg = obj.mood_average(7)
        if avg is None:
            return "-"
        return f"{avg:.1f}/10"
    mood_avg.short_description = "Humeur (7j)"
    
    def badges_count(self, obj):
        """Nombre de badges obtenus"""
        return obj.badges.count()
    badges_count.short_description = "Badges"
    
    def level_display(self, obj):
        """Affiche le niveau avec une barre visuelle"""
        level = obj.level
        from ..utils.levels import get_user_progress
        progress = get_user_progress(obj.total_entries())
        
        return format_html(
            '<div><strong>Niveau {}</strong></div>'
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px; margin-top: 2px;">'
            '<div style="width: {}%; background-color: #673AB7; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            level, progress["progress"], progress["progress"])
    level_display.short_description = "Niveau"
    
    def streak_display(self, obj):
        """Affiche les séries de jours consécutifs"""
        current = obj.current_streak()
        longest = obj.longest_streak
        
        if current == 0:
            return "Aucune série active"
        
        if current == longest:
            return format_html('<span style="color: #4CAF50; font-weight: bold;">{} jour(s) 🔥</span>', current)
        
        return format_html('Actuelle: <span style="color: #2196F3;">{}</span> | '
                          'Record: <span style="color: #4CAF50;">{}</span>', 
                          current, longest)
    streak_display.short_description = "Séries"


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'notifications_enabled', 'accent_color_display', 'font_choice')
    list_filter = ('dark_mode', 'notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique', 'font_choice')
    search_fields = ('user__username', 'user__email')
    actions = ['reset_to_defaults']
    
    def notifications_enabled(self, obj):
        """Affiche quelles notifications sont activées"""
        enabled = []
        if obj.notif_badge:
            enabled.append("Badge")
        if obj.notif_objectif:
            enabled.append("Objectif")
        if obj.notif_info:
            enabled.append("Info")
        if obj.notif_statistique:
            enabled.append("Statistique")
            
        if not enabled:
            return format_html('<span style="color: #F44336;">Aucune</span>')
        elif len(enabled) == 4:
            return format_html('<span style="color: #4CAF50;">Toutes</span>')
        else:
            return ", ".join(enabled)
    notifications_enabled.short_description = "Notifications"
    
    def accent_color_display(self, obj):
        """Affiche la couleur d'accent avec un échantillon visuel"""
        return format_html(
            '<div style="display: inline-block; width: 20px; height: 20px; background-color: {}; '
            'border-radius: 50%; vertical-align: middle; margin-right: 5px;"></div> {}',
            obj.accent_color, obj.accent_color)
    accent_color_display.short_description = "Couleur d'accent"
    
    def reset_to_defaults(self, request, queryset):
        """Action pour réinitialiser les préférences aux valeurs par défaut"""
        for pref in queryset:
            pref.reset_to_defaults()
        self.message_user(request, f"{queryset.count()} préférence(s) réinitialisée(s) avec succès.")
    reset_to_defaults.short_description = "Réinitialiser aux valeurs par défaut"


