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


# ===== 📜 Gestion des citations =====
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_preview', 'author', 'mood_tag', 'length_display')
    list_filter = ('mood_tag', 'author')
    search_fields = ('text', 'author')
    
    def quote_preview(self, obj):
        """Affiche un aperçu de la citation"""
        if len(obj.text) > 70:
            return f'"{obj.text[:70]}..."'
        return f'"{obj.text}"'
    quote_preview.short_description = "Citation"
    
    def length_display(self, obj):
        """Affiche la longueur de la citation avec une indication visuelle"""
        length = obj.length()
        if length < 50:
            category = "Courte"
            color = "#8BC34A"
        elif length < 120:
            category = "Moyenne"
            color = "#FFC107"
        else:
            category = "Longue"
            color = "#FF9800"
        
        return format_html('<span style="color: {};">{} ({} caractères)</span>', 
                          color, category, length)
    length_display.short_description = "Longueur"


