from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from Myevol_app.models.notification_model import Notification
from Myevol_app.serializers.notification_serializers import (
    NotificationSerializer,
    NotificationListSerializer,
    NotificationCreateSerializer,
    NotificationUpdateSerializer,
    NotificationCountSerializer,
    NotificationBulkActionSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.notification = Notification.objects.create(
            user=self.user,
            message="Test notification",
            notif_type="info"
        )

    # --- Test NotificationSerializer ---
    def test_notification_serializer(self):
        serializer = NotificationSerializer(self.notification)
        data = serializer.data
        self.assertEqual(data['message'], "Test notification")
        self.assertEqual(data['notif_type'], "info")
        self.assertEqual(data['user_username'], "testuser")
        self.assertIn('time_since_created', data)

    # --- Test NotificationListSerializer ---
    def test_notification_list_serializer(self):
        serializer = NotificationListSerializer(self.notification)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'message', 'notif_type', 'type_display', 'is_read', 'created_at', 'time_since_created'})

    # --- Test NotificationCreateSerializer ---
from unittest.mock import patch

@patch('Myevol_app.models.notification_model.Notification.create_notification')
def test_notification_create_serializer_valid(self, mock_create_notification):
    payload = {
        'message': 'Nouvelle notif',
        'notif_type': 'warning',
    }
    context = {'user': self.user}
    serializer = NotificationCreateSerializer(data=payload, context=context)

    self.assertTrue(serializer.is_valid())
    
    mock_instance = Notification(
        user=self.user,
        message='Nouvelle notif',
        notif_type='warning'
    )
    mock_create_notification.return_value = mock_instance

    notif = serializer.save()

    self.assertEqual(notif.user, self.user)
    self.assertEqual(notif.message, 'Nouvelle notif')
    self.assertEqual(notif.notif_type, 'warning')

    # --- Test NotificationUpdateSerializer ---
    def test_notification_update_serializer_mark_as_read(self):
        payload = {'mark_as_read': True}
        serializer = NotificationUpdateSerializer(instance=self.notification, data=payload, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_notification_update_serializer_archive(self):
        payload = {'archive': True}
        serializer = NotificationUpdateSerializer(instance=self.notification, data=payload, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.archived)

    # --- Test NotificationCountSerializer ---
    def test_notification_count_serializer(self):
        serializer = NotificationCountSerializer(instance=self.user)
        data = serializer.data
        self.assertIn('total', data)
        self.assertIn('unread', data)
        self.assertIn('today', data)
        self.assertIn('by_type', data)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['unread'], 1)
        self.assertEqual(data['today'], 1)
        self.assertIn('info', data['by_type'])
        self.assertEqual(data['by_type']['info']['total'], 1)

    # --- Test NotificationBulkActionSerializer ---
    def test_bulk_action_mark_all_read(self):
        payload = {
            'action': 'mark_all_read',
            'notif_type': 'all'
        }
        context = {'user': self.user}
        serializer = NotificationBulkActionSerializer(data=payload, context=context)
        self.assertTrue(serializer.is_valid())
        result = serializer.save()
        self.assertTrue(result['success'])
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_bulk_action_archive_all(self):
        payload = {
            'action': 'archive_all',
            'notif_type': 'all'
        }
        context = {'user': self.user}
        serializer = NotificationBulkActionSerializer(data=payload, context=context)
        self.assertTrue(serializer.is_valid())
        result = serializer.save()
        self.assertTrue(result['success'])
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.archived)

    def test_bulk_action_archive_read(self):
        self.notification.mark_as_read()  # D'abord la rendre "read"
        payload = {
            'action': 'archive_read',
            'notif_type': 'all'
        }
        context = {'user': self.user}
        serializer = NotificationBulkActionSerializer(data=payload, context=context)
        self.assertTrue(serializer.is_valid())
        result = serializer.save()
        self.assertTrue(result['success'])
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.archived)

    def test_bulk_action_invalid_without_user(self):
        payload = {
            'action': 'archive_all',
            'notif_type': 'all'
        }
        serializer = NotificationBulkActionSerializer(data=payload, context={})  # pas d'utilisateur
        self.assertTrue(serializer.is_valid())
        with self.assertRaisesMessage(Exception, "L'utilisateur est requis pour cette action."):
            serializer.save()
