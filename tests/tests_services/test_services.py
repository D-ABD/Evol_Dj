from django.test import TestCase
from unittest.mock import patch, MagicMock
from Myevol_app.services import (
    badge_service, challenge_service, event_log_service, journal_service,
    levels_services, notification_service, quote_service, stats_service,
    streak_service, user_service, user_stats_service, userpreference_service
)

# Badge Service
class BadgeServiceTests(TestCase):
    @patch("Myevol_app.services.badge_service.EventLog")
    @patch("Myevol_app.services.badge_service.BadgeTemplate")
    @patch("Myevol_app.services.badge_service.Badge")
    def test_update_user_badges_creates_new_badge(self, mock_badge, mock_template, mock_eventlog):
        user = MagicMock(username="mockuser")
        user.badges.values_list.return_value = []
        template = MagicMock(name="Test Badge", icon="star.png", description="Test description", level=1)
        template.check_unlock.return_value = True
        mock_template.objects.all.return_value = [template]
        mock_created_badge = MagicMock()
        mock_badge.objects.create.return_value = mock_created_badge

        result = badge_service.update_user_badges(user, log_events=True, return_new_badges=True)

        mock_badge.objects.create.assert_called_once_with(
            user=user, name=template.name, icon=template.icon, description=template.description, level=template.level
        )
        mock_eventlog.objects.create.assert_called_once()
        self.assertIn(mock_created_badge, result)

# Challenge Service
class ChallengeServiceTests(TestCase):
    @patch("Myevol_app.services.challenge_service.update_challenge_progress")
    @patch("Myevol_app.services.challenge_service.ChallengeProgress.objects.get_or_create")
    @patch("Myevol_app.services.challenge_service.Challenge.objects.filter")
    def test_check_user_challenges(self, mock_filter, mock_get_or_create, mock_update_progress):
        user = MagicMock(username="mockuser")
        challenge = MagicMock(title="Mock Challenge")
        mock_filter.return_value = [challenge]
        progress = MagicMock()
        mock_get_or_create.return_value = (progress, False)

        challenge_service.check_user_challenges(user)

        mock_filter.assert_called_once()
        mock_get_or_create.assert_called_once_with(user=user, challenge=challenge)
        mock_update_progress.assert_called_once_with(progress)

    @patch("Myevol_app.services.challenge_service.check_user_challenges")
    def test_check_challenges(self, mock_check):
        user = MagicMock()
        challenge_service.check_challenges(user)
        mock_check.assert_called_once_with(user)

    @patch("Myevol_app.services.challenge_service.Notification.objects.create")
    def test_update_challenge_progress_completed(self, mock_notify):
        user = MagicMock()
        challenge = MagicMock(title="Challenge 1", is_completed=MagicMock(return_value=True))
        progress = MagicMock(user=user, challenge=challenge, completed=False)
        progress.save = MagicMock()

        challenge_service.update_challenge_progress(progress)

        self.assertTrue(progress.completed)
        self.assertIsNotNone(progress.completed_at)
        progress.save.assert_called_once()
        mock_notify.assert_called_once()

# Event Log Service
class EventLogServiceTests(TestCase):
    @patch("Myevol_app.services.event_log_service.logger")
    @patch("Myevol_app.services.event_log_service.EventLog.log_action")
    def test_log_event_success(self, mock_log_action, mock_logger):
        user = MagicMock()
        user.username = "testuser"

        mock_log_action.return_value = MagicMock()

        result = event_log_service.log_event(
            action="connexion",
            description="User connected",
            user=user,
            severity="INFO",
            extra="data"
        )

        mock_log_action.assert_called_once_with(
            action="connexion",
            description="User connected",
            user=user,
            severity="INFO",
            extra="data"
        )
        mock_logger.error.assert_not_called()
        self.assertEqual(result, mock_log_action.return_value)

    @patch("Myevol_app.services.event_log_service.logger")
    @patch("Myevol_app.services.event_log_service.EventLog.objects.create")
    def test_log_event_failure(self, mock_create, mock_logger):
        mock_create.side_effect = Exception("DB error")
        user = MagicMock(username="testuser")
        result = event_log_service.log_event(action="test", user=user)
        mock_logger.error.assert_called_once()
        self.assertIsNone(result)

    @patch("Myevol_app.services.event_log_service.EventLog.objects")
    def test_get_event_statistics(self, mock_eventlog):
        mock_queryset = MagicMock()
        mock_queryset.filter.return_value.values.return_value.annotate.return_value.values_list.return_value = [
            ('connexion', 5), ('deconnexion', 2)
        ]
        mock_eventlog.filter.return_value = mock_queryset.filter.return_value

        stats = event_log_service.get_event_statistics(days=7)
        self.assertEqual(stats, {'connexion': 5, 'deconnexion': 2})
        mock_eventlog.filter.assert_called_once()

