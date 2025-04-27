# tests/test_badge_model.py

from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.db import IntegrityError
from django.urls import reverse, NoReverseMatch
from Myevol_app.models.badge_model import Badge, BadgeTemplate
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

class BadgeModelTestCase(TestCase):
    """Tests pour le modèle Badge."""

    @patch('Myevol_app.models.user_model.User.create_default_preferences')
    def setUp(self, mock_create_prefs):
        mock_create_prefs.return_value = None
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        self.badge = Badge.objects.create(
            name="Test Badge",
            description="Description du badge",
            icon="🏆",
            user=self.user
        )

    def test_badge_creation(self):
        self.assertEqual(self.badge.name, "Test Badge")
        self.assertEqual(self.badge.user, self.user)
        self.assertEqual(self.badge.icon, "🏆")

    def test_was_earned_today(self):
        today = now().date()
        self.badge.date_obtenue = today
        self.badge.save()

        self.assertTrue(self.badge.was_earned_today())

        yesterday = today - timedelta(days=1)
        self.badge.date_obtenue = yesterday
        self.badge.save()

        self.assertFalse(self.badge.was_earned_today())

    @patch('Myevol_app.models.badge_model.reverse')
    def test_get_absolute_url(self, mock_reverse):
        mock_reverse.return_value = f"/badges/{self.badge.pk}/"
        url = self.badge.get_absolute_url()
        self.assertIn(str(self.badge.pk), url)

    def test_unique_together_constraint(self):
        with self.assertRaises(IntegrityError):
            Badge.objects.create(
                name="Test Badge",
                description="Another description",
                icon="🥇",
                user=self.user
            )

    def test_str_representation(self):
        self.assertIn("Test Badge", str(self.badge))

    def test_date_obtenue_auto_filled(self):
        self.assertIsNotNone(self.badge.date_obtenue)


class BadgeTemplateModelTestCase(TestCase):
    """Tests pour le modèle BadgeTemplate."""

    def setUp(self):
        # Utilisation d'un MagicMock pour remplacer un User
        self.user = MagicMock()
        self.user.username = "mockuser"
        self.user.badges.filter.return_value.exists.return_value = False

        self.template = BadgeTemplate.objects.create(
            name="Première entrée",
            description="Premier test badge",
            icon="🌟",
            condition="Faire sa première entrée"
        )

    def test_badge_template_creation(self):
        self.assertEqual(self.template.name, "Première entrée")
        self.assertEqual(self.template.icon, "🌟")

    def test_extract_level_number(self):
        self.assertEqual(BadgeTemplate(name="Niveau 5").extract_level_number(), 5)
        self.assertIsNone(BadgeTemplate(name="Pas un niveau").extract_level_number())

    def test_check_unlock_first_entry(self):
        self.user.total_entries.return_value = 1
        self.user.mood_average.return_value = None
        self.user.has_entries_every_day.return_value = False
        self.user.entries_today.return_value = 0
        self.user.all_objectives_achieved.return_value = False

        result = self.template.check_unlock(self.user)
        self.assertTrue(result)

    def test_check_unlock_failure(self):
        self.user.total_entries.return_value = 0
        self.user.mood_average.return_value = 5
        self.user.has_entries_every_day.return_value = False
        self.user.entries_today.return_value = 0
        self.user.all_objectives_achieved.return_value = False

        result = self.template.check_unlock(self.user)
        self.assertFalse(result)

    def test_get_progress_unlocked(self):
        self.user.total_entries.return_value = 1
        self.user.badges.filter.return_value.exists.return_value = True

        progress = self.template.get_progress(self.user)
        self.assertTrue(progress["unlocked"])
        self.assertEqual(progress["percent"], 100)

    def test_get_progress_locked(self):
        self.user.total_entries.return_value = 0
        self.user.badges.filter.return_value.exists.return_value = False

        progress = self.template.get_progress(self.user)
        self.assertFalse(progress["unlocked"])
        self.assertEqual(progress["percent"], 0)
