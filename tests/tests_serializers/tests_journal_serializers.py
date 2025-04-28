from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta

from Myevol_app.models.journal_model import JournalEntry, JournalMedia
from Myevol_app.serializers.journal_serializers import (
    JournalMediaSerializer,
    JournalEntrySerializer,
    JournalEntryDetailSerializer,
    JournalEntryCreateSerializer,
    JournalEntryCalendarSerializer,
    JournalStatsSerializer,
    CategorySuggestionSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class TestJournalSerializers(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.entry = JournalEntry.objects.create(
            user=self.user,
            content="Contenu de test",
            mood=7,
            category="Travail"
        )
        self.media = JournalMedia.objects.create(
            entry=self.entry,
            file=SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg'),
            type='image'
        )

    # --- Tests JournalMedia ---
    def test_journal_media_serializer(self):
        serializer = JournalMediaSerializer(self.media)
        data = serializer.data
        self.assertEqual(data['type'], 'image')
        self.assertIn('file_url', data)
        self.assertIn('file_size', data)

    # --- Tests JournalEntry (simple) ---
    def test_journal_entry_serializer(self):
        serializer = JournalEntrySerializer(self.entry)
        data = serializer.data
        self.assertEqual(data['content'], self.entry.content)
        self.assertEqual(data['mood'], 7)
        self.assertEqual(data['category'], "Travail")
        self.assertEqual(data['user_username'], "testuser")
        self.assertIn('mood_emoji', data)
        self.assertIn('time_since_creation', data)

    # --- Tests JournalEntryDetail (plus d'infos) ---
    def test_journal_entry_detail_serializer(self):
        serializer = JournalEntryDetailSerializer(self.entry)
        data = serializer.data
        self.assertIn('is_editable', data)
        self.assertIn('day_entries_count', data)

    def test_is_editable_true(self):
        self.entry.created_at = timezone.now() - timedelta(hours=5)
        self.entry.save()
        serializer = JournalEntryDetailSerializer(self.entry)
        self.assertTrue(serializer.data['is_editable'])

    def test_is_editable_false(self):
        self.entry.created_at = timezone.now() - timedelta(days=2)
        self.entry.save()
        serializer = JournalEntryDetailSerializer(self.entry)
        self.assertFalse(serializer.data['is_editable'])

    # --- Tests JournalEntryCreate (entrée avec média) ---
    def test_journal_entry_create_serializer_valid(self):
        payload = {
            'content': "Nouvelle entrée",
            'mood': 8,
            'category': "Santé",
            'media_files': [SimpleUploadedFile('audio.mp3', b'music_test.mp4', content_type='audio/mpeg')],
            'media_types': ['audio']
        }
        context = {'request': type('Request', (), {'user': self.user})()}
        serializer = JournalEntryCreateSerializer(data=payload, context=context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_journal_entry_create_serializer_invalid_media_mismatch(self):
        payload = {
            'content': "Mismatch entrée",
            'mood': 5,
            'category': "Sport",
            'media_files': [SimpleUploadedFile('img.jpg', b'testcontent', content_type='image/jpeg')
],
            'media_types': []  # mismatch volontaire
        }
        context = {'request': type('Request', (), {'user': self.user})()}
        serializer = JournalEntryCreateSerializer(data=payload, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_journal_entry_create_min_content_validation(self):
        payload = {
            'content': "abc",
            'mood': 5,
            'category': "Test",
        }
        context = {'request': type('Request', (), {'user': self.user})()}
        serializer = JournalEntryCreateSerializer(data=payload, context=context)
        self.assertFalse(serializer.is_valid())

    # --- Tests JournalEntryCalendar ---
    def test_journal_entry_calendar_serializer(self):
        # Créer une entrée qui sera utilisée pour simuler le calendrier
        entry = JournalEntry.objects.create(
            user=self.user,
            content="Entrée calendrier",
            mood=7,
            category="Vie"
        )

        # Annoter l'entrée manuellement pour simuler le queryset que le serializer attendrait
        entry.day = entry.created_at.date()
        entry.count = 1
        entry.mood_avg = 7.0
        entry.categories = ["Vie"]

        serializer = JournalEntryCalendarSerializer(instance=entry)
        serialized = serializer.data

        self.assertIn('day', serialized)
        self.assertEqual(serialized['day'], entry.day)
        self.assertIn('count', serialized)
        self.assertEqual(serialized['count'], 1)
        self.assertIn('mood_avg', serialized)
        self.assertEqual(serialized['mood_avg'], 7.0)
        self.assertIn('categories', serialized)
        self.assertEqual(serialized['categories'], ["Vie"])

    # --- Tests JournalStats ---
    def test_journal_stats_serializer(self):
        serializer = JournalStatsSerializer(instance=self.user)
        data = serializer.data
        self.assertIn('total_entries', data)
        self.assertIn('entries_per_category', data)
        self.assertIn('mood_distribution', data)
        self.assertIn('monthly_entries', data)
        self.assertIn('average_mood', data)
        self.assertIn('entries_streak', data)

    def test_journal_stats_entries_streak_empty(self):
        user = User.objects.create_user(username="emptyuser", email="empty@example.com", password="password")
        serializer = JournalStatsSerializer(instance=user)
        data = serializer.data
        self.assertEqual(data['entries_streak']['current'], 0)

    # --- Tests CategorySuggestion ---
    def test_category_suggestion_serializer(self):
        serializer = CategorySuggestionSerializer(instance=self.user)
        data = serializer.data
        self.assertIn('categories', data)
        self.assertIsInstance(data['categories'], list)

    def test_category_suggestion_empty(self):
        new_user = User.objects.create_user(username="newbie", email="newbie@example.com", password="password")
        serializer = CategorySuggestionSerializer(instance=new_user)
        data = serializer.data
        self.assertEqual(data['categories'], [])

from unittest.mock import patch
import datetime


from unittest.mock import patch
import datetime

class TestJournalStreaksWithMock(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mockuser", email="mock@example.com", password="password")

    @patch('django.utils.timezone.now')
    def test_streak_active_mocked_dates(self, mock_now):
        today = datetime.date.today()

        for delta in range(3):
            fake_date = today - datetime.timedelta(days=delta)
            fake_datetime = timezone.make_aware(datetime.datetime.combine(fake_date, datetime.time.min))
            mock_now.return_value = fake_datetime

            entry = JournalEntry.objects.create(
                user=self.user,
                content=f"Entry -{delta}",
                mood=7,
                category="Test",
                created_at=fake_datetime  # ✅ Set directement à la création
            )

        # Ne pas mocker maintenant (on utilise la vraie date pour la validation)
        mock_now.return_value = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))

        serializer = JournalStatsSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['entries_streak']['current'], 3)
        self.assertEqual(data['entries_streak']['max'], 3)
        self.assertTrue(data['entries_streak']['current_active'])

    @patch('django.utils.timezone.now')
    def test_streak_interrupted_mocked_dates(self, mock_now):
        today = datetime.date.today()

        for delta in [2, 5]:
            fake_date = today - datetime.timedelta(days=delta)
            fake_datetime = timezone.make_aware(datetime.datetime.combine(fake_date, datetime.time.min))
            mock_now.return_value = fake_datetime

            entry = JournalEntry.objects.create(
                user=self.user,
                content=f"Break Entry -{delta}",
                mood=6,
                category="Break",
                created_at=fake_datetime
            )

        mock_now.return_value = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))

        serializer = JournalStatsSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['entries_streak']['current'], 0)
        self.assertEqual(data['entries_streak']['max'], 1)

    @patch('django.utils.timezone.now')
    def test_long_streak_mocked_dates(self, mock_now):
        today = datetime.date.today()

        for delta in range(7):
            fake_date = today - datetime.timedelta(days=delta)
            fake_datetime = timezone.make_aware(datetime.datetime.combine(fake_date, datetime.time.min))
            mock_now.return_value = fake_datetime

            entry = JournalEntry.objects.create(
                user=self.user,
                content=f"Streak Entry -{delta}",
                mood=7,
                category="Test",
                created_at=fake_datetime
            )

        mock_now.return_value = timezone.make_aware(datetime.datetime.combine(today, datetime.time.min))

        serializer = JournalStatsSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['entries_streak']['current'], 7)
        self.assertEqual(data['entries_streak']['max'], 7)
        self.assertTrue(data['entries_streak']['current_active'])
