from django.contrib import admin
from django.utils.html import format_html
import random

from ..models.quote_model import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author_display', 'text_preview', 'mood_tag_display', 'length_display')
    list_filter = ('mood_tag', 'author')
    search_fields = ('text', 'author', 'mood_tag')
    ordering = ('author', 'id')
    actions = ['assign_random_mood_tag']
    
    fieldsets = (
        (None, {
            'fields': ('text', 'author')
        }),
        ('Catégorisation', {
            'fields': ('mood_tag',),
            'description': 'Aide à cibler les citations en fonction du contexte.'
        }),
    )

    def author_display(self, obj):
        """Affiche l'auteur avec une mise en forme spéciale."""
        author = obj.author if obj.author else "Inconnu"
        if author == "Inconnu":
            return format_html('<em style="color:#6c757d;">Inconnu</em>')
        return format_html('<strong>{}</strong>', author)
    author_display.short_description = "Auteur"
    author_display.admin_order_field = 'author'

    def text_preview(self, obj):
        """Affiche un extrait stylisé de la citation."""
        max_length = 75
        text = obj.text
        if len(text) > max_length:
            preview = text[:max_length] + "..."
        else:
            preview = text
            
        return format_html('<span style="font-style:italic;">"{}"{}</span>', 
                          preview, 
                          " ..." if len(text) > max_length else "")
    text_preview.short_description = "Citation"

    def mood_tag_display(self, obj):
        """Affiche le mood_tag avec code couleur."""
        if not obj.mood_tag:
            return format_html('<span style="color:#6c757d;">—</span>')
            
        colors = {
            'positive': '#28a745',  # Vert
            'neutral': '#17a2b8',   # Bleu-cyan
            'low': '#dc3545'        # Rouge
        }
        bg_colors = {
            'positive': '#d4edda',  # Vert clair
            'neutral': '#d1ecf1',   # Bleu clair
            'low': '#f8d7da'        # Rouge clair
        }
        icons = {
            'positive': '😊',
            'neutral': '😐',
            'low': '😢'
        }
        
        color = colors.get(obj.mood_tag, '#6c757d')
        bg = bg_colors.get(obj.mood_tag, '#f8f9fa')
        icon = icons.get(obj.mood_tag, '')
        
        return format_html(
            '<span style="padding:3px 8px; border-radius:4px; background:{}; color:{};">{} {}</span>', 
            bg, color, icon, obj.mood_tag
        )
    mood_tag_display.short_description = "Humeur"
    mood_tag_display.admin_order_field = 'mood_tag'
    
    def length_display(self, obj):
        """Affiche la longueur de la citation."""
        length = obj.length()
        # Catégorisation de la longueur
        if length < 50:
            category = "Courte"
            color = "#28a745"  # Vert
        elif length < 150:
            category = "Moyenne"
            color = "#17a2b8"  # Bleu
        else:
            category = "Longue"
            color = "#dc3545"  # Rouge
            
        return format_html(
            '<span style="color:{};">{} ({} caractères)</span>',
            color, category, length
        )
    length_display.short_description = "Longueur"
    
    def assign_random_mood_tag(self, request, queryset):
        """Action pour assigner un mood_tag aléatoire aux citations sélectionnées."""
        mood_tags = ['positive', 'neutral', 'low']
        updated = 0
        
        for quote in queryset:
            if not quote.mood_tag:
                quote.mood_tag = random.choice(mood_tags)
                quote.save()
                updated += 1
                
        if updated:
            self.message_user(request, f"{updated} citation(s) mise(s) à jour avec un mood_tag aléatoire.")
        else:
            self.message_user(request, "Aucune citation n'a été mise à jour.")
    assign_random_mood_tag.short_description = "Assigner un mood_tag aléatoire"
    
    def get_readonly_fields(self, request, obj=None):
        """Affiche des champs supplémentaires en lecture seule lors de l'édition."""
        if obj:  # En édition
            return ['length_display']
        return []