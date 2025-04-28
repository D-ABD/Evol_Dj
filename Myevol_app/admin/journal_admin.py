from django.contrib import admin
from django.utils.html import format_html

from ..models.journal_model import JournalEntry, JournalMedia

class JournalMediaInline(admin.TabularInline):
    model = JournalMedia
    extra = 0
    readonly_fields = ('preview',)
    can_delete = False

    def preview(self, obj):
        """Affiche une miniature pour les images et un lecteur pour l'audio."""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height:100px;" />', obj.file.url)
        if obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_preview', 'mood_display', 'category', 'created_at')
    list_filter = ('mood', 'category')
    search_fields = ('content', 'user__username', 'category')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [JournalMediaInline]

    def content_preview(self, obj):
        """Affiche un extrait du contenu."""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = "Contenu"

    def mood_display(self, obj):
        """Affiche l'emoji d'humeur."""
        return obj.get_mood_emoji()
    mood_display.short_description = "Humeur"

@admin.register(JournalMedia)
class JournalMediaAdmin(admin.ModelAdmin):
    list_display = ('entry', 'type', 'file', 'created_at')
    list_filter = ('type',)
    search_fields = ('entry__content',)
    date_hierarchy = 'created_at'
