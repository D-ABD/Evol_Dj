# tests/tests_models/test_objective_model.py
from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from unittest.mock import patch
from freezegun import freeze_time

from Myevol_app.models import Objective, JournalEntry

User = get_user_model()

class ObjectiveModelTests(TestCase):
    @patch('Myevol_app.models.user_model.User.create_default_preferences')
    def setUp(self, mock_create_prefs):
        # Empêche la création des préférences utilisateur
        mock_create_prefs.return_value = None
        
        self.user = User.objects.create_user(
            username="objuser",
            email="obj@example.com",
            password="testpass"
        )
        
        # Date cible dans le futur
        self.target_date = now().date() + timedelta(days=7)
        
        self.objective = Objective.objects.create(
            user=self.user,
            title="Test objective",
            category="test",
            target_date=self.target_date,
            target_value=3
        )
        
    def test_str_method(self):
        self.assertIn("Test objective", str(self.objective))
        self.assertIn("🕓", str(self.objective))  # Non complété
        
        # Marquer comme complété et tester à nouveau
        self.objective.done = True
        self.objective.save()
        self.assertIn("✅", str(self.objective))
        
    def test_clean_future_date(self):
        # Date dans le passé devrait lever une exception
        objective = Objective(
            user=self.user,
            title="Past objective",
            category="test",
            target_date=now().date() - timedelta(days=1),
            target_value=1
        )
        
        with self.assertRaises(ValidationError):
            objective.clean()
            
    # On patche les méthodes appelées lors de la création d'entrées de journal

    @freeze_time("2025-04-25")
    @patch('Myevol_app.services.user_stats_service.compute_current_streak')
    @patch('Myevol_app.models.stats_model.DailyStat.generate_for_user')
    @patch('Myevol_app.services.challenge_service.check_challenges')  
    @patch('Myevol_app.models.user_model.User.update_badges')
    @patch('Myevol_app.models.user_model.User.update_streaks')
    def test_entries_done(self, mock_update_streaks, mock_update_badges,
                        mock_check_challenges, mock_generate_stats, mock_compute_streak):
        mock_compute_streak.return_value = 0

        # Entrée sans lien avec la date cible
        JournalEntry.objects.create(
            user=self.user,
            content="Wrong date entry",
            mood=7,
            category="test"
        )

        # Entrée correspondant à la target_date
        with freeze_time(self.target_date):
            JournalEntry.objects.create(
                user=self.user,
                content="Entry for target date",
                mood=7,
                category="test"
            )

        # Repasser dans un bloc à target_date pour la vérification
        with freeze_time(self.target_date):
            self.assertEqual(self.objective.entries_done(), 1)


    def test_progress(self):
        # Aucune entrée, progression à 0%
        self.assertEqual(self.objective.progress(), 0)
        
        # Créer une entrée pour atteindre 33% (1/3)
        with patch('Myevol_app.models.objective_model.Objective.entries_done') as mock_entries_done:
            mock_entries_done.return_value = 1
            self.assertEqual(self.objective.progress(), 33)
            
            # 2 entrées pour 66%
            mock_entries_done.return_value = 2
            self.assertEqual(self.objective.progress(), 66)
            
            # 3 entrées pour 100%
            mock_entries_done.return_value = 3
            self.assertEqual(self.objective.progress(), 100)
            
            # Plus que le target, toujours 100% max
            mock_entries_done.return_value = 4
            self.assertEqual(self.objective.progress(), 100)
            
    def test_is_achieved(self):
        # Non réalisé par défaut
        self.assertFalse(self.objective.is_achieved())
        
        # Marquer comme réalisé
        self.objective.done = True
        self.assertTrue(self.objective.is_achieved())
        
        # Réinitialiser
        self.objective.done = False
        
        # Atteint via progression
        with patch('Myevol_app.models.objective_model.Objective.progress') as mock_progress:
            mock_progress.return_value = 100
            self.assertTrue(self.objective.is_achieved())
            
    def test_days_remaining(self):
        target_date = now().date() + timedelta(days=3)
        self.objective.target_date = target_date
        self.objective.save()

        simulated_today = target_date - timedelta(days=3)

        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = simulated_today
            days = self.objective.days_remaining()
            self.assertEqual(days, 3)


            
    def test_is_overdue(self):
        # Par défaut, pas en retard
        self.assertFalse(self.objective.is_overdue())
        
        # Modifier la date cible pour qu'elle soit dans le passé (sans save pour éviter clean())
        self.objective.target_date = now().date() - timedelta(days=1)
        self.assertTrue(self.objective.is_overdue())
        
        # Si l'objectif est marqué comme complété, il ne doit plus être considéré en retard
        self.objective.done = True
        self.assertFalse(self.objective.is_overdue())

    @patch('Myevol_app.models.objective_model.Objective.progress', return_value=100)
    def test_save_sets_done_when_achieved(self, mock_progress):
        objective = Objective(
            user=self.user,
            title="Auto complete",
            category="test",
            target_date=now().date() + timedelta(days=2),
            target_value=1
        )
        objective.save()
        self.assertTrue(objective.done)
