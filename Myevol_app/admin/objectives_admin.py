from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta

from ..models.objective_model import Objective

@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_link', 'category', 'progress_display', 'status_display', 'target_date', 'days_remaining_display')
    list_filter = ('category', 'done', 'target_date')
    search_fields = ('title', 'category', 'user__username', 'user__email')
    date_hierarchy = 'target_date'
    ordering = ('target_date',)
    actions = ['mark_as_done', 'mark_as_undone']
    
    readonly_fields = ('created_at', 'entries_count', 'progress_bar', 'days_remaining_display')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'category')
        }),
        ('Objectif', {
            'fields': ('target_value', 'entries_count', 'progress_bar', 'done')
        }),
        ('Planification', {
            'fields': ('target_date', 'days_remaining_display', 'created_at')
        }),
    )

    def user_link(self, obj):
        """Affiche un lien vers l'utilisateur."""
        url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"

    def progress_display(self, obj):
        """Affiche une barre de progression avec code couleur basé sur le pourcentage."""
        percent = obj.progress_percent
        
        # Couleurs variant selon le pourcentage
        if percent >= 100:
            color = "#28a745"  # Vert
        elif percent >= 75:
            color = "#17a2b8"  # Bleu-vert
        elif percent >= 50:
            color = "#007bff"  # Bleu
        elif percent >= 25:
            color = "#fd7e14"  # Orange
        else:
            color = "#dc3545"  # Rouge
            
        # Style amélioré pour la barre de progression
        return format_html(
            '<div style="width:100px; background:#f0f0f0; border-radius:5px; overflow:hidden;">'
            '<div style="width:{}%; background:{}; color:white; padding:2px 5px; text-align:center; white-space:nowrap;">'
            '{} / {}'
            '</div>'
            '</div>',
            percent, color, obj.entries_done(), obj.target_value
        )
    progress_display.short_description = "Progression"

    def progress_bar(self, obj):
        """Version plus grande de la barre de progression pour la page de détail."""
        percent = obj.progress_percent
        
        if percent >= 100:
            color = "#28a745"  # Vert
        elif percent >= 75:
            color = "#17a2b8"  # Bleu-vert
        elif percent >= 50:
            color = "#007bff"  # Bleu
        elif percent >= 25:
            color = "#fd7e14"  # Orange
        else:
            color = "#dc3545"  # Rouge
            
        return format_html(
            '<div style="width:100%; max-width:300px; background:#f0f0f0; border-radius:5px; overflow:hidden; height:25px; margin:10px 0;">'
            '<div style="width:{}%; background:{}; height:100%; color:white; display:flex; align-items:center; justify-content:center;">'
            '{}%'
            '</div>'
            '</div>'
            '<p>{} sur {} entrées requises dans la catégorie "{}"</p>',
            percent, color, percent, obj.entries_done(), obj.target_value, obj.category
        )
    progress_bar.short_description = "Barre de progression"

    def status_display(self, obj):
        """Affiche si l'objectif est terminé, en retard ou en cours."""
        if obj.done:
            return format_html('<span style="background:#d4edda; color:#155724; padding:3px 8px; border-radius:3px;">✔ Terminé</span>')
        if obj.is_overdue():
            days = abs(obj.days_remaining())
            return format_html(
                '<span style="background:#f8d7da; color:#721c24; padding:3px 8px; border-radius:3px;">⚠ En retard de {} jour{}</span>',
                days, 's' if days > 1 else ''
            )
        if obj.is_due_today():
            return format_html('<span style="background:#fff3cd; color:#856404; padding:3px 8px; border-radius:3px;">⏰ Aujourd\'hui</span>')
        return format_html('<span style="background:#cce5ff; color:#004085; padding:3px 8px; border-radius:3px;">⏳ En cours</span>')
    status_display.short_description = "Statut"
    
    def days_remaining_display(self, obj):
        """Affiche le nombre de jours restants avant la date cible."""
        days = obj.days_remaining()
        if obj.done:
            return format_html('<span style="color:#28a745;">Objectif complété</span>')
        if days < 0:
            return format_html('<span style="color:#dc3545;">En retard de {} jour{}</span>', abs(days), 's' if abs(days) > 1 else '')
        if days == 0:
            return format_html('<span style="color:#fd7e14; font-weight:bold;">Aujourd\'hui</span>')
        if days == 1:
            return format_html('<span style="color:#fd7e14;">Demain</span>')
        if days <= 7:
            return format_html('<span style="color:#007bff;">{} jours</span>', days)
        return f"{days} jours"
    days_remaining_display.short_description = "Temps restant"
    
    def entries_count(self, obj):
        """Affiche le nombre d'entrées dans la catégorie pour la date cible."""
        entries = obj.entries_done()
        if entries == 0:
            return "Aucune entrée"
        return f"{entries} entrée{'s' if entries > 1 else ''}"
    entries_count.short_description = "Entrées effectuées"
    
    def mark_as_done(self, request, queryset):
        """Action pour marquer les objectifs sélectionnés comme terminés."""
        updated = queryset.update(done=True)
        self.message_user(request, f"{updated} objectif{'s' if updated > 1 else ''} marqué{'s' if updated > 1 else ''} comme terminé{'s' if updated > 1 else ''}.")
    mark_as_done.short_description = "Marquer comme terminé"
    
    def mark_as_undone(self, request, queryset):
        """Action pour marquer les objectifs sélectionnés comme non terminés."""
        updated = queryset.update(done=False)
        self.message_user(request, f"{updated} objectif{'s' if updated > 1 else ''} marqué{'s' if updated > 1 else ''} comme non terminé{'s' if updated > 1 else ''}.")
    mark_as_undone.short_description = "Marquer comme non terminé"
    
    def get_queryset(self, request):
        """Optimisation des requêtes."""
        return super().get_queryset(request).select_related('user')