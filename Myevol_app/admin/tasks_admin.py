from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
    ClockedSchedule
)
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from celery import current_app


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'interval', 'crontab', 'solar', 'clocked', 'enabled', 'last_run_at', 'one_off', 'start_time', 'expire_seconds', 'run_now_link')
    list_filter = ('enabled', 'task', 'crontab', 'interval', 'solar', 'clocked')
    search_fields = ('name', 'task')
    ordering = ('-last_run_at',)
    readonly_fields = ('last_run_at', 'total_run_count')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('run-now/<int:pk>/', self.admin_site.admin_view(self.run_now_view), name='periodictask_run_now'),
        ]
        return custom_urls + urls

    def run_now_link(self, obj):
        return format_html(
            '<a class="button" href="{}">▶️ Exécuter maintenant</a>',
            f'run-now/{obj.pk}/'
        )
    run_now_link.short_description = "Action immédiate"
    run_now_link.allow_tags = True

    def run_now_view(self, request, pk, *args, **kwargs):
        task = PeriodicTask.objects.get(pk=pk)
        try:
            current_app.send_task(task.task)
            self.message_user(request, f"Tâche {task.name} déclenchée avec succès ✅", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Erreur lors du lancement : {e}", messages.ERROR)
        return redirect('admin:django_celery_beat_periodictask_changelist')


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')
    search_fields = ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(admin.ModelAdmin):
    list_display = ('every', 'period')
    search_fields = ('every', 'period')


@admin.register(SolarSchedule)
class SolarScheduleAdmin(admin.ModelAdmin):
    list_display = ('event', 'latitude', 'longitude')
    search_fields = ('event',)


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(admin.ModelAdmin):
    list_display = ('clocked_time',)
    search_fields = ('clocked_time',)
