from django.test import TestCase
from django.contrib.auth import get_user_model
from Myevol_app.models.badge_model import Badge, BadgeTemplate
from Myevol_app.services.badge_service import update_user_badges

User = get_user_model()

class BadgeServiceTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        # Créer quelques templates de badges
        self.badge_template1 = BadgeTemplate.objects.create(
            name="Test Badge 1",
            description="Description du test badge 1",
            icon="🏆",
            condition="Test condition 1"
        )
        
        self.badge_template2 = BadgeTemplate.objects.create(
            name="Test Badge 2",
            description="Description du test badge 2",
            icon="🌟",
            condition="Test condition 2"
        )
        
    def test_update_user_badges_creates_new_badges(self):
        """Teste que update_user_badges crée de nouveaux badges si les conditions sont remplies"""
        # Mock la méthode check_unlock pour retourner True
        original_check_unlock = BadgeTemplate.check_unlock
        BadgeTemplate.check_unlock = lambda self, user: True
        
        # Vérifier qu'il n'y a pas de badges au départ
        self.assertEqual(Badge.objects.filter(user=self.user).count(), 0)
        
        # Appeler le service
        update_user_badges(self.user)
        
        # Vérifier que les badges ont été créés
        self.assertEqual(Badge.objects.filter(user=self.user).count(), 2)
        
        # Restaurer la méthode originale
        BadgeTemplate.check_unlock = original_check_unlock
    
    def test_update_user_badges_skips_existing_badges(self):
        """Teste que update_user_badges ne crée pas de doublons pour les badges existants"""
        # Créer un badge existant
        Badge.objects.create(
            user=self.user,
            name="Test Badge 1",
            description="Description existante",
            icon="🏆"
        )
        
        # Mock la méthode check_unlock pour retourner True
        original_check_unlock = BadgeTemplate.check_unlock
        BadgeTemplate.check_unlock = lambda self, user: True
        
        # Appeler le service
        update_user_badges(self.user)
        
        # Vérifier qu'un seul badge a été créé (pas de doublon)
        self.assertEqual(Badge.objects.filter(user=self.user).count(), 2)
        
        # Restaurer la méthode originale
        BadgeTemplate.check_unlock = original_check_unlock
    
    def test_update_user_badges_respects_conditions(self):
        """Teste que update_user_badges respecte les conditions de déblocage"""
        # Mock la méthode check_unlock pour ne débloquer que certains badges
        original_check_unlock = BadgeTemplate.check_unlock
        
        # Fonction de remplacement qui ne débloque que "Test Badge 1"
        def mock_check_unlock(self, user):
            return self.name == "Test Badge 1"
            
        BadgeTemplate.check_unlock = mock_check_unlock
        
        # Appeler le service
        update_user_badges(self.user)
        
        # Vérifier que seul le badge qui remplit la condition a été créé
        self.assertEqual(Badge.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Badge.objects.filter(user=self.user, name="Test Badge 1").count(), 1)
        self.assertEqual(Badge.objects.filter(user=self.user, name="Test Badge 2").count(), 0)
        
        # Restaurer la méthode originale
        BadgeTemplate.check_unlock = original_check_unlock

from django.test import TestCase
from django.contrib.auth import get_user_model
from Myevol_app.models.userPreference_model import UserPreference
from Myevol_app.services.userpreference_service import create_preferences_for_user

User = get_user_model()

class PreferencesServiceTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
    
    def test_create_preferences_for_user_creates_new_preferences(self):
        """Teste que create_preferences_for_user crée des préférences si elles n'existent pas"""
        # Supprimer les préférences existantes (créées par signal)
        UserPreference.objects.filter(user=self.user).delete()
        
        # Vérifier qu'il n'y a pas de préférences
        self.assertEqual(UserPreference.objects.filter(user=self.user).count(), 0)
        
        # Appeler le service
        prefs = create_preferences_for_user(self.user)
        
        # Vérifier que les préférences ont été créées
        self.assertIsNotNone(prefs)
        self.assertEqual(UserPreference.objects.filter(user=self.user).count(), 1)
        self.assertEqual(prefs.user, self.user)
    
    def test_create_preferences_for_user_returns_existing_preferences(self):
        """Teste que create_preferences_for_user retourne les préférences existantes"""
        # Les préférences existent déjà grâce au signal post_save
        # Récupérer les préférences existantes
        existing_prefs = UserPreference.objects.get(user=self.user)
        
        # Modifier-les pour les rendre distinctes
        existing_prefs.dark_mode = True
        existing_prefs.accent_color = "#FF0000"
        existing_prefs.save()
        
        # Appeler le service
        prefs = create_preferences_for_user(self.user)
        
        # Vérifier que les préférences existantes sont retournées
        self.assertEqual(prefs.id, existing_prefs.id)
        self.assertEqual(prefs.dark_mode, True)
        self.assertEqual(prefs.accent_color, "#FF0000")

from django.test import TestCase
from django.contrib.auth import get_user_model
from Myevol_app.services.streak_service import update_user_streak

User = get_user_model()

class StreakServiceTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            longest_streak=5  # Définir une valeur initiale
        )
    
    def test_update_user_streak_updates_when_current_is_higher(self):
        """Teste que update_user_streak met à jour longest_streak quand current_streak est plus grand"""
        # Mock la méthode current_streak pour retourner une valeur plus élevée
        original_current_streak = self.user.current_streak
        self.user.current_streak = lambda: 10
        
        # Appeler le service
        update_user_streak(self.user)
        
        # Recharger l'utilisateur de la base de données
        self.user.refresh_from_db()
        
        # Vérifier que longest_streak a été mis à jour
        self.assertEqual(self.user.longest_streak, 10)
        
        # Restaurer la méthode originale
        self.user.current_streak = original_current_streak
    
    def test_update_user_streak_does_not_update_when_current_is_lower(self):
        """Teste que update_user_streak ne fait rien quand current_streak est plus petit"""
        # Mock la méthode current_streak pour retourner une valeur plus basse
        original_current_streak = self.user.current_streak
        self.user.current_streak = lambda: 3
        
        # Appeler le service
        update_user_streak(self.user)
        
        # Recharger l'utilisateur de la base de données
        self.user.refresh_from_db()
        
        # Vérifier que longest_streak n'a pas changé
        self.assertEqual(self.user.longest_streak, 5)
        
        # Restaurer la méthode originale
        self.user.current_streak = original_current_streak

