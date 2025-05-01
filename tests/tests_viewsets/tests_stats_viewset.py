# tests/test_stats_viewset.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from tests.tests_viewsets.factories import DailyStatFactory, UserFactory

class StatsViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.stat = DailyStatFactory(user=self.user)

    def test_list_stats(self):
        url = reverse("dailystat-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_stat(self):
        url = reverse("dailystat-detail", args=[self.stat.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tests.tests_viewsets.factories import (
    UserFactory,
    DailyStatFactory,
    WeeklyStatFactory,
    MonthlyStatFactory,
    AnnualStatFactory
)

class StatsViewSetTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.daily = DailyStatFactory(user=self.user)
        self.weekly = WeeklyStatFactory(user=self.user)
        self.monthly = MonthlyStatFactory(user=self.user)
        self.annual = AnnualStatFactory(user=self.user)

    def test_overview(self):
        url = reverse("stats-overview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("daily", response.data)  # selon contenu du serializer

    def test_categories_analysis(self):
        url = reverse("stats-categories") + "?period=month"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("period", response.data)

    def test_daily_stats(self):
        url = reverse("stats-daily")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("meta", response.data)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data["meta"])
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_weekly_stats(self):
        url = reverse("stats-weekly")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("meta", response.data)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data["meta"])
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_monthly_stats(self):
        url = reverse("stats-monthly")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("meta", response.data)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data["meta"])
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_annual_stats(self):
        url = reverse("stats-annual")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("meta", response.data)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data["meta"])
        self.assertGreaterEqual(len(response.data["results"]), 1)
