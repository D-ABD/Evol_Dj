from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from Myevol_app.models.objective_model import Objective
from Myevol_app.serializers.objective_serializers import (
    ObjectiveSerializer,
    ObjectiveListSerializer,
    ObjectiveDetailSerializer,
    ObjectiveCompleteSerializer,
    ObjectiveStatsSerializer,
    ObjectiveUpcomingSerializer,
    ObjectiveCategorySerializer,
)

User = get_user_model()

class ObjectiveSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.objective = Objective.objects.create(
            user=self.user,
            title='Devenir meilleur',
            category='Santé',
            done=False,
            target_date=timezone.now().date() + timedelta(days=5),
            target_value=10,
        )

    # --- Tests ObjectiveSerializer ---
    def test_objective_serializer_fields(self):
        serializer = ObjectiveSerializer(self.objective)
        data = serializer.data
        self.assertEqual(data['title'], 'Devenir meilleur')
        self.assertEqual(data['category'], 'Santé')
        self.assertEqual(data['user_username'], 'testuser')
        self.assertIn('progress_percent', data)
        self.assertIn('days_remaining', data)
        self.assertIn('status', data)

    def test_objective_serializer_status_logic(self):
        # done = False, pas en retard => "upcoming"
        serializer = ObjectiveSerializer(self.objective)
        self.assertEqual(serializer.data['status'], 'upcoming')

        # done = True => "completed"
        self.objective.done = True
        self.objective.save()
        serializer = ObjectiveSerializer(self.objective)
        self.assertEqual(serializer.data['status'], 'completed')

    def test_objective_serializer_target_date_validation(self):
        past_date = timezone.now().date() - timedelta(days=1)
        serializer = ObjectiveSerializer(data={
            'title': 'Objectif passé',
            'category': 'Test',
            'target_date': past_date,
            'target_value': 10,
            'done': False,
        }, context={'request': type('Request', (), {'user': self.user})()})

        self.assertFalse(serializer.is_valid())
        self.assertIn('target_date', serializer.errors)

    # --- Tests ObjectiveListSerializer ---
    def test_objective_list_serializer_fields(self):
        serializer = ObjectiveListSerializer(self.objective)
        data = serializer.data
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('status', data)
        self.assertNotIn('user_username', data)  # pas affiché

    # --- Tests ObjectiveDetailSerializer ---
    def test_objective_detail_serializer_fields(self):
        serializer = ObjectiveDetailSerializer(self.objective)
        data = serializer.data
        self.assertIn('formatted_target_date', data)
        self.assertIn('time_until_due', data)

    # --- Tests ObjectiveCompleteSerializer ---
    def test_objective_complete_serializer_update(self):
        serializer = ObjectiveCompleteSerializer(instance=self.objective, data={'done': True})
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertTrue(obj.done)

    # --- Tests ObjectiveStatsSerializer ---
    def test_objective_stats_serializer(self):
        serializer = ObjectiveStatsSerializer(instance=self.user)
        data = serializer.data
        self.assertIn('total', data)
        self.assertIn('completed', data)
        self.assertIn('completion_rate', data)
        self.assertIn('overdue', data)
        self.assertIn('by_category', data)
        self.assertIn('upcoming_today', data)
        self.assertIn('upcoming_week', data)
        self.assertIn('recent_completions', data)

    # --- Tests ObjectiveUpcomingSerializer ---
    def test_objective_upcoming_serializer(self):
        serializer = ObjectiveUpcomingSerializer(instance=self.user)
        data = serializer.data
        self.assertIn('today', data)
        self.assertIn('this_week', data)
        self.assertIn('this_month', data)

    # --- Tests ObjectiveCategorySerializer ---
    def test_objective_category_serializer(self):
        serializer = ObjectiveCategorySerializer(instance=self.user)
        data = serializer.data
        self.assertIn('categories', data)
        self.assertIsInstance(data['categories'], list)
        self.assertIn('Santé', data['categories'])

