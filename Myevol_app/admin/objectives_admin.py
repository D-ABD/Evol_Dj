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


# ===== 🏅 Gestion des badges =====
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_link', 'icon_display', 'date_obtenue', 'level', 'is_new')
    list_filter = ('name', 'date_obtenue', 'level')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    date_hierarchy = 'date_obtenue'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur personnalisé"""
        if obj.user:
            url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"

    
    def icon_display(self, obj):
        """Affiche l'icône du badge"""
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    icon_display.short_description = "Icône"
    
    def is_new(self, obj):
        """Indique si le badge a été obtenu aujourd'hui"""
        return obj.was_earned_today()
    is_new.boolean = True
    is_new.short_description = "Nouveau"


@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_display', 'level', 'condition', 'badges_count')
    list_filter = ('level',)
    search_fields = ('name', 'description', 'condition')
    
    def icon_display(self, obj):
        """Affiche l'icône du template de badge"""
        return format_html('<span style="font-size: 1.5em; color: {};">{}</span>', 
                           obj.color_theme, obj.icon)
    icon_display.short_description = "Icône"
    
    def badges_count(self, obj):
        """Nombre de badges attribués de ce type"""
        return Badge.objects.filter(name=obj.name).count()
    badges_count.short_description = "Badges attribués"


# ===== 🎯 Gestion des défis =====
class ChallengeProgressInline(admin.TabularInline):
    model = ChallengeProgress
    extra = 0
    readonly_fields = ('user', 'completed', 'completed_at')
    fields = ('user', 'completed', 'completed_at')
    can_delete = False
    max_num = 20
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'target_entries', 'is_active_now', 'days_left', 'participants_count')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    inlines = [ChallengeProgressInline]
    
    def is_active_now(self, obj):
        """Vérifie si le défi est actuellement actif"""
        return obj.is_active()
    is_active_now.boolean = True
    is_active_now.short_description = "Actif"
    
    def days_left(self, obj):
        """Jours restants avant la fin du défi"""
        days = obj.days_remaining()
        if days <= 0:
            return "Terminé"
        return f"{days} jour{'s' if days > 1 else ''}"
    days_left.short_description = "Jours restants"
    
    def participants_count(self, obj):
        """Nombre d'utilisateurs participant au défi"""
        return obj.progresses.count()
    participants_count.short_description = "Participants"


@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge_link', 'completed', 'completed_at', 'progress_percent')
    list_filter = ('completed', 'completed_at', 'challenge')
    search_fields = ('user__username', 'user__email', 'challenge__title')
    date_hierarchy = 'completed_at'
    raw_id_fields = ('user', 'challenge')
    
    def challenge_link(self, obj):
        """Affiche un lien vers l'admin du défi"""
        url = reverse("admin:core_challenge_change", args=[obj.challenge.id])
        return format_html('<a href="{}">{}</a>', url, obj.challenge.title)
    challenge_link.short_description = "Défi"
    
    def progress_percent(self, obj):
        """Affiche le pourcentage de progression"""
        progress = obj.get_progress()
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px;">'
            '<div style="width: {}%; background-color: #4CAF50; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            progress['percent'], progress['percent'])
    progress_percent.short_description = "Progression"


