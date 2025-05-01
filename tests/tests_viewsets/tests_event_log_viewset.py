# tests/test_event_log_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tests.tests_viewsets.factories import EventLogFactory, UserFactory

class EventLogViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.log = EventLogFactory(user=self.user)

    def test_list_event_logs(self):
        url = reverse("eventlog-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_event_log(self):
        url = reverse("eventlog-detail", args=[self.log.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.log.id)

    def test_cannot_access_others_logs(self):
        other_log = EventLogFactory()
        url = reverse("eventlog-detail", args=[other_log.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_log_statistics(self):
        url = reverse("eventlog-statistics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("period_days", response.data)

    def test_search_logs(self):
        EventLogFactory(user=self.user, action="login")
        url = reverse("eventlog-list") + "?search=login"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
