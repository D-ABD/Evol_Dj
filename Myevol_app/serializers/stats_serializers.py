from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from collections import OrderedDict
from django.contrib.auth import get_user_model

from ..models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat

User = get_user_model()

class DailyStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques journalières."""
    day_of_week = serializers.SerializerMethodField()
    is_weekend = serializers.SerializerMethodField()
    date_formatted = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = DailyStat
        fields = [
            'id', 'user', 'user_username', 'date', 'date_formatted',
            'entries_count', 'mood_average', 'categories',
            'day_of_week', 'is_weekend', 'top_category'
        ]
        read_only_fields = fields

    def get_day_of_week(self, obj):
        return obj.day_of_week()

    def get_is_weekend(self, obj):
        return obj.is_weekend()

    def get_date_formatted(self, obj):
        return obj.date.strftime('%d %B %Y')

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]


class WeeklyStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques hebdomadaires."""
    week_end = serializers.SerializerMethodField()
    week_number = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    date_range = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = WeeklyStat
        fields = [
            'id', 'user', 'user_username', 'week_start', 'week_end',
            'week_number', 'entries_count', 'mood_average',
            'categories', 'top_category', 'date_range'
        ]
        read_only_fields = fields

    def get_week_end(self, obj):
        return obj.week_end()

    def get_week_number(self, obj):
        return obj.week_number()

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]

    def get_date_range(self, obj):
        week_end = obj.week_end()
        return {
            'start': obj.week_start.strftime('%d/%m/%Y'),
            'end': week_end.strftime('%d/%m/%Y'),
            'display': f"Du {obj.week_start.strftime('%d %B')} au {week_end.strftime('%d %B %Y')}"
        }


class MonthlyStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques mensuelles."""
    month_end = serializers.SerializerMethodField()
    month_name = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    date_range = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = MonthlyStat
        fields = [
            'id', 'user', 'user_username', 'month_start', 'month_end',
            'month_name', 'entries_count', 'mood_average',
            'categories', 'top_category', 'date_range'
        ]
        read_only_fields = fields

    def get_month_end(self, obj):
        """Retourne le dernier jour du mois."""
        next_month = (obj.month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        return next_month - timedelta(days=1)

    def get_month_name(self, obj):
        return obj.month_start.strftime('%B %Y')

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]

    def get_date_range(self, obj):
        month_end = self.get_month_end(obj)
        return {
            'start': obj.month_start.strftime('%d/%m/%Y'),
            'end': month_end.strftime('%d/%m/%Y'),
            'display': f"Du {obj.month_start.strftime('%d %B')} au {month_end.strftime('%d %B %Y')}"
        }



class AnnualStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques annuelles."""
    year_end = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AnnualStat
        fields = [
            'id', 'user', 'user_username', 'year_start', 'year_end',
            'year', 'entries_count', 'mood_average',
            'categories', 'top_category'
        ]
        read_only_fields = fields

    def get_year_end(self, obj):
        return obj.year_start.replace(month=12, day=31)

    def get_year(self, obj):
        return obj.year_start.year

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]


