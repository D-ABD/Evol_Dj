# tests/tests_serializers/test_event_log_serializers.py

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from Myevol_app.models.event_log_model import EventLog
from Myevol_app.serializers.event_log_serializers import (
    EventLogSerializer, 
    EventLogDetailSerializer, 
    EventLogStatisticsSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class TestEventLogSerializers(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour les tests
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        
        # Création de quelques événements
        self.event1 = EventLog.objects.create(
            user=self.user,
            action='login',
            description='User logged in',
            severity='info'
        )
        self.event2 = EventLog.objects.create(
            user=self.user,
            action='attribution_badge',
            description='Badge earned',
            severity='success',
            metadata={'badge_id': 1, 'badge_name': 'Starter'}
        )
        self.event3 = EventLog.objects.create(
            user=self.user,
            action='defi_termine',
            description='Challenge completed',
            severity='success',
            metadata={'challenge_id': 5}
        )

    def test_eventlog_serializer_basic(self):
        """Test de EventLogSerializer simple"""
        serializer = EventLogSerializer(self.event1)
        data = serializer.data
        self.assertEqual(data['action'], 'login')
        self.assertIn('temps_écoulé', data)
        self.assertIn('résumé', data)

    def test_eventlog_detail_serializer_valid_metadata(self):
        """Test EventLogDetailSerializer avec metadata valide"""
        serializer = EventLogDetailSerializer(self.event2)
        data = serializer.data
        self.assertEqual(data['action'], 'attribution_badge')
        self.assertTrue(data['has_metadata'])
        self.assertIn('badge attribué', data['formatted_metadata']['formatted'].lower())

    def test_eventlog_detail_serializer_invalid_metadata(self):
        """Test EventLogDetailSerializer avec metadata non valide"""
        event_invalid = EventLog.objects.create(
            user=self.user,
            action='login',
            description='No metadata',
            severity='info',
            metadata=None
        )
        serializer = EventLogDetailSerializer(event_invalid)
        data = serializer.data
        self.assertFalse(data['has_metadata'])
        self.assertIsNone(data['formatted_metadata'])

    def test_eventlog_statistics_serializer(self):
        """Test EventLogStatisticsSerializer"""
        input_data = {'user': self.user, 'period_days': 30}
        serializer = EventLogStatisticsSerializer(input_data)
        stats = serializer.data
        
        self.assertGreaterEqual(stats['total_events'], 3)
        self.assertIn('login', stats['events_by_action'])
        self.assertIn('success', stats['events_by_severity'])
        self.assertIn('last_24h', stats['events_by_time'])
        self.assertLessEqual(len(stats['most_recent']), 5)

    def test_eventlog_statistics_serializer_no_user(self):
        """Test EventLogStatisticsSerializer sans utilisateur"""
        input_data = {'period_days': 30}
        serializer = EventLogStatisticsSerializer(input_data)
        stats = serializer.data
        
        self.assertGreaterEqual(stats['total_events'], 3)

    def test_eventlog_serializer_time_human_readable(self):
        """Test affichage humain du temps écoulé"""
        self.event1.created_at = timezone.now() - timedelta(days=2)
        self.event1.save()
        serializer = EventLogSerializer(self.event1)
        human_time = serializer.data['temps_écoulé']['human_format']
        self.assertIn("il y a 2 jours", human_time)

