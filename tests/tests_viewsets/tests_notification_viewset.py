# tests/test_notification_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from tests.tests_viewsets.factories import NotificationFactory, UserFactory

class NotificationViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.notification = NotificationFactory(user=self.user)

    def test_create_notification(self):
        url = reverse("notification-list")
        data = {
            "message": "Test notification",
            "notif_type": "badge"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_notification(self):
        url = reverse("notification-detail", args=[self.notification.id])
        data = {"is_read": True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_delete_notification(self):
        url = reverse("notification-detail", args=[self.notification.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unread_notifications(self):
        # Ensure one unread, one read
        NotificationFactory(user=self.user, is_read=False)
        NotificationFactory(user=self.user, is_read=True)
        url = reverse("notification-unread")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(not notif["is_read"] for notif in response.data))

    def test_notification_count(self):
        url = reverse("notification-count")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total", response.data)

    def test_bulk_action_mark_read(self):
        n1 = NotificationFactory(user=self.user, is_read=False)
        n2 = NotificationFactory(user=self.user, is_read=False)
        url = reverse("notification-bulk-action")
        data = {
            "notif_type": "all",
            "action": "mark_all_read"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_access_others_notification(self):
        other_user = UserFactory()
        notif = NotificationFactory(user=other_user)
        url = reverse("notification-detail", args=[notif.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
