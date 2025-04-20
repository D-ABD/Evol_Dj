from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.db.utils import IntegrityError

from ..models.challenge_model import check_challenges

from ..models import Challenge, ChallengeProgress
from ..models.journal_model import JournalEntry

User = get_user_model()

class ChallengeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.challenge = Challenge.objects.create(
            title="Défi Test",
            description="Faites 3 entrées en 3 jours",
            start_date=now().date() - timedelta(days=1),
            end_date=now().date() + timedelta(days=1),
            target_entries=3
        )

    def test_str_method(self):
        self.assertEqual(str(self.challenge), f"{self.challenge.title} ({self.challenge.start_date} → {self.challenge.end_date})")

    def test_is_active_true(self):
        self.assertTrue(self.challenge.is_active())

    def test_is_active_false(self):
        self.challenge.start_date = now().date() - timedelta(days=10)
        self.challenge.end_date = now().date() - timedelta(days=5)
        self.challenge.save()
        self.assertFalse(self.challenge.is_active())

    def test_days_remaining_positive(self):
        self.assertEqual(self.challenge.days_remaining(), 1)

    def test_days_remaining_zero(self):
        self.challenge.end_date = now().date() - timedelta(days=1)
        self.challenge.save()
        self.assertEqual(self.challenge.days_remaining(), 0)

    def test_is_completed_true(self):
        # Ajoute 3 entrées dans la période du défi
        for _ in range(3):
            JournalEntry.objects.create(user=self.user, mood=5, content="Progress", category="perso")
        self.assertTrue(self.challenge.is_completed(self.user))

    def test_is_completed_false(self):
        self.assertFalse(self.challenge.is_completed(self.user))

    def test_get_progress_partial(self):
        for _ in range(2):
            JournalEntry.objects.create(user=self.user, mood=5, content="Entry", category="perso")
        progress = self.challenge.get_progress(self.user)
        self.assertEqual(progress["current"], 2)
        self.assertEqual(progress["target"], 3)
        self.assertEqual(progress["percent"], 66)
        self.assertFalse(progress["completed"])

    def test_get_progress_complete(self):
        for _ in range(3):
            JournalEntry.objects.create(user=self.user, mood=5, content="Entry", category="perso")
        progress = self.challenge.get_progress(self.user)
        self.assertEqual(progress["percent"], 100)
        self.assertTrue(progress["completed"])


class ChallengeProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="progressuser", email="progress@example.com", password="testpass")
        self.challenge = Challenge.objects.create(
            title="Test Challenge",
            description="Faites 2 entrées",
            start_date=now().date() - timedelta(days=1),
            end_date=now().date() + timedelta(days=1),
            target_entries=2
        )
        self.progress = ChallengeProgress.objects.create(user=self.user, challenge=self.challenge)

    def test_str_method(self):
        self.assertEqual(str(self.progress), f"{self.user.username} → {self.challenge.title} (⏳)")

    def test_get_progress(self):
        JournalEntry.objects.create(user=self.user, mood=5, content="One", category="perso")
        result = self.progress.get_progress()
        self.assertEqual(result["current"], 1)
        self.assertFalse(result["completed"])


class ChallengeUtilsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usernotif", email="u@example.com", password="pass")
        self.challenge = Challenge.objects.create(
            title="Objectif 2 entrées",
            description="Fais 2 entrées en 3 jours",
            start_date=now().date() - timedelta(days=1),
            end_date=now().date() + timedelta(days=1),
            target_entries=2
        )

    @patch("Myevol_app.models.notification_model.Notification.objects.create")
    def test_check_challenges_marks_completed_and_notifies(self, mock_notif_create):
        for _ in range(2):
            JournalEntry.objects.create(user=self.user, mood=6, content="Done", category="perso")

        check_challenges(self.user)

        progress = ChallengeProgress.objects.get(user=self.user, challenge=self.challenge)
        self.assertTrue(progress.completed)
        self.assertIsNotNone(progress.completed_at)

        # ✅ Vérifie qu'une notification "défi terminé" a bien été envoyée
        messages = [call.kwargs["message"] for call in mock_notif_create.call_args_list]
        defi_messages = [msg for msg in messages if "Tu as terminé le défi" in msg]

        self.assertTrue(defi_messages, "Aucune notification de défi terminée n'a été envoyée.")



    @patch("Myevol_app.models.notification_model.Notification.objects.create")
    def test_multiple_challenges_completed(self, mock_notif_create):
        # Crée un 2e défi actif
        challenge2 = Challenge.objects.create(
            title="Objectif 1 entrée",
            description="Fais 1 entrée",
            start_date=now().date() - timedelta(days=1),
            end_date=now().date() + timedelta(days=1),
            target_entries=1
        )

        # Crée les entrées nécessaires
        JournalEntry.objects.create(user=self.user, mood=6, content="1", category="perso")
        JournalEntry.objects.create(user=self.user, mood=6, content="2", category="perso")

        check_challenges(self.user)

        # ✅ Filtrer uniquement les messages de type défi
        messages = [call.kwargs["message"] for call in mock_notif_create.call_args_list]
        defi_messages = [msg for msg in messages if "Tu as terminé le défi" in msg]

        self.assertEqual(len(defi_messages), 2)


    @patch("Myevol_app.models.notification_model.Notification.objects.create")
    def test_no_duplicate_notification(self, mock_notif_create):
        # Crée un défi, le complète une première fois
        for _ in range(2):
            JournalEntry.objects.create(user=self.user, mood=5, content="done", category="perso")
        check_challenges(self.user)

        # On relance le check une 2e fois, rien ne doit changer
        mock_notif_create.reset_mock()
        check_challenges(self.user)

        progress = ChallengeProgress.objects.get(user=self.user, challenge=self.challenge)
        self.assertTrue(progress.completed)
        mock_notif_create.assert_not_called()


    def test_future_challenge_is_not_active(self):
        future_challenge = Challenge.objects.create(
            title="Future Challenge",
            description="Starts tomorrow",
            start_date=now().date() + timedelta(days=1),
            end_date=now().date() + timedelta(days=3),
            target_entries=1
        )
        self.assertFalse(future_challenge.is_active())

    def test_progress_zero_if_no_entry_in_period(self):
        # ✅ Supprime toute entrée existante (au cas où d'autres tests ont pollué la DB)
        JournalEntry.objects.filter(user=self.user).delete()

        progress = self.challenge.get_progress(self.user)
        self.assertEqual(progress["current"], 0)
        self.assertEqual(progress["percent"], 0)
        self.assertFalse(progress["completed"])


    def test_unique_challenge_progress_constraint(self):
        # Première progression : OK
        ChallengeProgress.objects.create(user=self.user, challenge=self.challenge)
        
        # Deuxième progression identique : doit échouer
        with self.assertRaises(IntegrityError):
            ChallengeProgress.objects.create(user=self.user, challenge=self.challenge)

