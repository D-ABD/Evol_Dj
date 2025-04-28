from django.test import TestCase
from django.contrib.auth import get_user_model
from Myevol_app.models.userPreference_model import UserPreference
from Myevol_app.serializers.userPreference_serializers import (
    UserPreferenceUpdateSerializer, 
    AppearancePreferenceSerializer, NotificationPreferenceSerializer,
    NotificationToggleSerializer, PreferenceResetSerializer, 
    UserPreferenceCreateSerializer,
)
from Myevol_app.serializers.user_serializers import UserPreferencesSerializer

User = get_user_model()

class UserPreferenceSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.prefs = UserPreference.get_or_create_for_user(self.user)  # ✅ get_or_create évite les doublons

    def _create_user(self, username, email):
        return User.objects.create_user(username=username, email=email, password="password123")




    def test_update_preference_serializer_valid(self):
        serializer = UserPreferenceUpdateSerializer(instance=self.prefs, data={'dark_mode': True})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_prefs = serializer.save()
        self.assertTrue(updated_prefs.dark_mode)

    def test_appearance_preference_serializer(self):
        serializer = AppearancePreferenceSerializer(instance=self.prefs)
        data = serializer.data
        self.assertIn('dark_mode', data)
        self.assertIn('accent_color', data)

    def test_notification_preference_serializer(self):
        serializer = NotificationPreferenceSerializer(instance=self.prefs)
        data = serializer.data
        self.assertIn('badge', data)
        self.assertIn('objectif', data)
        self.assertIn('info', data)
        self.assertIn('statistique', data)

    def test_notification_toggle_serializer_enable(self):
        serializer = NotificationToggleSerializer(instance=self.prefs, data={
            'notif_type': 'badge',
            'enabled': True
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_prefs = serializer.update(self.prefs, serializer.validated_data)
        self.assertTrue(updated_prefs.notif_badge)

    def test_notification_toggle_serializer_disable(self):
        serializer = NotificationToggleSerializer(instance=self.prefs, data={
            'notif_type': 'badge',
            'enabled': False
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_prefs = serializer.update(self.prefs, serializer.validated_data)
        self.assertFalse(updated_prefs.notif_badge)

    def test_preference_reset_serializer(self):
        self.prefs.dark_mode = True
        self.prefs.save()
        serializer = PreferenceResetSerializer(instance=self.prefs, data={'confirm': True})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        reset_prefs = serializer.update(self.prefs, serializer.validated_data)
        self.assertFalse(reset_prefs.dark_mode)

    def test_user_preference_create_serializer(self):
        # S'assurer qu'il n'existe pas déjà de UserPreference pour cet utilisateur
        self.user.preferences.delete()

        data = {
            'user': self.user.id,
            'dark_mode': True,
            'accent_color': '#FF5733',
            'font_choice': 'Open Sans',
            'enable_animations': False,
            'notif_badge': True,
            'notif_objectif': True,
            'notif_info': True,
            'notif_statistique': False,
        }
        serializer = UserPreferenceCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        # On sauvegarde pour vérifier ensuite
        instance = serializer.save()
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.accent_color, '#FF5733')
        self.assertFalse(instance.enable_animations)

