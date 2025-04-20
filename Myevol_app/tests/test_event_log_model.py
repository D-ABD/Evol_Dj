from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model

from ..models.event_log_model import EventLog

User = get_user_model()


class EventLogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="loguser", email="log@example.com", password="pass")

    def test_str_method(self):
        log = EventLog.objects.create(action="connexion", description="Connexion réussie", user=self.user)
        expected_str = f"{log.created_at:%Y-%m-%d %H:%M} - connexion"
        self.assertEqual(str(log), expected_str)

    def test_log_creation_with_user(self):
        log = EventLog.objects.create(action="test_action", description="Test", user=self.user)
        self.assertEqual(log.action, "test_action")
        self.assertEqual(log.user, self.user)

    def test_log_creation_without_user(self):
        log = EventLog.objects.create(action="system_event", description="Système", user=None)
        self.assertIsNone(log.user)
        self.assertEqual(log.action, "system_event")

    def test_log_action_utility_method(self):
        log = EventLog.log_action(
            action="badge_unlocked",
            description="Badge 'Niveau 1' attribué",
            user=self.user,
            extra_info="test",
            level=1
        )
        self.assertEqual(log.action, "badge_unlocked")
        self.assertEqual(log.user, self.user)
        self.assertIn("level", log.metadata)
        self.assertEqual(log.metadata["level"], 1)

    def test_get_action_counts_global(self):
        EventLog.objects.create(action="a", user=self.user)
        EventLog.objects.create(action="a", user=self.user)
        EventLog.objects.create(action="b", user=self.user)

        stats = EventLog.get_action_counts(days=1)
        self.assertEqual(stats["a"], 2)
        self.assertEqual(stats["b"], 1)

    def test_get_action_counts_filtered_by_user(self):
        other_user = User.objects.create_user(username="other", email="o@example.com", password="pass")
        EventLog.objects.create(action="a", user=self.user)
        EventLog.objects.create(action="a", user=other_user)
        EventLog.objects.create(action="a", user=other_user)

        stats = EventLog.get_action_counts(days=1, user=self.user)
        self.assertEqual(stats, {"a": 1})

    def test_get_action_counts_outside_range(self):
        old_date = now() - timedelta(days=60)
        log = EventLog.objects.create(action="x", user=self.user)
        # ⚠️ Mise à jour forcée de created_at
        EventLog.objects.filter(id=log.id).update(created_at=old_date)

        stats = EventLog.get_action_counts(days=30)
        self.assertEqual(stats, {})  # vide car trop ancien

    def test_log_action_with_metadata(self):
        metadata = {"source": "test", "ip": "127.0.0.1"}
        log = EventLog.log_action("test_action", "Test desc", user=self.user, **metadata)
        self.assertEqual(log.metadata["source"], "test")
        self.assertEqual(log.metadata["ip"], "127.0.0.1")

    def test_log_action_without_user(self):
        log = EventLog.log_action("system_action", "Système")
        self.assertIsNone(log.user)


