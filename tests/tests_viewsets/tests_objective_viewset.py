# tests/test_objective_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tests.tests_viewsets.factories import ObjectiveFactory, UserFactory
from datetime import date, timedelta

class ObjectiveViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.objective = ObjectiveFactory(user=self.user)

    def test_list_objectives(self):
        url = reverse("objective-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_objective(self):
        url = reverse("objective-detail", args=[self.objective.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_update_objective(self):
        url = reverse("objective-detail", args=[self.objective.id])
        data = {"title": "Objectif modifié"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_objective(self):
        url = reverse("objective-detail", args=[self.objective.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_complete_objective(self):
        url = reverse("objective-complete", args=[self.objective.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_objective_stats(self):
        url = reverse("objective-stats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_objective_upcoming(self):
        url = reverse("objective-upcoming")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_objective_categories(self):
        url = reverse("objective-categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
