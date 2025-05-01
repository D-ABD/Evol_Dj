# tests/test_quote_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from tests.tests_viewsets.factories import QuoteFactory, UserFactory

class QuoteViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.quote = QuoteFactory()

    def test_random_quote(self):
        url = reverse("quote-random")
        response = self.client.get(url)
        self.assertIn("quote", response.data)
        self.assertIn("text", response.data["quote"])

    def test_daily_quote(self):
        url = reverse("quote-daily")
        response = self.client.get(url)
        self.assertIn("quote", response.data)
        self.assertIn("text", response.data["quote"])

    def test_list_authors(self):
        url = reverse("quote-authors")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("authors", response.data)

    def test_list_mood_tags(self):
        url = reverse("quote-mood-tags")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("mood_tags", response.data)

    def test_search_quote(self):
        QuoteFactory(text="Le succès est une habitude", author="Napoleon Hill", mood_tag="motivated")
        url = reverse("quote-search") + "?query=succès&author=Napoleon Hill&mood_tag=motivated"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
