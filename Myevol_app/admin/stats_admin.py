from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from ..models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat

class BaseStatAdmin(admin.ModelAdmin):
    """Classe de base pour les administrateurs de statistiques."""
    readonly_fields = ('categories_display',)
    
    def user_link(self, obj):
        """Lien vers l'utilisateur."""
        url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def mood_average_display(self, obj):
        """Affiche la moyenne d'humeur avec une représentation visuelle."""
        if obj.mood_average is None:
            return format_html('<span style="color:#6c757d;">- Pas de données -</span>')
        
        # Définition des couleurs selon la valeur
        if obj.mood_average <= 3:
            color = "#dc3545"  # Rouge
        elif obj.mood_average <= 6:
            color = "#fd7e14"  # Orange
        else:
            color = "#28a745"  # Vert
        
        # Calcul de la largeur de la barre (10 = 100%)
        width = int(obj.mood_average * 10)
        
        return format_html(
            '<div style="display:flex; align-items:center;">'
            '<div style="width:100px; background:#f0f0f0; border-radius:5px; margin-right:10px;">'
            '<div style="width:{}px; height:12px; background:{}; border-radius:5px;"></div>'
            '</div>'
            '<span style="color:{}; font-weight:bold;">{:.1f}/10</span>'
            '</div>',
            width, color, color, obj.mood_average
        )
    mood_average_display.short_description = "Humeur moyenne"
    
    def categories_display(self, obj):
        """Affiche les catégories sous forme de tableau."""
        if not obj.categories:
            return format_html('<span style="color:#6c757d;">Aucune catégorie</span>')
        
        # Tri des catégories par nombre d'entrées (décroissant)
        sorted_categories = sorted(obj.categories.items(), key=lambda x: x[1], reverse=True)
        
        # Calcul du total pour les pourcentages
        total = sum(obj.categories.values())
        
        rows = []
        for category, count in sorted_categories:
            percentage = (count / total) * 100 if total > 0 else 0
            # Couleur aléatoire mais cohérente
            color = '#{:06x}'.format(hash(category) % 0xffffff)
            
            rows.append(
                f'<tr>'
                f'<td style="padding-right:15px;">{category}</td>'
                f'<td style="text-align:right; padding-right:15px;">{count}</td>'
                f'<td style="width:150px;">'
                f'<div style="background:#f0f0f0; border-radius:3px;">'
                f'<div style="width:{percentage}%; height:10px; background:{color}; border-radius:3px;"></div>'
                f'</div>'
                f'</td>'
                f'<td style="text-align:right;">{percentage:.1f}%</td>'
                f'</tr>'
            )
        
        table = format_html(
            '<table style="border-collapse:collapse;">'
            '<thead>'
            '<tr>'
            '<th style="text-align:left; padding-right:15px;">Catégorie</th>'
            '<th style="text-align:right; padding-right:15px;">Entrées</th>'
            '<th colspan="2" style="text-align:left;">Répartition</th>'
            '</tr>'
            '</thead>'
            '<tbody>{}</tbody>'
            '</table>',
            format_html(''.join(rows))
        )
        
        return table
    categories_display.short_description = "Répartition par catégorie"

@admin.register(DailyStat)
class DailyStatAdmin(BaseStatAdmin):
    list_display = ('user_link', 'date', 'day_of_week_display', 'entries_count', 'mood_average_display', 'top_category_display')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'day_of_week_display')
        }),
        ('Statistiques', {
            'fields': ('entries_count', 'mood_average_display')
        }),
        ('Catégories', {
            'fields': ('categories_display',)
        }),
    )
    
    readonly_fields = ('day_of_week_display',) + BaseStatAdmin.readonly_fields
    
    def day_of_week_display(self, obj):
        """Affiche le jour de la semaine avec couleur pour week-end."""
        day = obj.day_of_week()
        if obj.is_weekend():
            return format_html('<span style="color:#dc3545;">{}</span>', day)
        return day
    day_of_week_display.short_description = "Jour"
    
    def top_category_display(self, obj):
        """Affiche la catégorie la plus utilisée."""
        if not obj.categories:
            return "-"
        
        # Trouver la catégorie avec le plus d'entrées
        top_category = max(obj.categories.items(), key=lambda x: x[1])
        return format_html(
            '<span style="padding:2px 6px; background:#f8f9fa; border-radius:3px;">{} ({})</span>',
            top_category[0], top_category[1]
        )
    top_category_display.short_description = "Top catégorie"

