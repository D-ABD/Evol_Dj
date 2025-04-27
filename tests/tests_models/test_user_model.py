from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock, patch, PropertyMock

from Myevol_app.models import JournalEntry

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass"
        )

    def test_str_method(self):
        self.assertEqual(str(self.user), "testuser")
        
    def test_get_full_name(self):
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.save()
        self.assertEqual(self.user.get_full_name(), "Test User")
        
    def test_get_short_name(self):
        self.user.first_name = "Test"
        self.assertEqual(self.user.get_short_name(), "Test")

        self.user.first_name = ""
        self.user.save()
        self.assertEqual(self.user.get_short_name(), "testuser")
        
    def test_to_dict(self):
        with patch('Myevol_app.models.user_model.User.total_entries', new_callable=PropertyMock) as mock_entries, \
             patch('Myevol_app.models.user_model.User.current_streak', return_value=0), \
             patch('Myevol_app.models.user_model.User.mood_average', return_value=None), \
             patch('Myevol_app.models.user_model.User.level', return_value=0), \
             patch('Myevol_app.models.user_model.User.level_progress', return_value=0):

            mock_entries.return_value = 0
            user_dict = self.user.to_dict()

            self.assertEqual(user_dict["username"], "testuser")
            self.assertEqual(user_dict["email"], "test@example.com")

    def test_total_entries(self):
        JournalEntry.objects.create(user=self.user, content="Entry 1", mood=5, category="test")
        JournalEntry.objects.create(user=self.user, content="Entry 2", mood=7, category="test")
        self.assertEqual(self.user.total_entries, 2)

    @patch('Myevol_app.models.user_model.update_user_badges')
    def test_update_badges(self, mock_update_badges):
        self.user.update_badges()
        mock_update_badges.assert_called_once_with(self.user)

    @patch('Myevol_app.models.user_model.update_user_streak')
    def test_update_streaks(self, mock_update_streak):
        self.user.update_streaks()
        mock_update_streak.assert_called_once_with(self.user)

    def test_add_xp(self):
        self.assertEqual(self.user.xp, 0)
        self.user.add_xp(100)
        self.assertEqual(self.user.xp, 100)

        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.user.add_xp(-50)

    def test_entries_by_category(self):
        JournalEntry.objects.create(user=self.user, content="Entry 1", mood=5, category="work")
        JournalEntry.objects.create(user=self.user, content="Entry 2", mood=6, category="personal")
        entries = self.user.entries_by_category()
        self.assertIn("work", entries)
        self.assertIn("personal", entries)
        self.assertEqual(entries["work"], 1)
        self.assertEqual(entries["personal"], 1)

    from unittest.mock import patch

    @patch('django.db.models.signals.post_save.send')
    @patch.object(User, 'create_default_preferences')
    def test_save_triggers_create_default_preferences(self, mock_create_prefs, mock_post_save):
        user = User(username="saveuser", email="save@example.com")
        user.set_password("testpass")
        user.save()
        mock_create_prefs.assert_called_once()



    def test_has_entries_every_day(self):
        JournalEntry.objects.create(user=self.user, content="Entry 1", mood=7, category="test", created_at=now())
        JournalEntry.objects.create(user=self.user, content="Entry 2", mood=8, category="test", created_at=now())
        self.assertTrue(self.user.has_entries_every_day(1))

    def test_entries_today(self):
        JournalEntry.objects.create(user=self.user, content="Today's entry", mood=5, category="daily")
        self.assertEqual(self.user.entries_today(), 1)

    @patch('Myevol_app.models.user_model.compute_mood_average', return_value=7.5)
    def test_mood_average(self, mock_compute_mood):
        mood = self.user.mood_average()
        self.assertEqual(mood, 7.5)
        mock_compute_mood.assert_called_once_with(self.user, 7, None)

    @patch('Myevol_app.models.user_model.create_or_update_preferences')
    def test_create_default_preferences(self, mock_create_or_update):
        mock_create_or_update.return_value = MagicMock()  # simulate UserPreference object
        prefs = self.user.create_default_preferences()
        self.assertIsNotNone(prefs)
        mock_create_or_update.assert_called_once()

    @patch('Myevol_app.models.user_model.get_user_progress', return_value={'level': 2, 'progress': 50})
    def test_level_and_level_progress(self, mock_get_progress):
        level = self.user.level()
        progress = self.user.level_progress()
        self.assertEqual(level, 2)
        self.assertEqual(progress, 50)
        self.assertEqual(mock_get_progress.call_count, 2)

    @patch('Myevol_app.models.objective_model.Objective')
    def test_all_objectives_achieved(self, mock_objective):
        mock_objective.objects.filter.return_value.exists.return_value = False
        self.assertTrue(self.user.all_objectives_achieved())

    @patch('Myevol_app.models.user_model.compute_current_streak', return_value=5)
    def test_current_streak(self, mock_compute_streak):
        streak = self.user.current_streak()
        self.assertEqual(streak, 5)
        mock_compute_streak.assert_called_once_with(self.user, None)
