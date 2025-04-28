from django.contrib import admin

from ..models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat

@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'entries_count', 'mood_average_display')
    list_filter = ('date',)
    search_fields = ('user__username',)
    date_hierarchy = 'date'
    ordering = ('-date',)

    def mood_average_display(self, obj):
        if obj.mood_average is not None:
            return f"{obj.mood_average:.1f} / 10"
        return "-"
    mood_average_display.short_description = "Humeur"

@admin.register(WeeklyStat)
class WeeklyStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_start', 'entries_count', 'mood_average_display')
    list_filter = ('week_start',)
    search_fields = ('user__username',)
    ordering = ('-week_start',)

    def mood_average_display(self, obj):
        if obj.mood_average is not None:
            return f"{obj.mood_average:.1f} / 10"
        return "-"
    mood_average_display.short_description = "Humeur"

@admin.register(MonthlyStat)
class MonthlyStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'month_start', 'entries_count', 'mood_average_display')
    list_filter = ('month_start',)
    search_fields = ('user__username',)
    ordering = ('-month_start',)

    def mood_average_display(self, obj):
        if obj.mood_average is not None:
            return f"{obj.mood_average:.1f} / 10"
        return "-"
    mood_average_display.short_description = "Humeur"

@admin.register(AnnualStat)
class AnnualStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'year_start', 'entries_count', 'mood_average_display')
    list_filter = ('year_start',)
    search_fields = ('user__username',)
    ordering = ('-year_start',)

    def mood_average_display(self, obj):
        if obj.mood_average is not None:
            return f"{obj.mood_average:.1f} / 10"
        return "-"
    mood_average_display.short_description = "Humeur"
