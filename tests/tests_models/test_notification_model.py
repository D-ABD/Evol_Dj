# tests/tests_models/test_notification_model.py
from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from unittest.mock import patch

from Myevol_app.models import Notification

User = get_user_model()

class NotificationModelTests(TestCase):
    @patch('Myevol_app.models.user_model.User.create_default_preferences')
    def setUp(self, mock_create_prefs):
        # Empêche la création des préférences utilisateur
        mock_create_prefs.return_value = None
        
        self.user = User.objects.create_user(
            username="notifuser",
            email="notif@example.com",
            password="testpass"
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message="Test notification",
            notif_type="info"
        )
        
    def test_str_method(self):
        expected = f"{self.user.username} - Test notification"
        self.assertEqual(str(self.notification)[:len(expected)], expected)
        
    def test_type_display(self):
        self.assertEqual(self.notification.type_display, "Information générale")
        
        # Changer le type et tester à nouveau
        self.notification.notif_type = "badge"
        self.notification.save()
        self.assertEqual(self.notification.type_display, "Badge débloqué")
        
    def test_archive(self):
        self.assertFalse(self.notification.archived)
        self.notification.archive()
        self.assertTrue(self.notification.archived)
        
    def test_mark_as_read(self):
        self.assertFalse(self.notification.is_read)
        self.assertIsNone(self.notification.read_at)
        
        self.notification.mark_as_read()
        
        self.assertTrue(self.notification.is_read)
        self.assertIsNotNone(self.notification.read_at)
        
    def test_mark_all_as_read(self):
        # Créer quelques notifications supplémentaires
        Notification.objects.create(user=self.user, message="Another notification", notif_type="info")
        Notification.objects.create(user=self.user, message="Badge notification", notif_type="badge")
        
        # Compter combien de notifications sont non lues avant
        unread_before = Notification.objects.filter(user=self.user, is_read=False).count()

        # Marquer toutes comme lues
        count = Notification.mark_all_as_read(self.user)

        # Le nombre retourné doit correspondre aux notifications non lues initialement
        self.assertEqual(count, unread_before)

        # Vérifier que toutes les notifications sont bien marquées comme lues
        for notif in Notification.objects.filter(user=self.user):
            self.assertTrue(notif.is_read)
            self.assertIsNotNone(notif.read_at)

            
    def test_create_notification(self):
        new_notif = Notification.create_notification(
            user=self.user,
            message="New notification",
            notif_type="objectif",
            scheduled_at=now()
        )
        
        self.assertEqual(new_notif.user, self.user)
        self.assertEqual(new_notif.message, "New notification")
        self.assertEqual(new_notif.notif_type, "objectif")
        self.assertIsNotNone(new_notif.scheduled_at)