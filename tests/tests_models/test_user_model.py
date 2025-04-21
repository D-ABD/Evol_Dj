from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.utils.timezone import make_aware
from datetime import datetime
from ..models.journal_model import JournalEntry
from freezegun import freeze_time

UserModel = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="john",
            email="john@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            xp=0,
        )

    def test_str_method(self):
        self.assertEqual(str(self.user), "john")

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "John Doe")

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "John")

    def test_to_dict_contains_basic_fields(self):
        data = self.user.to_dict()
        self.assertEqual(data['username'], "john")
        self.assertIn('mood_average', data)
        self.assertIn('current_streak', data)

    def test_add_xp_increases_xp(self):
        self.user.add_xp(20)
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp, 20)

    def test_level_property(self):
        self.assertGreaterEqual(self.user.level, 1)

    def test_get_dashboard_data_structure(self):
        dashboard = self.user.get_dashboard_data()
        self.assertIn("total_entries", dashboard)
        self.assertIn("badges", dashboard)
        self.assertIn("objectives", dashboard)

    def test_entries_today_initial(self):
        self.assertEqual(self.user.entries_today(), 0)

    def test_all_objectives_achieved_with_none(self):
        self.assertTrue(self.user.all_objectives_achieved())

    @patch("Myevol_app.models.user_model.update_user_badges")
    def test_update_badges_calls_service(self, mock_update):
        self.user.update_badges()
        mock_update.assert_called_once_with(self.user)

    @patch("Myevol_app.models.user_model.update_user_streak")
    def test_update_streaks_calls_service(self, mock_update_streak):
        self.user.update_streaks()
        mock_update_streak.assert_called_once_with(self.user)

    @patch("Myevol_app.models.user_model.create_preferences_for_user")
    def test_create_default_preferences_calls_service(self, mock_pref_create):
        mock_pref = MagicMock()
        mock_pref_create.return_value = mock_pref
        pref = self.user.create_default_preferences()
        mock_pref_create.assert_called_once_with(self.user)
        self.assertEqual(pref, mock_pref)



class UserEntryStatsTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password",
        )

        # Crée 5 entrées : une par jour dans les 5 derniers jours
        for i in range(5):
            fake_day = now().date() - timedelta(days=i)
            with freeze_time(fake_day):
                JournalEntry.objects.create(
                    user=self.user,
                    mood=5 + i,
                    category="pro",
                    content=f"Jour {i + 1}",
                )

    def test_total_entries(self):
        self.assertEqual(self.user.total_entries(), 5)

    def test_current_streak(self):
        self.assertEqual(self.user.current_streak(), 5)

    def test_mood_average(self):
        average = self.user.mood_average(days=5)
        self.assertAlmostEqual(average, 7.0)

    def test_entries_today(self):
        self.assertEqual(self.user.entries_today(), 1)

    def test_has_entries_every_day_true(self):
        self.assertTrue(self.user.has_entries_every_day(5))

    def test_entries_per_day(self):
        data = self.user.entries_per_day(n=5)
        self.assertEqual(len(data), 5)
        for count in data.values():
            self.assertEqual(count, 1)

    def test_mood_trend(self):
        trend = self.user.mood_trend(n=5)
        self.assertEqual(len(trend), 5)
        self.assertIn(7.0, trend.values())

    def test_days_with_entries(self):
        days = self.user.days_with_entries(n=5)
        self.assertEqual(len(days), 5)

    def test_entries_by_category(self):
        by_cat = self.user.entries_by_category(days=5)
        self.assertEqual(by_cat.get("pro"), 5)
