# tests/test_user_preference_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from tests.tests_viewsets.factories import UserFactory, UserPreferenceFactory

class UserPreferenceViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.pref = UserPreferenceFactory(user=self.user)


    def test_update_preferences(self):
        url = reverse("user-get-preferences")
        data = {
            "dark_mode": True,
            "accent_color": "#FF0000"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["dark_mode"])
        self.assertEqual(response.data["accent_color"], "#FF0000")


    def test_appearance_preferences(self):
        url = reverse("userpreference-appearance")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("dark_mode", response.data)
        self.assertIn("font_choice", response.data)

    def test_notification_preferences(self):
        url = reverse("userpreference-notifications")
        response = self.client.get(url)
        self.assertIn("badge", response.data)
        self.assertIn("objectif", response.data)


    def test_toggle_notification(self):
        url = reverse("userpreference-toggle-notification")
        data = {
            "notif_type": "badge",  # ✅ sans préfixe
            "enabled": False
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_preferences(self):
        url = reverse("userpreference-reset")
        data = {"confirm": True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Préférences réinitialisées.")

    def test_default_preferences(self):
        url = reverse("userpreference-defaults")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("dark_mode", response.data)
        self.assertIn("notif_statistique", response.data)

    