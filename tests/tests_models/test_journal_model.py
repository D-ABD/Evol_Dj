from unittest import mock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from ..models import JournalEntry, JournalMedia

User = get_user_model()

class JournalEntryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")

    def test_create_valid_entry(self):
        entry = JournalEntry.objects.create(user=self.user, mood=7, category="travail", content="Une bonne journée")
        self.assertEqual(entry.mood, 7)

    def test_str_method(self):
        entry = JournalEntry.objects.create(user=self.user, mood=5, content="Test", category="perso")
        self.assertIn(self.user.username, str(entry))

    def test_get_mood_emoji(self):
        entry = JournalEntry.objects.create(user=self.user, mood=10, content="Test", category="perso")
        self.assertEqual(entry.get_mood_emoji(), "😍")

    def test_clean_content_too_short(self):
        entry = JournalEntry(user=self.user, mood=6, content="yo", category="rapide")
        with self.assertRaises(ValidationError):
            entry.clean()

    def test_count_today(self):
        JournalEntry.objects.create(user=self.user, mood=6, content="ok super", category="cool")
        self.assertEqual(JournalEntry.count_today(self.user), 1)

    def test_get_entries_by_date_range(self):
        today = now().date()
        JournalEntry.objects.create(user=self.user, mood=5, content="1", category="a")
        results = JournalEntry.get_entries_by_date_range(self.user, today, today)
        self.assertEqual(results.count(), 1)

    def test_get_category_suggestions(self):
        JournalEntry.objects.create(user=self.user, mood=5, content="test1", category="sport")
        JournalEntry.objects.create(user=self.user, mood=5, content="test2", category="sport")
        JournalEntry.objects.create(user=self.user, mood=5, content="test3", category="lecture")
        suggestions = JournalEntry.get_category_suggestions(self.user)
        self.assertEqual(suggestions[0], "sport")



    @patch("Myevol_app.models.stats_model.DailyStat.generate_for_user")
    @patch("Myevol_app.models.challenge_model.check_challenges")
    @patch("Myevol_app.models.user_model.User.update_badges")
    @patch("Myevol_app.models.user_model.User.update_streaks")
    def test_save_triggers_updates(self, mock_streaks, mock_badges, mock_check, mock_stats):
        JournalEntry.objects.create(user=self.user, mood=6, content="Exemple valide", category="dev")
        
        mock_stats.assert_any_call(self.user, mock.ANY)
        mock_check.assert_called_once()
        mock_stats.assert_called()
        mock_streaks.assert_called_once()


class JournalMediaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mediauser", password="pass")
        self.entry = JournalEntry.objects.create(user=self.user, mood=6, content="Content ok", category="notes")

    def test_str_method(self):
        file = SimpleUploadedFile("test.jpg", b"filecontent", content_type="image/jpeg")
        media = JournalMedia.objects.create(entry=self.entry, file=file, type="image")
        self.assertIn("Image", str(media))


    @patch("mimetypes.guess_type", return_value=("image/jpeg", None))
    def test_validate_file_type_image_valid(self, mock_mime):
        file = SimpleUploadedFile("test.jpg", b"abc", content_type="image/jpeg")
        media = JournalMedia(entry=self.entry, file=file, type="image")
        media.validate_file_type()  # ne doit pas lever d'erreur

    @patch("mimetypes.guess_type", return_value=("application/pdf", None))
    def test_validate_file_type_invalid_image(self, mock_mime):
        file = SimpleUploadedFile("test.pdf", b"abc", content_type="application/pdf")
        media = JournalMedia(entry=self.entry, file=file, type="image")
        with self.assertRaises(ValidationError):
            media.validate_file_type()

    def test_file_url_and_size(self):
        # Crée une entrée
        entry = JournalEntry.objects.create(user=self.user, mood=5, content="Test", category="test")
        
        # Fichier mock
        fake_file = SimpleUploadedFile("test.jpg", b"filecontent", content_type="image/jpeg")
        
        media = JournalMedia.objects.create(entry=entry, file=fake_file, type="image")

        self.assertTrue(media.file_url().endswith(".jpg"))
        self.assertEqual(media.file_size(), len(b"filecontent"))