from django.contrib import admin
from .models import JournalEntry, Objective, User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Badge, BadgeTemplate
from django.contrib import admin
from .models import Notification

admin.site.register(User, UserAdmin)
admin.site.register(JournalEntry)
admin.site.register(Objective)



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notif_type', 'message', 'is_read', 'is_archived', 'created_at')
    list_filter = ('notif_type', 'is_read', 'is_archived', 'created_at')
    search_fields = ('message',)


@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "condition")
    search_fields = ("name", "condition")
    list_per_page = 20

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "icon", "date_obtenue")
    list_filter = ("name", "date_obtenue")
    search_fields = ("name", "user__username")
    autocomplete_fields = ("user",)
    readonly_fields = ("date_obtenue",)
