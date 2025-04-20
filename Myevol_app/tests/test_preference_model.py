from django.test import TestCase
from django.contrib.auth import get_user_model
from Myevol_app.models.userPreference_model import UserPreference

User = get_user_model()

class UserPreferenceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        # Les préférences devraient être créées automatiquement via le signal
        self.preferences = UserPreference.objects.get(user=self.user)

    def test_preferences_created_for_new_user(self):
        """Vérifie que les préférences sont créées automatiquement pour un nouvel utilisateur"""
        # Créer un nouvel utilisateur
        new_user = User.objects.create_user(
            username="newuser",
            email="new@example.com",
            password="newpassword123"
        )
        
        # Vérifier que les préférences existent
        self.assertTrue(hasattr(new_user, 'preferences'))
        self.assertIsNotNone(new_user.preferences)
        
        # Vérifier les valeurs par défaut
        self.assertFalse(new_user.preferences.dark_mode)
        self.assertEqual(new_user.preferences.accent_color, "#6C63FF")
        self.assertEqual(new_user.preferences.font_choice, "Roboto")
        self.assertTrue(new_user.preferences.enable_animations)
        self.assertTrue(new_user.preferences.notif_badge)
        self.assertTrue(new_user.preferences.notif_objectif)
        self.assertTrue(new_user.preferences.notif_info)
        self.assertTrue(new_user.preferences.notif_statistique)

    def test_str_representation(self):
        """Teste la représentation en chaîne"""
        self.assertEqual(str(self.preferences), f"Préférences de {self.user.username}")

    def test_to_dict_method(self):
        """Teste la méthode to_dict"""
        prefs_dict = self.preferences.to_dict()
        
        # Vérifier la structure
        self.assertIn("dark_mode", prefs_dict)
        self.assertIn("accent_color", prefs_dict)
        self.assertIn("font_choice", prefs_dict)
        self.assertIn("enable_animations", prefs_dict)
        self.assertIn("notifications", prefs_dict)
        
        # Vérifier les sous-éléments
        self.assertIn("badge", prefs_dict["notifications"])
        self.assertIn("objectif", prefs_dict["notifications"])
        self.assertIn("info", prefs_dict["notifications"])
        self.assertIn("statistique", prefs_dict["notifications"])
        
        # Vérifier quelques valeurs
        self.assertEqual(prefs_dict["dark_mode"], self.preferences.dark_mode)
        self.assertEqual(prefs_dict["notifications"]["badge"], self.preferences.notif_badge)

    def test_get_appearance_settings(self):
        """Teste la méthode get_appearance_settings"""
        appearance = self.preferences.get_appearance_settings()
        
        # Vérifier que seuls les paramètres d'apparence sont présents
        self.assertIn("dark_mode", appearance)
        self.assertIn("accent_color", appearance)
        self.assertIn("font_choice", appearance)
        self.assertIn("enable_animations", appearance)
        
        # Vérifier qu'il n'y a pas de paramètres de notification
        self.assertNotIn("notifications", appearance)
        self.assertNotIn("notif_badge", appearance)
        
        # Vérifier les valeurs
        self.assertEqual(appearance["dark_mode"], self.preferences.dark_mode)
        self.assertEqual(appearance["accent_color"], self.preferences.accent_color)

    def test_get_notification_settings(self):
        """Teste la méthode get_notification_settings"""
        notif_settings = self.preferences.get_notification_settings()
        
        # Vérifier que seuls les paramètres de notification sont présents
        self.assertIn("badge", notif_settings)
        self.assertIn("objectif", notif_settings)
        self.assertIn("info", notif_settings)
        self.assertIn("statistique", notif_settings)
        
        # Vérifier qu'il n'y a pas de paramètres d'apparence
        self.assertNotIn("dark_mode", notif_settings)
        self.assertNotIn("accent_color", notif_settings)
        
        # Vérifier les valeurs
        self.assertEqual(notif_settings["badge"], self.preferences.notif_badge)
        self.assertEqual(notif_settings["objectif"], self.preferences.notif_objectif)

    def test_reset_to_defaults(self):
        """Teste la méthode reset_to_defaults"""
        # Modifier les préférences
        self.preferences.dark_mode = True
        self.preferences.accent_color = "#FF0000"
        self.preferences.font_choice = "Arial"
        self.preferences.enable_animations = False
        self.preferences.notif_badge = False
        self.preferences.notif_objectif = False
        self.preferences.save()
        
        # Réinitialiser
        self.preferences.reset_to_defaults()
        
        # Vérifier que les valeurs sont revenues aux défauts
        self.assertFalse(self.preferences.dark_mode)
        self.assertEqual(self.preferences.accent_color, "#6C63FF")
        self.assertEqual(self.preferences.font_choice, "Roboto")
        self.assertTrue(self.preferences.enable_animations)
        self.assertTrue(self.preferences.notif_badge)
        self.assertTrue(self.preferences.notif_objectif)
        self.assertTrue(self.preferences.notif_info)
        self.assertTrue(self.preferences.notif_statistique)

    def test_get_or_create_for_user(self):
        """Teste la méthode get_or_create_for_user"""
        # Obtenir les préférences pour un utilisateur existant
        prefs = UserPreference.get_or_create_for_user(self.user)
        self.assertEqual(prefs, self.preferences)
        
        # Supprimer les préférences et vérifier qu'elles sont recréées
        self.preferences.delete()
        
        prefs = UserPreference.get_or_create_for_user(self.user)
        self.assertIsNotNone(prefs)
        self.assertEqual(prefs.user, self.user)
        
        # Vérifier les valeurs par défaut
        self.assertFalse(prefs.dark_mode)
        self.assertEqual(prefs.accent_color, "#6C63FF")

    def test_should_send_notification(self):
        """Teste la méthode should_send_notification"""
        # Par défaut, toutes les notifications sont activées
        self.assertTrue(self.preferences.should_send_notification('badge'))
        self.assertTrue(self.preferences.should_send_notification('objectif'))
        self.assertTrue(self.preferences.should_send_notification('info'))
        self.assertTrue(self.preferences.should_send_notification('statistique'))
        
        # Désactiver certaines notifications
        self.preferences.notif_badge = False
        self.preferences.notif_info = False
        self.preferences.save()
        
        # Vérifier que seules les notifications désactivées retournent False
        self.assertFalse(self.preferences.should_send_notification('badge'))
        self.assertTrue(self.preferences.should_send_notification('objectif'))
        self.assertFalse(self.preferences.should_send_notification('info'))
        self.assertTrue(self.preferences.should_send_notification('statistique'))
        
        # Tester avec un type inexistant
        self.assertFalse(self.preferences.should_send_notification('unknown_type'))

    def test_create_preferences_for_user_service(self):
        """Test du service create_preferences_for_user"""
        from Myevol_app.services.preferences_service import create_preferences_for_user
        
        # Supprimer d'abord les préférences existantes
        self.preferences.delete()
        
        # Utiliser le service pour créer de nouvelles préférences
        prefs = create_preferences_for_user(self.user)
        
        # Vérifier que les préférences ont été créées
        self.assertIsNotNone(prefs)
        self.assertEqual(prefs.user, self.user)
        
        # Vérifier qu'un second appel renvoie les mêmes préférences
        prefs2 = create_preferences_for_user(self.user)
        self.assertEqual(prefs.id, prefs2.id)  # Même instance en DB

    def test_preference_persistence_after_user_changes(self):
        """Teste que les préférences persistent après modification de l'utilisateur"""
        # Modifier les préférences
        self.preferences.dark_mode = True
        self.preferences.save()
        
        # Modifier l'utilisateur
        self.user.first_name = "Test"
        self.user.save()
        
        # Vérifier que les préférences n'ont pas changé
        self.preferences.refresh_from_db()
        self.assertTrue(self.preferences.dark_mode)

    def test_default_creation_behavior(self):
        """Teste le comportement par défaut lors de la création de préférences"""
        # Supprimer les préférences existantes
        self.preferences.delete()
        
        # Créer un dictionnaire de valeurs modifiées pour certains champs
        custom_values = {
            "dark_mode": True,
            "accent_color": "#FF5733"
        }
        
        # Utiliser get_or_create avec des valeurs personnalisées
        prefs, created = UserPreference.objects.get_or_create(
            user=self.user,
            defaults=custom_values
        )
        
        # Vérifier que les valeurs personnalisées sont utilisées
        self.assertTrue(prefs.dark_mode)
        self.assertEqual(prefs.accent_color, "#FF5733")
        
        # Vérifier que les autres champs ont les valeurs par défaut
        self.assertEqual(prefs.font_choice, "Roboto")
        self.assertTrue(prefs.enable_animations)