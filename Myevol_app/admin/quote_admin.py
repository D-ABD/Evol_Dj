from django.contrib import admin

from ..models.quote_model import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author_display', 'text_preview', 'mood_tag')
    list_filter = ('mood_tag',)
    search_fields = ('text', 'author')
    ordering = ('author',)

    def author_display(self, obj):
        """Affiche l'auteur ou 'Inconnu'."""
        return obj.author if obj.author else "Inconnu"
    author_display.short_description = "Auteur"

    def text_preview(self, obj):
        """Affiche un extrait de la citation."""
        if len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text
    text_preview.short_description = "Citation"
