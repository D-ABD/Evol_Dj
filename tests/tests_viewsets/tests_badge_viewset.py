# tests/test_badge_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Myevol_app.models.badge_model import Badge
from tests.tests_viewsets.factories import BadgeFactory, BadgeTemplateFactory, UserFactory

class BadgeViewSetTests(APITestCase):

    def setUp(self):
      self.user = UserFactory()
      self.client.force_authenticate(user=self.user)
      self.badge = BadgeFactory(user=self.user)  # 👈 important !


    def test_list_badges(self):
        url = reverse("badge-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_badge(self):
        url = reverse("badge-detail", args=[self.badge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.badge.id)


    def test_create_badge(self):
        url = reverse("badge-list")
        template = BadgeTemplateFactory()
        data = {
            "name": "Test Badge",
            "description": "Badge pour test",
            "icon": "test-icon.png",
            "template": template.id,  # <- correct
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_badge(self):
        url = reverse("badge-detail", args=[self.badge.id])
        data = {"name": "Badge modifié"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.badge.refresh_from_db()
        self.assertEqual(self.badge.name, "Badge modifié")

    def test_delete_badge(self):
        url = reverse("badge-detail", args=[self.badge.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Badge.objects.filter(id=self.badge.id).exists())

    def test_user_cannot_access_others_badge(self):
        other_user = UserFactory()
        other_badge = BadgeFactory(user=other_user)
        url = reverse("badge-detail", args=[other_badge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_badges(self):
        BadgeFactory(user=self.user, name="UniqueSearchBadge")
        url = reverse("badge-list") + "?search=UniqueSearchBadge"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertTrue(any("UniqueSearchBadge" in b["name"] for b in results))


    def test_ordering_badges(self):
        # Nouveau user pour un contexte isolé
        user = UserFactory()
        self.client.force_authenticate(user=user)

        BadgeFactory(user=user, name="A", date_obtenue="2025-01-01")
        BadgeFactory(user=user, name="B", date_obtenue="2025-04-01")
        
        url = reverse("badge-list") + "?ordering=date_obtenue"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual([r["name"] for r in results], ["A", "B"])
