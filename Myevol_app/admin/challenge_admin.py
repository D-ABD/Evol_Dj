from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import now

from ..models.challenge_model import Challenge, ChallengeProgress

class ChallengeProgressInline(admin.TabularInline):
    model = ChallengeProgress
    extra = 0
    readonly_fields = ('user', 'completed', 'completed_at', 'progress_display')
    can_delete = False
    
    def progress_display(self, obj):
        """Affiche la progression de l'utilisateur en pourcentage."""
        progress = obj.get_progress()
        percent = progress['percent']
        color = "green" if percent >= 100 else "orange" if percent >= 50 else "red"
        return format_html(
            '<div style="width:100px; background:#eee;"><div style="width:{}px; background:{}; height:10px;"></div></div> {}%',
            percent, color, percent
        )
    progress_display.short_description = "Progression"

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'days_remaining_display', 'is_active_display', 'participants_display', 'target_entries')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')
    inlines = [ChallengeProgressInline]
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'target_entries')}),
        ('Période', {'fields': ('start_date', 'end_date')}),
    )

    def is_active_display(self, obj):
        """Affiche l'état actif/inactif du défi avec couleur."""
        color = "green" if obj.is_active else "red"
        status = "Actif" if obj.is_active else "Inactif"
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', color, status)
    is_active_display.short_description = "Statut"
    is_active_display.boolean = False

    def participants_display(self, obj):
        """Affiche le nombre de participants."""
        count = obj.participants_count
        url = reverse("admin:Myevol_app_challengeprogress_changelist") + f"?challenge__id__exact={obj.id}"
        return format_html('<a href="{}">{} participant(s)</a>', url, count)
    participants_display.short_description = "Participants"
    
    def days_remaining_display(self, obj):
        """Affiche le nombre de jours restants avec couleur."""
        days = obj.days_remaining
        if not obj.is_active:
            if now().date() < obj.start_date:
                return format_html('<span style="color:blue;">Commence dans {} jour(s)</span>', (obj.start_date - now().date()).days)
            return format_html('<span style="color:gray;">Terminé</span>')
        
        color = "green" if days > 7 else "orange" if days > 3 else "red"
        return format_html('<span style="color:{};">{} jour(s)</span>', color, days)
    days_remaining_display.short_description = "Reste"

@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'challenge_link', 'progress_bar', 'completed', 'completed_at')
    list_filter = ('completed', 'challenge')
    search_fields = ('user__username', 'challenge__title')
    raw_id_fields = ('user', 'challenge')
    readonly_fields = ('completed_at', 'progress_detail')
    
    fieldsets = (
        (None, {'fields': ('user', 'challenge')}),
        ('État', {'fields': ('completed', 'completed_at', 'progress_detail')}),
    )

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
    
    def progress_bar(self, obj):
        """Affiche la progression sous forme de barre colorée."""
        progress = obj.get_progress()
        percent = progress['percent']
        color = "green" if percent >= 100 else "orange" if percent >= 50 else "red"
        return format_html(
            '<div style="width:100px; background:#eee;"><div style="width:{}px; background:{}; height:10px;"></div></div> {}%',
            percent, color, percent
        )
    progress_bar.short_description = "Progression"
    
    def progress_detail(self, obj):
        """Affiche les détails de la progression."""
        progress = obj.get_progress()
        return format_html(
            '{} / {} entrées ({}%)',
            progress['current'], 
            progress['target'],
            progress['percent']
        )
    progress_detail.short_description = "Détails de progression"