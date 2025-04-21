from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from unittest.mock import patch
from datetime import timedelta
from django.db import IntegrityError

from ..utils.levels import get_user_progress

from ..models import Badge, BadgeTemplate
from ..models.journal_model import JournalEntry

User = get_user_model()

LEVEL_THRESHOLDS = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]

class BadgeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass"
        )

    def test_str_method(self):
        badge = Badge.objects.create(
            user=self.user,
            name="Niveau 1",
            description="Test",
            icon="🥇"
        )
        self.assertEqual(str(badge), "Niveau 1 (testuser)")

    def test_was_earned_today_true(self):
        badge = Badge.objects.create(
            user=self.user,
            name="Today Badge",
            description="Test",
            icon="🎉"
        )
        self.assertTrue(badge.was_earned_today())

    def test_was_earned_today_false(self):
        yesterday = now().date() - timedelta(days=1)
        badge = Badge.objects.create(
            user=self.user,
            name="Old Badge",
            description="Test",
            icon="🎖️"
        )
        badge.date_obtenue = yesterday
        badge.save()
        self.assertFalse(badge.was_earned_today())

    @patch("Myevol_app.models.notification_model.Notification.objects.create")
    @patch("Myevol_app.models.event_log_model.EventLog.objects.create")
    def test_save_creates_notification_and_log(self, mock_eventlog_create, mock_notification_create):
        badge = Badge(
            user=self.user,
            name="Test Badge",
            description="Description",
            icon="🔥"
        )
        badge.save()

        mock_notification_create.assert_called_once()
        mock_eventlog_create.assert_called_once()


class BadgeTemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="templateuser",
            email="template@example.com",
            password="testpass"
        )
        self.template = BadgeTemplate.objects.create(
            name="Première entrée",
            description="Tu as fait ta première entrée",
            icon="✨",
            condition="1 entrée",
            level=1
        )

    def test_str_method(self):
        self.assertEqual(str(self.template), "Première entrée")

    def test_check_unlock_true(self):
        JournalEntry.objects.create(user=self.user, mood=5, content="Hello", category="perso")
        self.assertTrue(self.template.check_unlock(self.user))

    def test_check_unlock_false(self):
        self.assertFalse(self.template.check_unlock(self.user))

    def test_get_progress_unlocked(self):
        # On simule l’obtention du badge
        Badge.objects.create(user=self.user, name="Première entrée", description="Test", icon="🎉")
        progress = self.template.get_progress(self.user)
        self.assertTrue(progress["unlocked"])
        self.assertEqual(progress["percent"], 100)

    def test_get_progress_not_unlocked(self):
        progress = self.template.get_progress(self.user)
        self.assertFalse(progress["unlocked"])
        self.assertEqual(progress["percent"], 0)
        self.assertEqual(progress["target"], 1)


    def test_unique_constraint_per_user(self):
        Badge.objects.create(
            user=self.user,
            name="Unique Badge",
            description="Premier badge",
            icon="🏆"
        )

        with self.assertRaises(IntegrityError):
            Badge.objects.create(
                user=self.user,
                name="Unique Badge",  # Même nom
                description="Deuxième badge",
                icon="🏅"
            )
    def test_level_condition(self):
        # Crée 40 entrées pour atteindre le niveau 5
        for i in range(40):
            JournalEntry.objects.create(user=self.user, mood=6, category="perso", content=f"Entry {i}")

        # Crée un badge template de type "Niveau 5"
        level_template = BadgeTemplate.objects.create(
            name="Niveau 5",
            description="Tu as atteint le niveau 5",
            icon="🏅",
            condition="Atteindre 35 entrées",
            level=5
        )

        self.assertTrue(level_template.check_unlock(self.user))

    def test_get_progress_for_level_5(self):
        for i in range(40):
            JournalEntry.objects.create(user=self.user, mood=6, category="perso", content=f"Entry {i}")
        
        badge_template = BadgeTemplate.objects.create(
            name="Niveau 5",
            description="Tu as atteint le niveau 5",
            icon="🏅",
            condition="Atteindre 35 entrées",
            level=5
        )

        progress = badge_template.get_progress(self.user)
        expected_target = get_user_progress(40)["next_threshold"]

        self.assertTrue(progress["unlocked"])
        self.assertEqual(progress["percent"], 100)
        self.assertEqual(progress["target"], expected_target)
        self.assertEqual(progress["current"], 40)