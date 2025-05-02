from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import now

from ..models.journal_model import JournalEntry, JournalMedia

class JournalMediaInline(admin.TabularInline):
    model = JournalMedia
    extra = 0
    readonly_fields = ('preview', 'file_size_display')
    can_delete = True
    fields = ('type', 'file', 'preview', 'file_size_display')

    def preview(self, obj):
        """Affiche une miniature pour les images et un lecteur pour l'audio."""
        if not obj.file:
            return "-"
        
        if obj.type == 'image':
            return format_html('<img src="{}" style="max-height:100px; border-radius:5px;" />', obj.file.url)
        elif obj.type == 'audio':
            return format_html('<audio controls style="max-width:200px;"><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"
    
    def file_size_display(self, obj):
        """Affiche la taille du fichier en format lisible."""
        if not obj.file:
            return "-"
        
        size_bytes = obj.file_size()
        if size_bytes < 1024:
            return f"{size_bytes} octets"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} Ko"
        else:
            return f"{size_bytes/(1024*1024):.1f} Mo"
    file_size_display.short_description = "Taille"

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'content_preview', 'mood_display', 'category', 'created_at', 'media_count')
    list_filter = ('mood', 'category', 'created_at')
    search_fields = ('content', 'user__username', 'category')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [JournalMediaInline]
    
    readonly_fields = ('mood_emoji_display', 'created_at', 'updated_at', 'media_count')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'content', ('mood', 'mood_emoji_display'), 'category')
        }),
        ('Informations temporelles', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_link(self, obj):
        """Affiche un lien vers l'utilisateur."""
        url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"

    def content_preview(self, obj):
        """Affiche un extrait du contenu."""
        max_length = 50
        if len(obj.content) > max_length:
            return format_html('{}...', obj.content[:max_length])
        return obj.content
    content_preview.short_description = "Contenu"

    def mood_display(self, obj):
        """Affiche l'humeur avec un indicateur visuel et l'emoji."""
        emoji = obj.get_mood_emoji()
        # Couleur progressive: rouge pour 1-3, orange pour 4-6, vert pour 7-10
        if obj.mood <= 3:
            color = "#dc3545"  # Rouge
        elif obj.mood <= 6:
            color = "#fd7e14"  # Orange
        else:
            color = "#28a745"  # Vert
            
        return format_html(
            '<div style="display:flex; align-items:center;">'
            '<div style="width:{}px; height:10px; background-color:{}; border-radius:5px; margin-right:5px;"></div> {} {}/10'
            '</div>',
            obj.mood * 10, color, emoji, obj.mood
        )
    mood_display.short_description = "Humeur"
    
    def mood_emoji_display(self, obj):
        """Affiche uniquement l'emoji pour le champ de détail."""
        return format_html('<span style="font-size:2em;">{}</span>', obj.get_mood_emoji())
    mood_emoji_display.short_description = "Emoji"
    
    def media_count(self, obj):
        """Compte le nombre de médias associés."""
        count = obj.media.count()
        if count == 0:
            return "Aucun média"
        return f"{count} média{'s' if count > 1 else ''}"
    media_count.short_description = "Médias"

@admin.register(JournalMedia)
class JournalMediaAdmin(admin.ModelAdmin):
    list_display = ('entry_link', 'type', 'file', 'preview_thumb', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('entry__content', 'entry__user__username')
    date_hierarchy = 'created_at'
    
    readonly_fields = ('preview', 'file_size_display', 'created_at')
    
    fieldsets = (
        (None, {
            'fields': ('entry', 'type', 'file')
        }),
        ('Aperçu', {
            'fields': ('preview', 'file_size_display', 'created_at')
        }),
    )
    
    def entry_link(self, obj):
        """Affiche un lien vers l'entrée associée."""
        url = reverse("admin:Myevol_app_journalentry_change", args=[obj.entry.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.entry))
    entry_link.short_description = "Entrée"
    
    def preview_thumb(self, obj):
        """Version miniature de l'aperçu pour la liste."""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height:40px; border-radius:3px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls style="max-width:100px; height:20px;"><source src="{}"></audio>', obj.file.url)
        return "-"
    preview_thumb.short_description = "Aperçu"
    
    def preview(self, obj):
        """Aperçu complet pour la page de détail."""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height:300px; border-radius:5px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls style="width:100%;"><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"
    
    def file_size_display(self, obj):
        """Affiche la taille du fichier en format lisible."""
        if not obj.file:
            return "-"
        
        size_bytes = obj.file_size()
        if size_bytes < 1024:
            return f"{size_bytes} octets"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} Ko"
        else:
            return f"{size_bytes/(1024*1024):.1f} Mo"
    file_size_display.short_description = "Taille du fichier"