# ===== 📝 Gestion du journal =====
class JournalMediaInline(admin.TabularInline):
    model = JournalMedia
    extra = 0
    fields = ('file', 'type', 'created_at', 'preview')
    readonly_fields = ('created_at', 'preview')
    
    def preview(self, obj):
        """Affiche un aperçu du média"""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 300px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'display_date', 'mood_with_emoji', 'category', 'content_preview')
    list_filter = ('mood', 'category', 'created_at')
    search_fields = ('content', 'user__username', 'user__email', 'category')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    inlines = [JournalMediaInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def display_date(self, obj):
        """Affiche la date de création formatée"""
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    display_date.short_description = "Date"
    
    def mood_with_emoji(self, obj):
        """Affiche l'humeur avec son emoji correspondant"""
        return format_html('{} <span style="font-size: 1.2em;">{}</span>', 
                           obj.mood, obj.get_mood_emoji())
    mood_with_emoji.short_description = "Humeur"
    
    def content_preview(self, obj):
        """Affiche un aperçu du contenu"""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = "Contenu"


@admin.register(JournalMedia)
class JournalMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry_link', 'type', 'file_size_display', 'created_at', 'preview')
    list_filter = ('type', 'created_at')
    search_fields = ('entry__content', 'entry__user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'preview')
    
    def entry_link(self, obj):
        """Affiche un lien vers l'admin de l'entrée"""
        url = reverse("admin:core_journalentry_change", args=[obj.entry.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.entry))
    entry_link.short_description = "Entrée"
    
    def file_size_display(self, obj):
        """Affiche la taille du fichier en format lisible"""
        size = obj.file_size()
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    file_size_display.short_description = "Taille"
    
    def preview(self, obj):
        """Affiche un aperçu du média"""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 400px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"


# ===== 🎯 Gestion des objectifs =====
@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_link', 'category', 'target_date', 'done_status', 'progress_display')
    list_filter = ('done', 'category', 'target_date')
    search_fields = ('title', 'user__username', 'user__email', 'category')
    date_hierarchy = 'target_date'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def done_status(self, obj):
        """Affiche l'état de complétion de l'objectif"""
        if obj.done:
            return format_html('<span style="color: green;">✓ Terminé</span>')
        elif obj.is_overdue():
            return format_html('<span style="color: red;">⚠ En retard</span>')
        else:
            return format_html('<span style="color: orange;">⏳ En cours</span>')
    done_status.short_description = "État"
    
    def progress_display(self, obj):
        """Affiche la progression de l'objectif sous forme de barre"""
        progress = obj.progress()
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px;">'
            '<div style="width: {}%; background-color: {}; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            progress, '#4CAF50' if progress == 100 else '#2196F3', progress)
    progress_display.short_description = "Progression"


# ===== 🔔 Gestion des notifications =====
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'notif_type_display', 'message_preview', 'is_read', 'archived', 'created_at')
    list_filter = ('notif_type', 'is_read', 'archived', 'created_at')
    search_fields = ('message', 'user__username', 'user__email')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    actions = ['mark_as_read', 'mark_as_unread', 'archive_notifications']
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def notif_type_display(self, obj):
        """Affiche le type de notification avec une couleur distinctive"""
        colors = {
            'badge': '#9C27B0',
            'objectif': '#4CAF50',
            'statistique': '#2196F3',
            'info': '#607D8B'
        }
        return format_html('<span style="color: {};">{}</span>', 
                          colors.get(obj.notif_type, 'black'), obj.type_display)
    notif_type_display.short_description = "Type"
    
    def message_preview(self, obj):
        """Affiche un aperçu du message"""
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = "Message"
    
    def mark_as_read(self, request, queryset):
        """Action pour marquer les notifications comme lues"""
        updated = queryset.update(is_read=True, read_at=now())
        self.message_user(request, f"{updated} notification(s) marquée(s) comme lue(s).")
    mark_as_read.short_description = "Marquer comme lues"
    
    def mark_as_unread(self, request, queryset):
        """Action pour marquer les notifications comme non lues"""
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f"{updated} notification(s) marquée(s) comme non lue(s).")
    mark_as_unread.short_description = "Marquer comme non lues"
    
    def archive_notifications(self, request, queryset):
        """Action pour archiver les notifications"""
        updated = queryset.update(archived=True)
        self.message_user(request, f"{updated} notification(s) archivée(s).")
    archive_notifications.short_description = "Archiver les notifications"


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


