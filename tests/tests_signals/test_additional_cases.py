# tests/tests_models/test_additional_cases.py

from django.test import TestCase
from django.utils.timezone import now
from django.conf import settings
from unittest.mock import patch, MagicMock

from Myevol_app.models.user_model import User
from Myevol_app.models.notification_model import Notification
from Myevol_app.models.quote_model import Quote
from Myevol_app.services.notification_service import create_admin_notification, create_user_notification, send_scheduled_notifications, archive_user_notifications

class AdditionalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="edgecaseuser",
            email="edgecase@example.com",
            password="testpass"
        )

    def test_create_admin_notification_without_admin_email(self):
        """Tester création notification admin sans DEFAULT_ADMIN_EMAIL"""
        with self.settings(DEFAULT_ADMIN_EMAIL=None):
            notif = create_admin_notification("Test admin message")
            self.assertIsNone(notif)

    def test_create_admin_notification_user_does_not_exist(self):
        """Tester création notification admin avec email inexistant"""
        with self.settings(DEFAULT_ADMIN_EMAIL="nonexistent@example.com"):
            notif = create_admin_notification("Test admin missing user")
            self.assertIsNone(notif)

    def test_create_user_notification_blocked_by_preferences(self):
        """Tester création de notification utilisateur bloquée par préférences"""
        # Simuler un utilisateur avec préférence de notification désactivée
        if hasattr(self.user, 'preferences'):
            self.user.preferences.notif_info = False
            self.user.preferences.save()

        notif = create_user_notification(self.user, "Info message", notif_type="info")
        self.assertIsNone(notif)

    def test_send_scheduled_notifications_empty(self):
        """Tester envoi de notifications programmées avec aucune notification"""
        count = send_scheduled_notifications()
        self.assertEqual(count, 0)

    def test_archive_user_notifications_none_existing(self):
        """Tester archivage avec aucune notification active"""
        count = archive_user_notifications(self.user)
        self.assertEqual(count, 0)

    def test_signal_quote_post_save_without_admin(self):
        """Tester signal Quote post_save sans admin configuré"""
        with self.settings(DEFAULT_ADMIN_EMAIL=None):
            quote = Quote.objects.create(text="Signal test quote", author="Tester")
            self.assertIsNotNone(quote)
            # Ici tu pourrais même vérifier que aucun Notification n'est créé (optionnel)

    @patch('Myevol_app.models.user_model.compute_mood_average', return_value=None)
    def test_user_mood_average_when_no_entries(self, mock_compute_mood):
        """Tester mood_average retourne None quand aucun journal"""
        mood = self.user.mood_average()
        self.assertIsNone(mood)
        mock_compute_mood.assert_called_once_with(self.user, 7, None)

    def test_create_preferences_when_deleted(self):
        """Tester recréation de préférences après suppression"""
        self.user.preferences.delete()
        from Myevol_app.services.userpreference_service import create_or_update_preferences
        prefs = create_or_update_preferences(self.user)
        self.assertIsNotNone(prefs)
        self.assertEqual(prefs.user, self.user)