# Journal Service
class JournalServiceTests(TestCase):
    @patch("Myevol_app.services.journal_service.JournalEntry.objects.create")
    def test_create_journal_entry(self, mock_create):
        user = MagicMock()
        mock_entry = MagicMock()
        mock_create.return_value = mock_entry

        result = journal_service.create_journal_entry(user, "Test content", 5, "Work")

        mock_create.assert_called_once_with(user=user, content="Test content", mood=5, category="Work")
        self.assertEqual(result, mock_entry)

    @patch("Myevol_app.services.journal_service.JournalEntry.get_entries_by_date_range")
    def test_get_journal_entries(self, mock_get_entries):
        user = MagicMock()
        mock_qs = MagicMock()
        mock_get_entries.return_value = mock_qs

        result = journal_service.get_journal_entries(user, "2023-01-01", "2023-01-31")
        mock_get_entries.assert_called_once_with(user, "2023-01-01", "2023-01-31")
        self.assertEqual(result, mock_qs)

# Level Service
class LevelServiceTests(TestCase):
    def test_get_user_level_and_progress(self):
        self.assertEqual(levels_services.get_user_level(0), 0)
        self.assertEqual(levels_services.get_user_progress(0)["level"], 0)
        self.assertEqual(levels_services.get_user_progress(30)["level"], 4)

# Notification Service
class NotificationServiceTests(TestCase):
    @patch("Myevol_app.services.notification_service.Notification.objects.create")
    def test_create_user_notification(self, mock_create):
        user = MagicMock()
        notification_service.create_user_notification(user, "Hello", "badge")
        mock_create.assert_called_once_with(user=user, message="Hello", notif_type="badge", scheduled_at=None)

    @patch("Myevol_app.services.notification_service.Notification.objects.filter")
    def test_send_scheduled_notifications(self, mock_filter):
        notif1, notif2 = MagicMock(), MagicMock()
        mock_filter.return_value = [notif1, notif2]
        notification_service.send_scheduled_notifications()
        notif1.mark_as_read.assert_called_once()
        notif2.mark_as_read.assert_called_once()

    @patch("Myevol_app.services.notification_service.Notification.objects.filter")
    def test_archive_user_notifications(self, mock_filter):
        user = MagicMock()
        mock_qs = MagicMock()
        mock_filter.return_value = mock_qs
        mock_qs.update.return_value = 3
        result = notification_service.archive_user_notifications(user)
        self.assertEqual(result, 3)

# Quote Service
class QuoteServiceTests(TestCase):
    @patch("Myevol_app.services.quote_service.Quote.objects.all")
    def test_get_random_quote(self, mock_all):
        mock_all.return_value.count.return_value = 1
        mock_all.return_value.__getitem__.return_value = "Quote"
        self.assertEqual(quote_service.get_random_quote(), "Quote")

    @patch("Myevol_app.services.quote_service.Quote.objects.all")
    def test_get_random_quote_empty(self, mock_all):
        mock_all.return_value.count.return_value = 0
        self.assertIsNone(quote_service.get_random_quote())

# Stats Service
    @patch("Myevol_app.services.stats_service.DailyStat.objects.update_or_create")
    def test_generate_daily_stats(self, mock_update):
        user = MagicMock()
        mock_stat = MagicMock()
        mock_update.return_value = (mock_stat, True)  # <-- Bien retourner 2 éléments
        result = stats_service.generate_daily_stats(user)
        self.assertIsNotNone(result)


    def test_compute_stats_for_period(self):
        user = MagicMock()
        user.entries.filter.return_value.count.return_value = 5
        user.entries.filter.return_value.aggregate.return_value = {'avg': 7}
        result = stats_service.compute_stats_for_period(user, "2024-01-01", "2024-01-31")
        self.assertEqual(result["entries_count"], 5)
        self.assertEqual(result["mood_average"], 7)

