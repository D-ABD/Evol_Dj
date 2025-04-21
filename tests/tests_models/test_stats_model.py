from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta, date
from django.contrib.auth import get_user_model
from Myevol_app.models.stats_model import WeeklyStat, DailyStat
from Myevol_app.models.journal_model import JournalEntry

User = get_user_model()

class StatsModelTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        JournalEntry.objects.all().delete()
        self.today = now().date()
        self.monday = self.today - timedelta(days=self.today.weekday())

        self.entry1 = JournalEntry.objects.create(
            user=self.user,
            content="Test entry 1",
            category="Travail",
            mood=7,
            created_at=now()
        )

        self.entry2 = JournalEntry.objects.create(
            user=self.user,
            content="Test entry 2",
            category="Sport",
            mood=9,
            created_at=now()
        )

        yesterday = now() - timedelta(days=1)
        self.entry3 = JournalEntry.objects.create(
            user=self.user,
            content="Entry from yesterday",
            category="Travail",
            mood=6,
            created_at=yesterday
        )

        last_week = now() - timedelta(days=8)
        self.entry4 = JournalEntry.objects.create(
            user=self.user,
            content="Entry from last week",
            category="Loisirs",
            mood=8,
            created_at=last_week
        )

        self.today_entries = JournalEntry.objects.filter(
            user=self.user,
            created_at__date=self.today
        ).count()

        self.this_week_entries = JournalEntry.objects.filter(
            user=self.user,
            created_at__date__range=(self.monday, self.monday + timedelta(days=6))
        ).count()

    def test_daily_stat_generation(self):
        stat = DailyStat.generate_for_user(self.user, date=self.today)
        self.assertEqual(stat.date, self.today)
        self.assertEqual(stat.entries_count, self.today_entries)
        if stat.entries_count == 2:
            self.assertEqual(stat.mood_average, 8.0)
            self.assertEqual(len(stat.categories), 2)
            self.assertEqual(stat.categories.get("Travail"), 1)
            self.assertEqual(stat.categories.get("Sport"), 1)

    def test_daily_stat_day_of_week(self):
        DailyStat.objects.filter(user=self.user, date=now().date()).delete()
        stat = DailyStat.objects.create(
            user=self.user,
            date=now().date(),
            entries_count=3,
            mood_average=6.0
        )
        self.assertEqual(stat.day_of_week(), "Lundi")  # Correction possible à adapter selon la date

    def test_daily_stat_is_weekend(self):
        test_date = now().date()
        DailyStat.objects.filter(user=self.user, date=test_date).delete()
        stat = DailyStat.objects.create(
            user=self.user,
            date=test_date,
            entries_count=2,
            mood_average=7.0
        )
        is_weekend = test_date.weekday() >= 5
        self.assertEqual(stat.is_weekend(), is_weekend)

    def test_daily_stat_calendar_data(self):
        DailyStat.generate_for_user(self.user, date=self.today)
        DailyStat.generate_for_user(self.user, date=self.today - timedelta(days=1))
        calendar_data = DailyStat.get_calendar_data(self.user)
        self.assertIsInstance(calendar_data, list)
        self.assertTrue(len(calendar_data) >= 2)
        item = calendar_data[0]
        self.assertIn('date', item)
        self.assertIn('count', item)
        self.assertIn('mood', item)
        self.assertIn('intensity', item)
        self.assertTrue(0 <= item['intensity'] <= 1)

    def test_weekly_stat_generation(self):
        stat, created = WeeklyStat.generate_for_user(self.user, reference_date=self.today)
        self.assertEqual(stat.week_start, self.monday)
        self.assertEqual(stat.entries_count, self.this_week_entries)
        if stat.entries_count == 3:
            self.assertAlmostEqual(stat.mood_average, 7.3, places=1)
            self.assertEqual(len(stat.categories), 2)
            self.assertEqual(stat.categories.get("Travail"), 2)
            self.assertEqual(stat.categories.get("Sport"), 1)

    def test_weekly_stat_week_end(self):
        stat = WeeklyStat.objects.create(
            user=self.user,
            week_start=self.monday,
            entries_count=1,
            mood_average=7.0
        )
        self.assertEqual(stat.week_end(), self.monday + timedelta(days=6))

    def test_weekly_stat_week_number(self):
        stat = WeeklyStat.objects.create(
            user=self.user,
            week_start=self.monday,
            entries_count=1,
            mood_average=7.0
        )
        expected_week_number = self.monday.isocalendar()[1]
        self.assertEqual(stat.week_number(), expected_week_number)

    def test_weekly_stat_top_category(self):
        stat = WeeklyStat.objects.create(
            user=self.user,
            week_start=self.monday,
            entries_count=3,
            mood_average=7.0,
            categories={"Travail": 2, "Sport": 1}
        )
        self.assertEqual(stat.top_category(), "Travail")
        stat.categories = {"Loisirs": 3, "Travail": 2}
        stat.save()
        self.assertEqual(stat.top_category(), "Loisirs")
        stat.categories = {}
        stat.save()
        self.assertIsNone(stat.top_category())

    def test_daily_stat_with_no_entries(self):
        JournalEntry.objects.filter(user=self.user).delete()
        stat = DailyStat.generate_for_user(self.user, date=self.today)
        self.assertEqual(stat.entries_count, 0)
        self.assertIsNone(stat.mood_average)
        self.assertEqual(stat.categories, {})

    def test_weekly_stat_with_no_entries(self):
        JournalEntry.objects.filter(user=self.user).delete()
        stat, created = WeeklyStat.generate_for_user(self.user, reference_date=self.today)
        self.assertEqual(stat.entries_count, 0)
        self.assertIsNone(stat.mood_average)
        self.assertEqual(stat.categories, {})

    def test_daily_stat_update(self):
        initial_stat = DailyStat.generate_for_user(self.user, date=self.today)
        initial_count = initial_stat.entries_count
        JournalEntry.objects.create(
            user=self.user,
            content="Une entrée supplémentaire",
            category="Loisirs",
            mood=5,
            created_at=now()
        )
        updated_stat = DailyStat.generate_for_user(self.user, date=self.today)
        self.assertEqual(updated_stat.entries_count, initial_count + 1)
        self.assertIn("Loisirs", updated_stat.categories)

    def test_daily_stat_calendar_data_with_filters(self):
        DailyStat.generate_for_user(self.user, date=self.today)
        month_data = DailyStat.get_calendar_data(
            user=self.user,
            month=self.today.month,
            year=self.today.year
        )
        self.assertTrue(len(month_data) > 0)
        other_month = 1 if self.today.month != 1 else 2
        empty_data = DailyStat.get_calendar_data(
            user=self.user,
            month=other_month,
            year=self.today.year
        )
        self.assertEqual(len(empty_data), 0)
