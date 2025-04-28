from django.contrib import admin
from django.utils.html import format_html

from ..models.objective_model import Objective

@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'progress_display', 'status_display', 'target_date')
    list_filter = ('category', 'done')
    search_fields = ('title', 'category', 'user__username')
    date_hierarchy = 'target_date'
    ordering = ('target_date',)

    def progress_display(self, obj):
        """Affiche une barre de progression."""
        percent = obj.progress_percent
        color = "green" if percent == 100 else "blue"
        return format_html(
            '<div style="width:100px; background:#f0f0f0;"><div style="width:{}%; background:{}; color:white;">{}%</div></div>',
            percent, color, percent
        )
    progress_display.short_description = "Progression"

    def status_display(self, obj):
        """Affiche si l'objectif est terminé, en retard ou en cours."""
        if obj.done:
            return format_html('<span style="color:green;">✔ Terminé</span>')
        if obj.is_overdue():
            return format_html('<span style="color:red;">⚠ En retard</span>')
        return format_html('<span style="color:orange;">⏳ En cours</span>')
    status_display.short_description = "Statut"
