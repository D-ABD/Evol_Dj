from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tests.tests_viewsets.factories import (
    ChallengeFactory,
    ChallengeProgressFactory,
    UserFactory
)

class ChallengeViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.challenge = ChallengeFactory()

    def test_list_challenges(self):
        url = reverse("challenge-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_challenge(self):
        url = reverse("challenge-detail", args=[self.challenge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.challenge.id)

    def test_active_challenges(self):
        active = ChallengeFactory(title="Actif", start_date="2025-01-01", end_date="2030-01-01")
        ChallengeFactory(title="Inactif", start_date="2020-01-01", end_date="2021-01-01")
        url = reverse("challenge-active-challenges")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [c["title"] for c in response.data]
        self.assertIn("Actif", titles)
        self.assertNotIn("Inactif", titles)

    def test_challenge_participants(self):
        challenge = ChallengeFactory()
        ChallengeProgressFactory(user=self.user, challenge=challenge)
        url = reverse("challenge-participants", args=[challenge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
