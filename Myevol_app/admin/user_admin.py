from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from ..models.user_model import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'level_display', 'xp', 'longest_streak', 'current_streak_display', 'total_entries_display', 'date_joined', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Infos personnelles', {'fields': ('first_name', 'last_name', 'avatar_url')}),
        ('Statistiques', {'fields': ('xp',)}),  # Retiré longest_streak car non-editable
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('longest_streak',)  # Ajouter longest_streak comme champ en lecture seule

    def level_display(self, obj):
        """Affiche le niveau calculé de l'utilisateur."""
        level = obj.level()
        progress = obj.level_progress()
        return format_html('{} <small>({}%)</small>', level, progress)
    level_display.short_description = "Niveau"
    
    def current_streak_display(self, obj):
        """Affiche la série actuelle d'entrées consécutives."""
        return obj.current_streak()
    current_streak_display.short_description = "Série actuelle"
    
    def total_entries_display(self, obj):
        """Affiche le nombre total d'entrées de journal."""
        return obj.total_entries
    total_entries_display.short_description = "Entrées"