# Streak Service
class StreakServiceTests(TestCase):
    def test_update_user_streak(self):
        user = MagicMock(current_streak=MagicMock(return_value=10), longest_streak=5)
        streak_service.update_user_streak(user)
        self.assertEqual(user.longest_streak, 10)
        user.save.assert_called_once()

# User Service
class UserServiceTests(TestCase):
    @patch("Myevol_app.services.user_service.handle_user_badges")
    @patch("Myevol_app.services.user_service.handle_user_streak")
    @patch("Myevol_app.services.user_service.handle_user_preferences")
    def test_initialize_user_profile(self, mock_prefs, mock_streak, mock_badge):
        user = MagicMock()
        user_service.initialize_user_profile(user)
        mock_prefs.assert_called_once()
        mock_streak.assert_called_once()
        mock_badge.assert_called_once()

# User Stats Service
class UserStatsServiceTests(TestCase):
    def test_compute_mood_average_and_streak(self):
        user = MagicMock()
        user.entries.all.return_value.filter.return_value.aggregate.return_value = {'avg': 6.0}

        result = user_stats_service.compute_mood_average(user, days=7)

        self.assertEqual(result, 6.0)

# User Preference Service
class UserPreferenceServiceTests(TestCase):
    @patch("Myevol_app.services.userpreference_service.UserPreference.objects.get_or_create")
    def test_create_or_update_preferences(self, mock_get_or_create):
        user = MagicMock()
        prefs = MagicMock()
        mock_get_or_create.return_value = (prefs, True)
        result = userpreference_service.create_or_update_preferences(user, {"dark_mode": True})
        prefs.save.assert_called_once()
        self.assertEqual(result, prefs)

    @patch("Myevol_app.services.userpreference_service.get_object_or_404")
    def test_reset_preferences_to_defaults(self, mock_get):
        user = MagicMock()
        prefs = MagicMock()
        mock_get.return_value = prefs
        result = userpreference_service.reset_preferences_to_defaults(user)
        prefs.reset_to_defaults.assert_called_once()
        self.assertEqual(result, prefs)

    @patch("Myevol_app.services.challenge_service.update_challenge_progress")
    @patch("Myevol_app.services.challenge_service.ChallengeProgress.objects.get_or_create")
    @patch("Myevol_app.services.challenge_service.Challenge.objects.filter")
    def test_check_user_challenges_creates_progress(self, mock_filter, mock_get_or_create, mock_update_progress):
        user = MagicMock()
        challenge = MagicMock()
        mock_filter.return_value = [challenge]
        progress = MagicMock()
        mock_get_or_create.return_value = (progress, True)  # created = True

        challenge_service.check_user_challenges(user)

        mock_get_or_create.assert_called_once_with(user=user, challenge=challenge)
        mock_update_progress.assert_called_once_with(progress)

    @patch("Myevol_app.services.notification_service.Notification.objects.filter")
    def test_send_scheduled_notifications_none(self, mock_filter):
        mock_filter.return_value = []
        notification_service.send_scheduled_notifications()  # doit passer sans erreur

    @patch("Myevol_app.services.badge_service.Badge.objects.create")
    @patch("Myevol_app.services.badge_service.BadgeTemplate")
    @patch("Myevol_app.services.badge_service.EventLog")
    def test_update_user_badges_creation_failure(self, mock_eventlog, mock_template, mock_create_badge):
        user = MagicMock()
        template = MagicMock()
        template.check_unlock.return_value = True
        mock_template.objects.all.return_value = [template]
        mock_create_badge.side_effect = Exception("DB error")

        badges = badge_service.update_user_badges(user)

        self.assertEqual(badges, [])  # Doit retourner une liste vide
    @patch("Myevol_app.services.userpreference_service.get_object_or_404")
    def test_reset_preferences_user_not_found(self, mock_get):
        mock_get.side_effect = Exception("Not found")
        user = MagicMock()

        with self.assertRaises(Exception):
            userpreference_service.reset_preferences_to_defaults(user)
    def test_compute_stats_for_period_no_entries(self):
        user = MagicMock()
        user.entries.filter.return_value.count.return_value = 0
        user.entries.filter.return_value.aggregate.return_value = {'avg': None}

        stats = stats_service.compute_stats_for_period(user, "2024-01-01", "2024-01-31")

        self.assertEqual(stats["entries_count"], 0)
        self.assertIsNone(stats["mood_average"])
