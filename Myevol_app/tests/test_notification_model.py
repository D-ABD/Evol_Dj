from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from ..models.notification_model import Notification
from ..signals import limit_notifications

User = get_user_model()

class NotificationModelTests(TestCase):
    def setUp(self):
        # Désactiver le signal qui limite à 100 notifs
        post_save.disconnect(receiver=limit_notifications, sender=Notification)
        Notification.objects.all().delete()
        self.user = User.objects.create_user(username="notifuser", password="pass")

    def tearDown(self):
        # Réactiver le signal
        post_save.connect(receiver=limit_notifications, sender=Notification)

    def _create_notif(self, **kwargs):
        data = {
            "user": self.user,
            "message": "Test",
            "is_read": False,
            "archived": False,
            "notif_type": "info"
        }
        data.update(kwargs)
        return Notification.objects.create(**data)

    def test_str_method(self):
        notif = self._create_notif(message="Salut le monde")
        self.assertIn(self.user.username, str(notif))
        self.assertIn("Salut", str(notif))

    def test_type_display(self):
        notif = self._create_notif(notif_type="badge")
        self.assertEqual(notif.type_display, "Badge débloqué")

    def test_mark_as_read(self):
        notif = self._create_notif()
        notif.mark_as_read()
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
        self.assertIsNotNone(notif.read_at)

    def test_archive(self):
        notif = self._create_notif()
        notif.archive()
        notif.refresh_from_db()
        self.assertTrue(notif.archived)

    def test_get_unread(self):
        notif = self._create_notif()
        unread = Notification.get_unread(self.user)
        self.assertIn(notif, unread)

    def test_mark_all_as_read(self):
        n1 = self._create_notif(is_read=False)
        n2 = self._create_notif(is_read=True)
        count = Notification.mark_all_as_read(self.user)
        self.assertEqual(count, 1)
        n1.refresh_from_db()
        self.assertTrue(n1.is_read)

    def test_get_inbox(self):
        notif = self._create_notif()
        inbox = Notification.get_inbox(self.user)
        self.assertIn(notif, inbox)

    def test_get_archived(self):
        notif = self._create_notif(archived=True)
        archived = Notification.get_archived(self.user)
        self.assertIn(notif, archived)

    def test_mark_as_read_sets_flags(self):
        notif = self._create_notif()
        notif.mark_as_read()
        self.assertTrue(notif.is_read)
        self.assertIsNotNone(notif.read_at)

    def test_archive_sets_flag(self):
        notif = self._create_notif()
        notif.archive()
        self.assertTrue(notif.archived)

    def test_get_archived_returns_only_archived(self):
        a = self._create_notif(archived=True)
        b = self._create_notif(archived=False)
        archived = Notification.get_archived(self.user)
        self.assertIn(a, archived)
        self.assertNotIn(b, archived)

    def test_create_notification_method(self):
        notif = Notification.create_notification(
            user=self.user,
            message="Message test",
            notif_type="info"
        )
        self.assertTrue(Notification.objects.filter(id=notif.id).exists())

    def test_type_display_returns_readable_label(self):
        notif = self._create_notif(notif_type="statistique")
        self.assertEqual(notif.type_display, "Statistique")

    def test_mark_all_as_read_marks_all(self):
        n1 = self._create_notif(is_read=False)
        n2 = self._create_notif(is_read=False)
        self._create_notif(is_read=True)
        self._create_notif(archived=True, is_read=False)

        count = Notification.mark_all_as_read(self.user)
        self.assertEqual(count, 2)
        self.assertTrue(Notification.objects.get(id=n1.id).is_read)
        self.assertTrue(Notification.objects.get(id=n2.id).is_read)
        self.assertEqual(Notification.get_unread(self.user).count(), 0)

    def test_get_notification_count(self):
        self._create_notif(is_read=False, archived=False)  # Non lue
        self._create_notif(is_read=True, archived=False)   # Lue
        self._create_notif(is_read=False, archived=True)   # Archivée

        counts = Notification.get_notification_count(self.user)
        print("COUNTS:", counts)
        self.assertEqual(counts["unread"], 1)
        self.assertEqual(counts["total"], 2)
        self.assertEqual(counts["archived"], 1)
