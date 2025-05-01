from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from tests.tests_viewsets.factories import UserFactory


class UserViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory(password="password123")
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_my_profile(self):
        url = reverse("user-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_update_my_profile(self):
        url = reverse("user-me")
        data = {"first_name": "Nouveau"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Nouveau")

    def test_change_password(self):
        url = reverse("user-change-password")
        data = {
            "current_password": "password123",
            "new_password": "newpassword456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_stats(self):
        url = reverse("user-stats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("mood_stats", response.data)
        self.assertIn("streak_stats", response.data)
        self.assertIn("activity_stats", response.data)

    def test_add_xp(self):
        url = reverse("user-add-xp")
        data = {"amount": 50}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount_added"], 50)
        self.assertEqual(response.data["new_total"], 50)

    def test_get_preferences(self):
        url = reverse("user-get-preferences")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("dark_mode", response.data)

    def test_update_preferences(self):
        url = reverse("user-get-preferences")
        data = {
            "dark_mode": True,
            "accent_color": "#FF0000",
            "font_choice": "Arial",
            "enable_animations": False,
            "notif_badge": True,
            "notif_objectif": True,
            "notif_info": True,
            "notif_statistique": True
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["dark_mode"], True)
        self.assertEqual(response.data["accent_color"], "#FF0000")
