# tests/test_journal_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tests.tests_viewsets.factories import JournalEntryFactory, UserFactory

class JournalViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.entry = JournalEntryFactory(user=self.user)

    def test_list_entries(self):
        url = reverse("journalentry-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_entry(self):
        url = reverse("journalentry-detail", args=[self.entry.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_entry(self):
        url = reverse("journalentry-list")
        data = {
            "content": "Nouvelle entrée",
            "mood": 4,
            "category": "Santé"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_entry(self):
        url = reverse("journalentry-detail", args=[self.entry.id])
        data = {"content": "Contenu mis à jour"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.content, "Contenu mis à jour")

    def test_delete_entry(self):
        url = reverse("journalentry-detail", args=[self.entry.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_calendar_view(self):
        url = reverse("journalentry-calendar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_stats_view(self):
        url = reverse("journalentry-stats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("average_mood", response.data)