@admin.register(WeeklyStat)
class WeeklyStatAdmin(BaseStatAdmin):
    list_display = ('user_link', 'week_start', 'week_end_display', 'week_number_display', 'entries_count', 'mood_average_display', 'top_category_display')
    list_filter = ('week_start', 'user')
    search_fields = ('user__username', 'user__email')
    ordering = ('-week_start',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'week_start', 'week_end_display', 'week_number_display')
        }),
        ('Statistiques', {
            'fields': ('entries_count', 'mood_average_display')
        }),
        ('Catégories', {
            'fields': ('categories_display',)
        }),
    )
    
    readonly_fields = ('week_end_display', 'week_number_display') + BaseStatAdmin.readonly_fields
    
    def week_end_display(self, obj):
        """Affiche la date de fin de semaine."""
        return obj.week_end()
    week_end_display.short_description = "Fin de semaine"
    
    def week_number_display(self, obj):
        """Affiche le numéro de la semaine."""
        return format_html('Semaine {} de {}', obj.week_number(), obj.week_start.year)
    week_number_display.short_description = "Numéro de semaine"
    
    def top_category_display(self, obj):
        """Affiche la catégorie la plus utilisée."""
        top = obj.top_category()
        if not top:
            return "-"
        
        return format_html(
            '<span style="padding:2px 6px; background:#f8f9fa; border-radius:3px;">{} ({})</span>',
            top, obj.categories[top]
        )
    top_category_display.short_description = "Top catégorie"

@admin.register(MonthlyStat)
class MonthlyStatAdmin(BaseStatAdmin):
    list_display = ('user_link', 'month_display', 'entries_count', 'mood_average_display', 'top_category_display')
    list_filter = ('month_start', 'user')
    search_fields = ('user__username', 'user__email')
    ordering = ('-month_start',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'month_start', 'month_display')
        }),
        ('Statistiques', {
            'fields': ('entries_count', 'mood_average_display')
        }),
        ('Catégories', {
            'fields': ('categories_display',)
        }),
    )
    
    readonly_fields = ('month_display',) + BaseStatAdmin.readonly_fields
    
    def month_display(self, obj):
        """Affiche le mois en format lisible."""
        # Conversion des noms de mois en français
        month_names = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
            7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        return format_html('{} {}', month_names[obj.month_start.month], obj.month_start.year)
    month_display.short_description = "Mois"
    
    def top_category_display(self, obj):
        """Affiche la catégorie la plus utilisée."""
        if not obj.categories:
            return "-"
        
        # Trouver la catégorie avec le plus d'entrées
        top_category = max(obj.categories.items(), key=lambda x: x[1])
        return format_html(
            '<span style="padding:2px 6px; background:#f8f9fa; border-radius:3px;">{} ({})</span>',
            top_category[0], top_category[1]
        )
    top_category_display.short_description = "Top catégorie"

@admin.register(AnnualStat)
class AnnualStatAdmin(BaseStatAdmin):
    list_display = ('user_link', 'year_display', 'entries_count', 'mood_average_display', 'top_category_display')
    list_filter = ('year_start', 'user')
    search_fields = ('user__username', 'user__email')
    ordering = ('-year_start',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'year_start', 'year_display')
        }),
        ('Statistiques', {
            'fields': ('entries_count', 'mood_average_display')
        }),
        ('Catégories', {
            'fields': ('categories_display',)
        }),
    )
    
    readonly_fields = ('year_display',) + BaseStatAdmin.readonly_fields
    
    def year_display(self, obj):
        """Affiche l'année."""
        return format_html('Année {}', obj.year_start.year)
    year_display.short_description = "Année"
    
    def top_category_display(self, obj):
        """Affiche la catégorie la plus utilisée."""
        if not obj.categories:
            return "-"
        
        # Trouver la catégorie avec le plus d'entrées
        top_category = max(obj.categories.items(), key=lambda x: x[1])
        return format_html(
            '<span style="padding:2px 6px; background:#f8f9fa; border-radius:3px;">{} ({})</span>',
            top_category[0], top_category[1]
        )
    top_category_display.short_description = "Top catégorie"