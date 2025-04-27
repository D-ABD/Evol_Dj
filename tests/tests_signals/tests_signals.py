from django.test import TransactionTestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from Myevol_app.models import Badge, Objective, Notification, UserPreference, JournalEntry
from django.utils import timezone
import datetime

User = get_user_model()

class SignalTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")

    @patch("Myevol_app.signals.badge_signals.create_user_notification")
    def test_badge_creation_triggers_notification(self, mock_create_notification):
        """Test que la création d'un badge déclenche une notification."""
        badge = Badge.objects.create(
            user=self.user,
            name="Test Badge",
            description="Test badge description",
            icon="🏆"
        )

        mock_create_notification.assert_called_once()
        call_args = mock_create_notification.call_args[1]
        self.assertEqual(call_args["user"], self.user)
        self.assertEqual(call_args["notif_type"], "badge")
        self.assertIn("Test Badge", call_args["message"])

    def test_objective_completion_notification(self):
        """Test qu'une notification est créée quand un objectif est marqué comme complété."""
        objective = Objective.objects.create(
            user=self.user,
            title="Pending Objective",
            category="test",
            done=False,
            target_date=timezone.now().date() + datetime.timedelta(days=7),
            target_value=1
        )

        # Marquer comme complété
        objective.done = True
        objective.save()

        notif = Notification.objects.filter(
            user=self.user,
            notif_type="objectif",
            message__icontains="Pending Objective"
        ).first()

        self.assertIsNotNone(notif, "Aucune notification créée pour l'objectif complété")

    def test_userpreference_triggers_badge_update(self):
        """Test que la modification des préférences utilisateur déclenche la mise à jour des badges."""
        special_user = User.objects.create_user(username="pref_test_user", email="pref_test@example.com", password="testpass")
        prefs = UserPreference.objects.get(user=special_user)

        # Patcher update_badges sur cet utilisateur spécifique
        with patch.object(special_user, "update_badges") as mock_update_badges:
            prefs.user = special_user  # S'assurer que c'est bien notre user mocké
            prefs.dark_mode = not prefs.dark_mode
            prefs.save()

            mock_update_badges.assert_called_once()

# tests/tests_signals/tests_signals.py

    # Journal Signal - Vérifie la mise à jour des défis quand une entrée de journal est créée
    @patch("Myevol_app.signals.journal_signals.check_challenges")
    def test_journal_entry_triggers_challenge_check(self, mock_check_challenges):
        entry = JournalEntry.objects.create(
            user=self.user,
            content="Test entry",
            mood=7,
            category="Work"
        )
        mock_check_challenges.assert_called_once_with(self.user)

    # Stats Signal - Vérifie que la création d'une entrée de journal génère des stats
    @patch("Myevol_app.signals.stats_signals.generate_daily_stats")
    @patch("Myevol_app.signals.stats_signals.generate_weekly_stats")
    @patch("Myevol_app.signals.stats_signals.generate_monthly_stats")
    @patch("Myevol_app.signals.stats_signals.generate_annual_stats")
    def test_journal_entry_triggers_stats_update(self, mock_annual, mock_monthly, mock_weekly, mock_daily):
        JournalEntry.objects.create(
            user=self.user,
            content="Another test entry",
            mood=8,
            category="Personal"
        )
        mock_daily.assert_called_once_with(self.user)
        mock_weekly.assert_called_once_with(self.user)
        mock_monthly.assert_called_once_with(self.user)
        mock_annual.assert_called_once_with(self.user)

    # User Signal - Vérifie que la création d'un utilisateur initialise son profil
    @patch("Myevol_app.signals.user_signals.handle_user_streak")
    @patch("Myevol_app.signals.user_signals.handle_user_badges")
    @patch("Myevol_app.signals.user_signals.handle_user_preferences")
    def test_user_creation_initializes_profile(self, mock_preferences, mock_badges, mock_streak):
        """
        Test que la création d'un utilisateur appelle bien
        l'initialisation des préférences, badges et streaks.
        """
        user = User.objects.create_user(username="newuser", email="new@example.com", password="password123")

        mock_preferences.assert_called_once_with(user)
        mock_badges.assert_called_once_with(user)
        mock_streak.assert_called_once_with(user)

    # Event Log Signal - Vérifie que log_event fonctionne bien même sans utilisateur
    @patch("Myevol_app.services.event_log_service.EventLog.log_action")
    def test_log_event_without_user(self, mock_log_action):
        from Myevol_app.services.event_log_service import log_event
        result = log_event(action="test_action", description="No user provided")
        mock_log_action.assert_called_once_with(
            action="test_action",
            description="No user provided",
            user=None,
            severity="INFO"
        )
        self.assertIsNotNone(result)

    # Quote Signal (optionnel) - Teste que get_daily_quote() ne crash pas si vide
    @patch("Myevol_app.models.quote_model.Quote.objects.all")
    def test_quote_daily_no_crash_if_empty(self, mock_all):
        mock_all.return_value.count.return_value = 0
        from Myevol_app.services import quote_service
        quote = quote_service.get_daily_quote()
        self.assertIsNone(quote)
