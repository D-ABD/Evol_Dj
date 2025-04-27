# tests/tests_models/test_stats_model.py
from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

from freezegun import freeze_time

from Myevol_app.models import DailyStat, WeeklyStat, JournalEntry

User = get_user_model()

@freeze_time("2025-04-23")
class StatsModelsTests(TestCase): 
    @patch('Myevol_app.models.user_model.User.create_default_preferences')
    def setUp(self, mock_create_prefs):
        # Empêche la création des préférences utilisateur
        mock_create_prefs.return_value = None
        
        self.user = User.objects.create_user(
            username="statuser",
            email="stat@example.com",
            password="testpass"
        )
        
        # Patcher les méthodes appelées lors de la création d'entrées de journal
        patcher1 = patch('Myevol_app.services.user_stats_service.compute_current_streak', return_value=0)
        patcher2 = patch('Myevol_app.models.stats_model.DailyStat.generate_for_user')
        patcher3 = patch('Myevol_app.services.challenge_service.check_challenges')
        patcher4 = patch('Myevol_app.models.user_model.User.update_badges')
        patcher5 = patch('Myevol_app.models.user_model.User.update_streaks')
        
        # Démarrer les patchers
        self.mock_compute_streak = patcher1.start()
        self.mock_generate_stats = patcher2.start()
        self.mock_check_challenges = patcher3.start()
        self.mock_update_badges = patcher4.start()
        self.mock_update_streaks = patcher5.start()
        
        # Créer quelques entrées pour les statistiques
        today = now().date()
        
        JournalEntry.objects.create(
            user=self.user,
            content="Entry 1",
            mood=7,
            category="work"
        )
        
        JournalEntry.objects.create(
            user=self.user,
            content="Entry 2",
            mood=8,
            category="personal"
        )
        
        # Arrêter de patcher generate_for_user pour permettre au test de l'appeler
        patcher2.stop()
        
        # Générer les statistiques
        self.daily_stat = DailyStat.generate_for_user(self.user, today)
        self.weekly_stat = WeeklyStat.generate_for_user(self.user, today)
        
        # Nous devons maintenant arrêter les autres patchers pour éviter les problèmes de fuite
        patcher1.stop()
        patcher3.stop()
        patcher4.stop()
        patcher5.stop()
        
    def test_daily_stat_str(self):
        self.assertIn(self.user.username, str(self.daily_stat))
        
    def test_weekly_stat_str(self):
        self.assertIn(self.user.username, str(self.weekly_stat))
        self.assertIn("semaine du", str(self.weekly_stat))
        
    def test_daily_stat_entries_count(self):
        self.assertEqual(self.daily_stat.entries_count, 2)
        
    def test_weekly_stat_entries_count(self):
        self.assertEqual(self.weekly_stat.entries_count, 2)
        
    def test_daily_stat_mood_average(self):
        # (7 + 8) / 2 = 7.5
        self.assertEqual(self.daily_stat.mood_average, 7.5)
        
    def test_daily_stat_categories(self):
        expected = {"work": 1, "personal": 1}
        self.assertEqual(self.daily_stat.categories, expected)
        
    def test_day_of_week(self):
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        weekday = now().date().weekday()
        self.assertEqual(self.daily_stat.day_of_week(), days[weekday])
        
    def test_is_weekend(self):
        today = now().date()
        weekday = today.weekday()
        
        # Modifier la date du stat pour tester weekend/jour de semaine
        if weekday < 5:  # Lundi-Vendredi
            self.assertFalse(self.daily_stat.is_weekend())
            
            # Tester avec une date de weekend (samedi)
            saturday = today + timedelta(days=(5 - weekday))
            stat_weekend = DailyStat.objects.create(
                user=self.user,
                date=saturday,
                entries_count=0
            )
            self.assertTrue(stat_weekend.is_weekend())
            
    def test_week_end(self):
        start_date = self.weekly_stat.week_start
        expected_end = start_date + timedelta(days=6)
        self.assertEqual(self.weekly_stat.week_end(), expected_end)
        
    def test_week_number(self):
        # Utiliser la date réelle pour obtenir le numéro de semaine attendu
        expected = self.weekly_stat.week_start.isocalendar()[1]
        self.assertEqual(self.weekly_stat.week_number(), expected)
        
    @patch('Myevol_app.services.user_stats_service.compute_current_streak', return_value=0)
    @patch('Myevol_app.services.challenge_service.check_challenges')
    @patch('Myevol_app.models.user_model.User.update_badges')
    @patch('Myevol_app.models.user_model.User.update_streaks')
    def test_top_category(self, mock_update_streaks, mock_update_badges, mock_check_challenges, mock_compute_streak):
        # Catégories {"work": 1, "personal": 1}
        # On n'a pas de catégorie majoritaire, donc le résultat dépend de l'ordre de traitement
        self.assertIn(self.weekly_stat.top_category(), ["work", "personal"])
        
        # Ajouter une entrée supplémentaire pour avoir une catégorie majoritaire
        JournalEntry.objects.create(
            user=self.user,
            content="Another work entry",
            mood=6,
            category="work"
        )
        
        # Régénérer les stats
        today = now().date()
        self.weekly_stat = WeeklyStat.generate_for_user(self.user, today)
        
        # Maintenant la catégorie "work" devrait être majoritaire
        self.assertEqual(self.weekly_stat.top_category(), "work")