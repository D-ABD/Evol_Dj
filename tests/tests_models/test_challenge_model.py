from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from unittest.mock import patch

from Myevol_app.models import Challenge, ChallengeProgress, JournalEntry

User = get_user_model()

class ChallengeModelTests(TestCase):

    @patch('Myevol_app.models.user_model.User.create_default_preferences')
    def setUp(self, mock_create_prefs):
        mock_create_prefs.return_value = None

        self.user = User.objects.create_user(
            username="challengeuser",
            email="challenge@example.com",
            password="testpass"
        )

        today = now().date()
        self.challenge = Challenge.objects.create(
            title="Défi actif",
            description="Un défi actif pour tester",
            start_date=today - timedelta(days=2),
            end_date=today + timedelta(days=5),
            target_entries=3
        )

        self.future_challenge = Challenge.objects.create(
            title="Défi futur",
            description="Un défi futur",
            start_date=today + timedelta(days=2),
            end_date=today + timedelta(days=10),
            target_entries=5
        )

        self.past_challenge = Challenge.objects.create(
            title="Défi passé",
            description="Un défi passé",
            start_date=today - timedelta(days=10),
            end_date=today - timedelta(days=2),
            target_entries=2
        )

        self.progress = ChallengeProgress.objects.create(
            user=self.user,
            challenge=self.challenge
        )

    def test_str_method(self):
        self.assertEqual(str(self.challenge), "Défi actif")

    def test_is_active(self):
        self.assertTrue(self.challenge.is_active)
        self.assertFalse(self.future_challenge.is_active)
        self.assertFalse(self.past_challenge.is_active)

    def test_days_remaining(self):
        expected_days = (self.challenge.end_date - now().date()).days
        self.assertEqual(self.challenge.days_remaining, expected_days)
        self.assertEqual(self.past_challenge.days_remaining, 0)

    def test_participants_count(self):
        self.assertEqual(self.challenge.participants_count, 1)
        self.assertEqual(self.future_challenge.participants_count, 0)

        with patch('Myevol_app.models.user_model.User.create_default_preferences'):
            other_user = User.objects.create_user(
                username="otheruser",
                email="other@example.com",
                password="testpass"
            )

        ChallengeProgress.objects.create(
            user=other_user,
            challenge=self.challenge
        )
        self.assertEqual(self.challenge.participants_count, 2)

    @patch('Myevol_app.services.user_stats_service.compute_current_streak')
    @patch('Myevol_app.models.stats_model.DailyStat.generate_for_user')
    @patch('Myevol_app.services.challenge_service.check_challenges')
    @patch('Myevol_app.models.user_model.User.update_badges')
    @patch('Myevol_app.models.user_model.User.update_streaks')
    def test_is_completed(self, mock_update_streaks, mock_update_badges, mock_check_challenges, mock_generate_stats, mock_compute_streak):
        mock_compute_streak.return_value = 0

        self.assertFalse(self.challenge.is_completed(self.user))

        for i in range(3):
            JournalEntry.objects.create(
                user=self.user,
                content=f"Entry {i}",
                mood=7,
                category="challenge"
            )

        self.assertTrue(self.challenge.is_completed(self.user))

    @patch('Myevol_app.services.user_stats_service.compute_current_streak')
    @patch('Myevol_app.models.stats_model.DailyStat.generate_for_user')
    @patch('Myevol_app.services.challenge_service.check_challenges')
    @patch('Myevol_app.models.user_model.User.update_badges')
    @patch('Myevol_app.models.user_model.User.update_streaks')
    def test_get_progress(self, mock_update_streaks, mock_update_badges, mock_check_challenges, mock_generate_stats, mock_compute_streak):
        mock_compute_streak.return_value = 0

        progress = self.challenge.get_progress(self.user)
        self.assertEqual(progress['percent'], 0)
        self.assertFalse(progress['completed'])

        for i in range(2):
            JournalEntry.objects.create(
                user=self.user,
                content=f"Entry {i}",
                mood=7,
                category="challenge"
            )

        progress = self.challenge.get_progress(self.user)
        self.assertEqual(progress['percent'], 66)
        self.assertFalse(progress['completed'])

        JournalEntry.objects.create(
            user=self.user,
            content="Final Entry",
            mood=8,
            category="challenge"
        )

        progress = self.challenge.get_progress(self.user)
        self.assertEqual(progress['percent'], 100)
        self.assertTrue(progress['completed'])

    @patch('Myevol_app.models.challenge_model.reverse')
    def test_get_absolute_url(self, mock_reverse):
        mock_reverse.return_value = f"/challenges/{self.challenge.pk}/"
        url = self.challenge.get_absolute_url()
        self.assertIn(str(self.challenge.pk), url)


class ChallengeProgressTests(TestCase):

    @patch('Myevol_app.models.user_model.User.create_default_preferences')
    def setUp(self, mock_create_prefs):
        mock_create_prefs.return_value = None

        self.user = User.objects.create_user(
            username="progressuser",
            email="progress@example.com",
            password="testpass"
        )

        today = now().date()
        self.challenge = Challenge.objects.create(
            title="Test Challenge",
            description="Description",
            start_date=today - timedelta(days=1),
            end_date=today + timedelta(days=6),
            target_entries=3
        )

        self.progress = ChallengeProgress.objects.create(
            user=self.user,
            challenge=self.challenge
        )

    def test_str_method(self):
        expected = f"{self.user.username} - {self.challenge.title}"
        self.assertEqual(str(self.progress), expected)

    @patch('Myevol_app.services.user_stats_service.compute_current_streak')
    @patch('Myevol_app.models.stats_model.DailyStat.generate_for_user')
    @patch('Myevol_app.services.challenge_service.check_challenges')
    @patch('Myevol_app.models.user_model.User.update_badges')
    @patch('Myevol_app.models.user_model.User.update_streaks')
    def test_get_progress(self, mock_update_streaks, mock_update_badges, mock_check_challenges, mock_generate_stats, mock_compute_streak):
        mock_compute_streak.return_value = 0

        progress = self.progress.get_progress()
        self.assertEqual(progress['percent'], 0)
        self.assertFalse(progress['completed'])

        for i in range(2):
            JournalEntry.objects.create(
                user=self.user,
                content=f"Entry {i}",
                mood=7,
                category="test"
            )

        progress = self.progress.get_progress()
        self.assertEqual(progress['percent'], 66)

    @patch('Myevol_app.models.challenge_model.reverse')
    def test_get_absolute_url(self, mock_reverse):
        mock_reverse.return_value = f"/challenge-progress/{self.progress.pk}/"
        url = self.progress.get_absolute_url()
        self.assertIn(str(self.progress.pk), url)