# ===== 📝 Gestion des logs d'événements =====
@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_link', 'action', 'description_preview', 'has_metadata')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'user__email', 'action', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'user', 'action', 'description', 'metadata_formatted')
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        if obj.user:
            url = reverse("admin:auth_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = "Utilisateur"
    
    def description_preview(self, obj):
        """Affiche un aperçu de la description"""
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description
    description_preview.short_description = "Description"
    
    def has_metadata(self, obj):
        """Indique si le log contient des métadonnées"""
        return obj.metadata is not None and bool(obj.metadata)
    has_metadata.boolean = True
    has_metadata.short_description = "Métadonnées"
    
    def metadata_formatted(self, obj):
        """Affiche les métadonnées formatées en JSON"""
        if not obj.metadata:
            return "-"
        import json
        return format_html('<pre>{}</pre>', json.dumps(obj.metadata, indent=2))
    metadata_formatted.short_description = "Métadonnées"


# ===== 👤 Gestion des utilisateurs et préférences =====
class UserPreferenceInline(admin.StackedInline):
    model = UserPreference
    can_delete = False
    fieldsets = (
        ('Notifications', {
            'fields': (('notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique'),)
        }),
        ('Apparence', {
            'fields': (('dark_mode', 'accent_color'), ('font_choice', 'enable_animations'))
        }),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'date_joined', 'level_display', 'entries_count', 'streak_display')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login', 'entries_count', 'current_streak', 'mood_avg', 'badges_count')
    inlines = [UserPreferenceInline]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'avatar_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Statistiques', {'fields': ('entries_count', 'current_streak', 'longest_streak', 'xp', 'mood_avg', 'badges_count')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    def full_name(self, obj):
        """Retourne le nom complet de l'utilisateur"""
        return obj.get_full_name() or "-"
    full_name.short_description = "Nom complet"
    
    def entries_count(self, obj):
        """Nombre total d'entrées de journal"""
        return obj.total_entries()
    entries_count.short_description = "Entrées"
    
    def current_streak(self, obj):
        """Série actuelle de jours consécutifs"""
        return obj.current_streak()
    current_streak.short_description = "Série actuelle"
    
    def mood_avg(self, obj):
        """Moyenne d'humeur sur les 7 derniers jours"""
        avg = obj.mood_average(7)
        if avg is None:
            return "-"
        return f"{avg:.1f}/10"
    mood_avg.short_description = "Humeur (7j)"
    
    def badges_count(self, obj):
        """Nombre de badges obtenus"""
        return obj.badges.count()
    badges_count.short_description = "Badges"
    
    def level_display(self, obj):
        """Affiche le niveau avec une barre visuelle"""
        level = obj.level
        from ..utils.levels import get_user_progress
        progress = get_user_progress(obj.total_entries())
        
        return format_html(
            '<div><strong>Niveau {}</strong></div>'
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px; margin-top: 2px;">'
            '<div style="width: {}%; background-color: #673AB7; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            level, progress["progress"], progress["progress"])
    level_display.short_description = "Niveau"
    
    def streak_display(self, obj):
        """Affiche les séries de jours consécutifs"""
        current = obj.current_streak()
        longest = obj.longest_streak
        
        if current == 0:
            return "Aucune série active"
        
        if current == longest:
            return format_html('<span style="color: #4CAF50; font-weight: bold;">{} jour(s) 🔥</span>', current)
        
        return format_html('Actuelle: <span style="color: #2196F3;">{}</span> | '
                          'Record: <span style="color: #4CAF50;">{}</span>', 
                          current, longest)
    streak_display.short_description = "Séries"


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'notifications_enabled', 'accent_color_display', 'font_choice')
    list_filter = ('dark_mode', 'notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique', 'font_choice')
    search_fields = ('user__username', 'user__email')
    actions = ['reset_to_defaults']
    
    def notifications_enabled(self, obj):
        """Affiche quelles notifications sont activées"""
        enabled = []
        if obj.notif_badge:
            enabled.append("Badge")
        if obj.notif_objectif:
            enabled.append("Objectif")
        if obj.notif_info:
            enabled.append("Info")
        if obj.notif_statistique:
            enabled.append("Statistique")
            
        if not enabled:
            return format_html('<span style="color: #F44336;">Aucune</span>')
        elif len(enabled) == 4:
            return format_html('<span style="color: #4CAF50;">Toutes</span>')
        else:
            return ", ".join(enabled)
    notifications_enabled.short_description = "Notifications"
    
    def accent_color_display(self, obj):
        """Affiche la couleur d'accent avec un échantillon visuel"""
        return format_html(
            '<div style="display: inline-block; width: 20px; height: 20px; background-color: {}; '
            'border-radius: 50%; vertical-align: middle; margin-right: 5px;"></div> {}',
            obj.accent_color, obj.accent_color)
    accent_color_display.short_description = "Couleur d'accent"
    
    def reset_to_defaults(self, request, queryset):
        """Action pour réinitialiser les préférences aux valeurs par défaut"""
        for pref in queryset:
            pref.reset_to_defaults()
        self.message_user(request, f"{queryset.count()} préférence(s) réinitialisée(s) avec succès.")
    reset_to_defaults.short_description = "Réinitialiser aux valeurs par défaut"


# Configuration des groupes d'administration
admin.site.site_header = "Administration MyEvol"
admin.site.site_title = "MyEvol Admin"
admin.site.index_title = "Tableau de bord d'administration"

# Organisation des modèles par sections dans l'admin
class MyEvolAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Organise les modèles par groupes fonctionnels pour une navigation plus intuitive
        """
        app_list = super().get_app_list(request)
        
        # Créer des sections personnalisées
        custom_app_list = []
        
        # Section Utilisateurs
        users_app = {
            'name': 'Utilisateurs',
            'app_label': 'users',
            'app_url': '/admin/users/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Journal
        journal_app = {
            'name': 'Journal',
            'app_label': 'journal',
            'app_url': '/admin/journal/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Engagement
        engagement_app = {
            'name': 'Engagement',
            'app_label': 'engagement',
            'app_url': '/admin/engagement/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Statistiques
        stats_app = {
            'name': 'Statistiques',
            'app_label': 'stats',
            'app_url': '/admin/stats/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Système
        system_app = {
            'name': 'Système',
            'app_label': 'system',
            'app_url': '/admin/system/',
            'has_module_perms': True,
            'models': []
        }
        
        # Dictionnaire pour mapper les modèles aux sections
        model_mapping = {
            'users': ['User', 'UserPreference', 'Badge', 'BadgeTemplate'],
            'journal': ['JournalEntry', 'JournalMedia', 'Objective'],
            'engagement': ['Challenge', 'ChallengeProgress', 'Notification', 'Quote'],
            'stats': ['DailyStat', 'WeeklyStat'],
            'system': ['EventLog']
        }
        
        # Obtenir tous les modèles
        all_models = []
        for app in app_list:
            all_models.extend(app['models'])
        
        # Répartir les modèles dans les sections personnalisées
        for model in all_models:
            model_name = model['object_name']
            
            if model_name in model_mapping['users']:
                users_app['models'].append(model)
            elif model_name in model_mapping['journal']:
                journal_app['models'].append(model)
            elif model_name in model_mapping['engagement']:
                engagement_app['models'].append(model)
            elif model_name in model_mapping['stats']:
                stats_app['models'].append(model)
            elif model_name in model_mapping['system']:
                system_app['models'].append(model)
        
        # Ajouter les sections à la liste personnalisée
        custom_app_list.append(users_app)
        custom_app_list.append(journal_app)
        custom_app_list.append(engagement_app)
        custom_app_list.append(stats_app)
        custom_app_list.append(system_app)
        
        # Garder les autres applications non classées
        for app in app_list:
            if app['app_label'] not in ['users', 'journal', 'engagement', 'stats', 'system']:
                custom_app_list.append(app)
        
        return custom_app_list


# Utiliser notre site admin personnalisé si activé
# Pour activer, décommentez ces lignes et modifiez urls.py
# admin_site = MyEvolAdminSite(name='myadmin')
# admin_site.register(User, UserAdmin)
# admin_site.register(UserPreference, UserPreferenceAdmin)
# ... (enregistrer tous les autres modèles)

# Dans urls.py, vous devrez remplacer:
# from django.contrib import admin
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
# Par:
# from myapp.admin import admin_site
# urlpatterns = [
#     path('admin/', admin_site.urls),
# ]