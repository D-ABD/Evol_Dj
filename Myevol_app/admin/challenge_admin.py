from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from ..models.challenge_model import Challenge, ChallengeProgress

class ChallengeProgressInline(admin.TabularInline):
    model = ChallengeProgress
    extra = 0
    readonly_fields = ('user', 'completed', 'completed_at')
    can_delete = False

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active_display', 'participants_display', 'target_entries')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title',)
    inlines = [ChallengeProgressInline]
    date_hierarchy = 'start_date'

    def is_active_display(self, obj):
        """Affiche l'état actif/inactif du défi avec couleur."""
        color = "green" if obj.is_active else "red"
        status = "Actif" if obj.is_active else "Inactif"
        return format_html('<span style="color:{};">{}</span>', color, status)
    is_active_display.short_description = "Actif ?"

    def participants_display(self, obj):
        """Affiche le nombre de participants."""
        return obj.participants_count
    participants_display.short_description = "Participants"

@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'challenge_link', 'completed', 'completed_at')
    list_filter = ('completed',)
    search_fields = ('user__username', 'challenge__title')
    raw_id_fields = ('user', 'challenge')

    def user_link(self, obj):
        """Lien direct vers l'utilisateur."""
        url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"

    def challenge_link(self, obj):
        """Lien direct vers le défi."""
        url = reverse("admin:Myevol_app_challenge_change", args=[obj.challenge.id])
        return format_html('<a href="{}">{}</a>', url, obj.challenge.title)
    challenge_link.short_description = "Défi"
