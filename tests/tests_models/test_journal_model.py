# tests/tests_models/test_journal_model.py

from datetime import timedelta
from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock
from freezegun import freeze_time

from Myevol_app.models import JournalEntry, JournalMedia

User = get_user_model()


class BaseUserTestMixin:
    def create_mock_user(self, username="testuser", email="test@example.com", password="testpass"):
        with patch('Myevol_app.models.user_model.User.create_default_preferences'):
            return User.objects.create_user(username=username, email=email, password=password)


class JournalEntryTests(TestCase, BaseUserTestMixin):
    def setUp(self):
        self.user = self.create_mock_user(username="journaluser", email="journal@example.com")
        self.entry = JournalEntry.objects.create(
            user=self.user,
            content="Test journal entry",
            mood=8,
            category="test"
        )

    def test_str_method(self):
        expected = f"{self.user.username} - {self.entry.created_at.date()}"
        self.assertEqual(str(self.entry), expected)

    def test_repr_method(self):
        repr_output = repr(self.entry)
        self.assertIn(f"id={self.entry.id}", repr_output)
        self.assertIn(f"user='{self.user.username}'", repr_output)
        self.assertIn(f"category='{self.entry.category}'", repr_output)

    @patch('Myevol_app.models.journal_model.reverse')
    def test_get_absolute_url(self, mock_reverse):
        mock_reverse.return_value = f"/journalentries/{self.entry.pk}/"
        url = self.entry.get_absolute_url()
        self.assertEqual(url, f"/journalentries/{self.entry.pk}/")

    def test_get_mood_emoji(self):
        for mood, emoji in JournalEntry.MOOD_EMOJIS.items():
            self.entry.mood = mood
            self.assertEqual(self.entry.get_mood_emoji(), emoji)

    def test_clean_validation(self):
        self.entry.content = "Hi"
        with self.assertRaises(ValidationError):
            self.entry.clean()

    @patch('Myevol_app.models.stats_model.DailyStat.generate_for_user')
    @patch('Myevol_app.services.challenge_service.check_challenges')
    @patch('Myevol_app.models.user_model.User.update_badges')
    @patch('Myevol_app.models.user_model.User.update_streaks')
    def test_save_method_triggers_updates(self, mock_update_streaks, mock_update_badges,
                                          mock_check_challenges, mock_generate_stats):
        new_entry = JournalEntry(
            user=self.user,
            content="New entry to test save",
            mood=7,
            category="save_test"
        )
        new_entry.save()

        mock_generate_stats.assert_called_with(self.user, new_entry.created_at.date())
        mock_check_challenges.assert_called_with(self.user)
        mock_update_badges.assert_called()
        mock_update_streaks.assert_called()

    @freeze_time("2025-04-22")
    def test_count_today(self):
        self.assertEqual(JournalEntry.count_today(self.user), 0)
        JournalEntry.objects.create(
            user=self.user,
            content="Entry today",
            mood=6,
            category="test"
        )
        self.assertEqual(JournalEntry.count_today(self.user), 1)

    @freeze_time("2025-04-22")
    def test_get_entries_by_date_range(self):
        today = now().date()
        yesterday = today - timedelta(days=1)

        JournalEntry.objects.create(user=self.user, content="Today", mood=7, category="now")
        with freeze_time("2025-04-21"):
            JournalEntry.objects.create(user=self.user, content="Yesterday", mood=5, category="past")

        entries_today = JournalEntry.get_entries_by_date_range(self.user, today, today)
        entries_both = JournalEntry.get_entries_by_date_range(self.user, yesterday, today)
        
        self.assertEqual(entries_today.count(), 1)
        self.assertEqual(entries_both.count(), 2)

    def test_get_category_suggestions(self):
        JournalEntry.objects.create(user=self.user, content="Work", mood=7, category="work")
        JournalEntry.objects.create(user=self.user, content="More work", mood=7, category="work")
        JournalEntry.objects.create(user=self.user, content="Personal", mood=6, category="personal")

        suggestions = JournalEntry.get_category_suggestions(self.user)
        self.assertEqual(suggestions[0], "work")
        self.assertIn("personal", suggestions)
        self.assertIn("test", suggestions)


class JournalMediaTests(TestCase, BaseUserTestMixin):
    def setUp(self):
        self.user = self.create_mock_user(username="mediauser", email="media@example.com")
        self.entry = JournalEntry.objects.create(
            user=self.user,
            content="Entry with media",
            mood=7,
            category="media_test"
        )

        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        self.media = JournalMedia.objects.create(
            entry=self.entry,
            file=self.image_file,
            type="image"
        )

    def test_str_method(self):
        expected = f"Image pour {self.entry}"
        self.assertEqual(str(self.media), expected)

    def test_file_url(self):
        mock_file = MagicMock()
        mock_file.url = 'http://example.com/test_image.jpg'

        self.media.file = mock_file  # Remplacer tout le `file` par un mock
        self.assertEqual(self.media.file_url(), 'http://example.com/test_image.jpg')

        empty_media = JournalMedia(entry=self.entry, type="image")
        self.assertIsNone(empty_media.file_url())


    def test_file_size(self):
        self.assertEqual(self.media.file_size(), len(b'file_content'))

        empty_media = JournalMedia(entry=self.entry, type="image")
        self.assertEqual(empty_media.file_size(), 0)

    def test_validate_file_type(self):
        with patch('mimetypes.guess_type', return_value=('image/jpeg', None)):
            self.media.validate_file_type()

        with patch('mimetypes.guess_type', return_value=('text/plain', None)):
            with self.assertRaises(ValidationError):
                self.media.validate_file_type()

        audio_media = JournalMedia(
            entry=self.entry,
            file=SimpleUploadedFile('test_audio.mp3', b'audio content', 'audio/mpeg'),
            type="audio"
        )
        with patch('mimetypes.guess_type', return_value=('audio/mpeg', None)):
            audio_media.validate_file_type()

        with patch('mimetypes.guess_type', return_value=('image/jpeg', None)):
            with self.assertRaises(ValidationError):
                audio_media.validate_file_type()
