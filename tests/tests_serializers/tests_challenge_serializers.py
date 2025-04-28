from django.test import TestCase
from django.utils import timezone
from Myevol_app.models.challenge_model import Challenge, ChallengeProgress
from Myevol_app.models.user_model import User
from Myevol_app.serializers.challenge_serializers import (
    ChallengeSerializer,
    ChallengeProgressSerializer,
    ChallengeDetailSerializer
)

class ChallengeSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.challenge = Challenge.objects.create(
            title="7 jours d'écriture",
            description="Écrire chaque jour pendant 7 jours",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=7),
            target_entries=7
        )
        self.progress = ChallengeProgress.objects.create(
            user=self.user,
            challenge=self.challenge,
            completed=False
        )

    def test_challenge_serializer_fields(self):
        serializer = ChallengeSerializer(instance=self.challenge)
        data = serializer.data

        self.assertEqual(data["title"], "7 jours d'écriture")
        self.assertIn("is_active", data)
        self.assertIn("participants_count", data)

    def test_challenge_progress_serializer_fields(self):
        serializer = ChallengeProgressSerializer(instance=self.progress)
        data = serializer.data

        self.assertEqual(data["challenge_title"], "7 jours d'écriture")
        self.assertIn("progress", data)

    def test_challenge_detail_serializer_fields(self):
        serializer = ChallengeDetailSerializer(instance=self.challenge, context={'request': None})
        data = serializer.data

        self.assertIn("user_progress", data)
        self.assertIn("joined", data)

    def test_challenge_progress_serializer_missing_challenge(self):
        """Teste que ChallengeProgressSerializer refuse une progression sans challenge lié."""
        invalid_data = {
            'user': self.user.id,
        }
        serializer = ChallengeProgressSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('challenge', serializer.errors)
