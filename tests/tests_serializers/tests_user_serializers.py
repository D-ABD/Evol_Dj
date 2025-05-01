from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from datetime import timedelta

from Myevol_app.serializers.user_serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserStatsSerializer,
    UserPreferencesSerializer,
    UserRegistrationSerializer,
    UserXpSerializer
)

User = get_user_model()

class UserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

    def test_user_serializer_fields(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['username'], "testuser")
        self.assertEqual(data['email'], "test@example.com")
        self.assertIn('level', data)
        self.assertIn('current_streak', data)

class UserProfileSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@example.com",
            password="password123"
        )

    @patch('Myevol_app.models.user_model.User.mood_average')
    def test_user_profile_serializer_fields(self, mock_mood_average):
        mock_mood_average.return_value = 7
        serializer = UserProfileSerializer(self.user)
        data = serializer.data
        self.assertIn('stats_summary', data)
        self.assertIn('mood_average', data)
        self.assertIn('badges_count', data)
        self.assertIsInstance(data['activity_summary'], dict)

class UserUpdateSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="updateuser",
            email="update@example.com",
            password="oldpassword"
        )

    def test_update_serializer_without_password_change(self):
        serializer = UserUpdateSerializer(
            instance=self.user,
            data={'username': 'updateduser', 'email': 'new@example.com'},
            partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'new@example.com')

    def test_update_serializer_with_password_change(self):
        data = {
            'current_password': 'oldpassword',
            'new_password': 'newsecurepassword'
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertTrue(self.user.check_password('newsecurepassword'))

    def test_update_serializer_invalid_current_password(self):
        data = {
            'current_password': 'wrongpassword',
            'new_password': 'newsecurepassword'
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())

class UserRegistrationSerializerTests(TestCase):
    def test_registration_serializer_success(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        serializer = UserRegistrationSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('password123'))

    def test_registration_serializer_password_mismatch(self):
        payload = {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'password123',
            'password_confirm': 'differentpassword'
        }
        serializer = UserRegistrationSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', serializer.errors)

class UserStatsSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="statuser",
            email="stat@example.com",
            password="password123"
        )

    @patch('Myevol_app.models.user_model.User.mood_average')
    @patch('Myevol_app.models.user_model.User.entries_by_category')
    def test_user_stats_serializer_fields(self, mock_entries_by_category, mock_mood_average):
        mock_mood_average.return_value = 7
        mock_entries_by_category.return_value = {'Travail': 10, 'Santé': 5}
        serializer = UserStatsSerializer()
        output = serializer.to_representation(self.user)
        self.assertIn('mood_stats', output)
        self.assertIn('streak_stats', output)
        self.assertIn('activity_stats', output)
        self.assertIn('category_distribution', output)

class UserPreferencesSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="prefuser",
            email="pref@example.com",
            password="password123"
        )

    def test_user_preferences_serializer_default(self):
        preferences_data = {
            'dark_mode': True,
            'accent_color': '#FF0000',
            'font_choice': 'Arial',
            'enable_animations': False,
            'notif_badge': True,
            'notif_objectif': False,
            'notif_info': True,
            'notif_statistique': False
        }
        serializer = UserPreferencesSerializer(data=preferences_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        output = serializer.validated_data
        self.assertTrue(output['dark_mode'])
        self.assertEqual(output['accent_color'], '#FF0000')


class UserXpSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="xpuser",
            email="xp@example.com",
            password="password123"
        )

    def test_user_xp_serializer_add(self):
        context = {'user': self.user}
        payload = {'amount': 50}
        serializer = UserXpSerializer(data=payload, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save()
        self.assertEqual(result['amount_added'], 50)
        self.assertEqual(self.user.xp, 50)

    def test_user_xp_serializer_invalid_amount(self):
        payload = {'amount': -10}
        serializer = UserXpSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
