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


# ===== 📊 Gestion des statistiques =====
@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = ('date', 'user_link', 'entries_count', 'mood_average_display', 'day_of_week_display', 'categories_preview')
    list_filter = ('date',)
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'date'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def mood_average_display(self, obj):
        """Affiche la moyenne d'humeur avec une couleur indicative"""
        if obj.mood_average is None:
            return "-"
        
        color = "#CCCCCC"  # Gris par défaut
        if obj.mood_average >= 8:
            color = "#4CAF50"  # Vert
        elif obj.mood_average >= 6:
            color = "#8BC34A"  # Vert clair
        elif obj.mood_average >= 4:
            color = "#FFC107"  # Ambre
        elif obj.mood_average >= 2:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Rouge
            
        return format_html('<span style="color: {}; font-weight: bold;">{:.1f}</span>', 
                           color, obj.mood_average)
    mood_average_display.short_description = "Humeur moyenne"
    
    def day_of_week_display(self, obj):
        """Affiche le jour de la semaine avec mise en évidence du weekend"""
        day = obj.day_of_week()
        is_weekend = obj.is_weekend()
        return format_html('<span style="{}font-weight: {};">{}</span>', 
                          'color: #E91E63; ' if is_weekend else '', 
                          'bold' if is_weekend else 'normal', 
                          day)
    day_of_week_display.short_description = "Jour"
    
    def categories_preview(self, obj):
        """Affiche un aperçu des catégories utilisées"""
        if not obj.categories:
            return "-"
        
        # Limiter à 3 catégories maximum pour l'affichage
        cats = list(obj.categories.items())
        if len(cats) <= 3:
            return ", ".join([f"{cat}: {count}" for cat, count in cats])
        else:
            preview = ", ".join([f"{cat}: {count}" for cat, count in cats[:3]])
            return f"{preview}, ... (+{len(cats)-3})"
    categories_preview.short_description = "Catégories"


@admin.register(WeeklyStat)
class WeeklyStatAdmin(admin.ModelAdmin):
    list_display = ('week_display', 'user_link', 'entries_count', 'mood_average_display', 'top_category_display')
    list_filter = ('week_start',)
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'week_start'
    raw_id_fields = ('user',)
    
    def week_display(self, obj):
        """Affiche la semaine de façon lisible"""
        return f"Semaine {obj.week_number()} ({obj.week_start.strftime('%d/%m')} - {obj.week_end().strftime('%d/%m/%Y')})"
    week_display.short_description = "Semaine"
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def mood_average_display(self, obj):
        """Affiche la moyenne d'humeur avec une couleur indicative"""
        if obj.mood_average is None:
            return "-"
        
        color = "#CCCCCC"  # Gris par défaut
        if obj.mood_average >= 8:
            color = "#4CAF50"  # Vert
        elif obj.mood_average >= 6:
            color = "#8BC34A"  # Vert clair
        elif obj.mood_average >= 4:
            color = "#FFC107"  # Ambre
        elif obj.mood_average >= 2:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Rouge
            
        return format_html('<span style="color: {}; font-weight: bold;">{:.1f}</span>', 
                           color, obj.mood_average)
    mood_average_display.short_description = "Humeur moyenne"
    
    def top_category_display(self, obj):
        """Affiche la catégorie la plus fréquente avec le compte"""
        top = obj.top_category()
        if not top:
            return "-"
        count = obj.categories.get(top, 0)
        return f"{top} ({count})"
    top_category_display.short_description = "Catégorie principale"


