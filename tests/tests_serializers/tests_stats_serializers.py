from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from Myevol_app.models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat
from Myevol_app.serializers.stats_serializers import (
    DailyStatSerializer,
    WeeklyStatSerializer,
    MonthlyStatSerializer,
    AnnualStatSerializer,
    StatsOverviewSerializer,
    StatsCategoryAnalysisSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class StatsSerializersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="statuser", email="stat@example.com", password="password")
        
        today = timezone.now().date()
        self.daily_stat = DailyStat.objects.create(
            user=self.user, date=today, entries_count=5, mood_average=7.2,
            categories={"travail": 3, "santé": 2}
        )
        self.weekly_stat = WeeklyStat.objects.create(
            user=self.user, week_start=today - timedelta(days=today.weekday()),
            entries_count=20, mood_average=7.0,
            categories={"travail": 10, "loisir": 5}
        )
        self.monthly_stat = MonthlyStat.objects.create(
            user=self.user, month_start=today.replace(day=1),
            entries_count=60, mood_average=7.5,
            categories={"travail": 30, "famille": 20}
        )
        self.annual_stat = AnnualStat.objects.create(
            user=self.user, year_start=today.replace(month=1, day=1),
            entries_count=300, mood_average=7.8,
            categories={"travail": 150, "santé": 80}
        )

    # --- DailyStat ---
    def test_daily_stat_serializer_fields(self):
        serializer = DailyStatSerializer(self.daily_stat)
        data = serializer.data
        self.assertEqual(data['entries_count'], 5)
        self.assertEqual(data['top_category'], "travail")
        self.assertIn('day_of_week', data)
        self.assertIn('is_weekend', data)
        self.assertIn('date_formatted', data)

    # --- WeeklyStat ---
    def test_weekly_stat_serializer_fields(self):
        serializer = WeeklyStatSerializer(self.weekly_stat)
        data = serializer.data
        self.assertEqual(data['entries_count'], 20)
        self.assertEqual(data['top_category'], "travail")
        self.assertIn('week_number', data)
        self.assertIn('date_range', data)

    # --- MonthlyStat ---
    def test_monthly_stat_serializer_fields(self):
        serializer = MonthlyStatSerializer(self.monthly_stat)
        data = serializer.data
        self.assertEqual(data['entries_count'], 60)
        self.assertEqual(data['top_category'], "travail")
        self.assertIn('month_name', data)
        self.assertIn('date_range', data)

    # --- AnnualStat ---
    def test_annual_stat_serializer_fields(self):
        serializer = AnnualStatSerializer(self.annual_stat)
        data = serializer.data
        self.assertEqual(data['entries_count'], 300)
        self.assertEqual(data['top_category'], "travail")
        self.assertIn('year', data)
        self.assertIn('year_end', data)

    # --- StatsOverview ---
    def test_stats_overview_serializer(self):
        serializer = StatsOverviewSerializer()
        output = serializer.to_representation(self.user)
        
        self.assertIn('daily', output)
        self.assertIn('weekly', output)
        self.assertIn('monthly', output)
        self.assertIn('annual', output)
        self.assertIn('trends', output)

    # --- StatsCategoryAnalysis ---
    def test_stats_category_analysis_week(self):
        serializer = StatsCategoryAnalysisSerializer()
        output = serializer.to_representation({'user': self.user, 'period': 'week'})
        
        self.assertIn('categories', output)
        self.assertEqual(output['period'], 'week')

    def test_stats_category_analysis_month(self):
        serializer = StatsCategoryAnalysisSerializer()
        output = serializer.to_representation({'user': self.user, 'period': 'month'})
        
        self.assertIn('categories', output)
        self.assertEqual(output['period'], 'month')

    def test_stats_category_analysis_year(self):
        serializer = StatsCategoryAnalysisSerializer()
        output = serializer.to_representation({'user': self.user, 'period': 'year'})
        
        self.assertIn('categories', output)
        self.assertEqual(output['period'], 'year')

    def test_stats_category_analysis_all(self):
        serializer = StatsCategoryAnalysisSerializer()
        output = serializer.to_representation({'user': self.user, 'period': 'all'})
        
        self.assertIn('categories', output)
        self.assertEqual(output['period'], 'all')

    def test_stats_category_analysis_no_user(self):
        serializer = StatsCategoryAnalysisSerializer()
        output = serializer.to_representation({'period': 'month'})
        
        self.assertIn('error', output)