class StatsOverviewSerializer(serializers.Serializer):
    """Serializer pour afficher un résumé global des statistiques."""
    daily = serializers.SerializerMethodField()
    weekly = serializers.SerializerMethodField()
    monthly = serializers.SerializerMethodField()
    annual = serializers.SerializerMethodField()
    trends = serializers.SerializerMethodField()

    def get_daily(self, user):
        today = timezone.now().date()
        stat = DailyStat.generate_for_user(user, today)
        return DailyStatSerializer(stat).data

    def get_weekly(self, user):
        today = timezone.now().date()
        stat = WeeklyStat.generate_for_user(user, today)
        return WeeklyStatSerializer(stat).data

    def get_monthly(self, user):
        today = timezone.now().date()
        stat = MonthlyStat.generate_for_user(user, today)
        return MonthlyStatSerializer(stat).data

    def get_annual(self, user):
        today = timezone.now().date()
        stat = AnnualStat.generate_for_user(user, today)
        return AnnualStatSerializer(stat).data

    def get_trends(self, user):
        today = timezone.now().date()
        daily_stats = DailyStat.objects.filter(user=user, date__gte=today - timedelta(days=30)).order_by('date')

        if not daily_stats.exists():
            return {
                'entries_trend': 'stable',
                'mood_trend': 'stable',
                'entries_change': 0,
                'mood_change': 0,
                'most_active_day': None,
                'best_mood_day': None
            }

        past_15_days = daily_stats.filter(date__gte=today - timedelta(days=15))
        previous_15_days = daily_stats.filter(date__lt=today - timedelta(days=15))

        recent_entries_avg = sum(s.entries_count for s in past_15_days) / max(1, len(past_15_days))
        previous_entries_avg = sum(s.entries_count for s in previous_15_days) / max(1, len(previous_15_days))

        recent_moods = [s.mood_average for s in past_15_days if s.mood_average is not None]
        previous_moods = [s.mood_average for s in previous_15_days if s.mood_average is not None]

        recent_mood_avg = sum(recent_moods) / max(1, len(recent_moods)) if recent_moods else 0
        previous_mood_avg = sum(previous_moods) / max(1, len(previous_moods)) if previous_moods else 0

        entries_change = recent_entries_avg - previous_entries_avg
        mood_change = recent_mood_avg - previous_mood_avg

        entries_trend = 'up' if entries_change > 0.5 else ('down' if entries_change < -0.5 else 'stable')
        mood_trend = 'up' if mood_change > 0.5 else ('down' if mood_change < -0.5 else 'stable')

        most_active = max(daily_stats, key=lambda s: s.entries_count, default=None)
        best_mood = max((s for s in daily_stats if s.mood_average is not None), key=lambda s: s.mood_average, default=None)

        return {
            'entries_trend': entries_trend,
            'mood_trend': mood_trend,
            'entries_change': round(entries_change, 1),
            'mood_change': round(mood_change, 1),
            'most_active_day': {
                'date': most_active.date.strftime('%d/%m/%Y'),
                'day_of_week': most_active.day_of_week(),
                'entries_count': most_active.entries_count
            } if most_active else None,
            'best_mood_day': {
                'date': best_mood.date.strftime('%d/%m/%Y'),
                'day_of_week': best_mood.day_of_week(),
                'mood_average': best_mood.mood_average
            } if best_mood else None
        }


class StatsCategoryAnalysisSerializer(serializers.Serializer):
    """Serializer pour l'analyse des catégories."""
    period = serializers.ChoiceField(choices=['week', 'month', 'year', 'all'], default='month')

    def to_representation(self, instance):
        user = instance.get('user')
        period = instance.get('period', 'month')

        if not user:
            return {'error': 'Utilisateur non spécifié'}

        today = timezone.now().date()

        if period == 'week':
            stat = WeeklyStat.generate_for_user(user, today)
            start_date = stat.week_start
        elif period == 'month':
            stat = MonthlyStat.generate_for_user(user, today)
            start_date = stat.month_start
        elif period == 'year':
            stat = AnnualStat.generate_for_user(user, today)
            start_date = stat.year_start
        else:  # all
            stats = AnnualStat.objects.filter(user=user)
            if not stats.exists():
                return {
                    'title': "Analyse de toutes les entrées",
                    'categories': {},
                    'total_entries': 0,
                    'period': period
                }
            categories = {}
            total_entries = 0
            for stat in stats:
                total_entries += stat.entries_count
                for category, count in stat.categories.items():
                    categories[category] = categories.get(category, 0) + count
            return {
                'title': "Analyse de toutes les entrées",
                'categories': OrderedDict(sorted({
                    k: {'count': v, 'percentage': round((v / total_entries) * 100, 1) if total_entries > 0 else 0}
                    for k, v in categories.items()
                }.items(), key=lambda x: x[1]['count'], reverse=True)),
                'total_entries': total_entries,
                'period': period
            }

        categories = {
            k: {
                'count': v,
                'percentage': round((v / stat.entries_count) * 100, 1) if stat.entries_count > 0 else 0
            }
            for k, v in stat.categories.items()
        }

        end_date = (
            start_date + timedelta(days=6) if period == 'week' else
            (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            if period == 'month' else
            start_date.replace(month=12, day=31)
        )

        return {
            'title': f"Analyse des entrées - {period}",
            'categories': OrderedDict(sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True)),
            'total_entries': stat.entries_count,
            'period': period,
            'date_range': {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y')
            }
        }
