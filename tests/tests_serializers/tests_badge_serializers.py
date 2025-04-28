from django.test import TestCase
from django.utils import timezone
from Myevol_app.models.badge_model import Badge, BadgeTemplate
from Myevol_app.models.user_model import User
from Myevol_app.serializers.badge_serializers import (
    BadgeSerializer, 
    BadgeTemplateSerializer, 
    BadgeTemplateWithProgressSerializer
)

class BadgeSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.badge = Badge.objects.create(
            user=self.user,
            name="Premier Pas",
            description="Félicitations pour votre première entrée !",
            icon="premier_pas.png",
            level=1,
            date_obtenue=timezone.now()
        )
        self.badge_template = BadgeTemplate.objects.create(
            name="Niveau 1",
            description="Atteindre le niveau 1",
            icon="niveau1.png",
            condition="xp >= 100",
            level=1,
            animation_url="anim1.gif",
            color_theme="#FFD700"
        )

    def test_badge_serializer_fields(self):
        serializer = BadgeSerializer(instance=self.badge)
        data = serializer.data

        self.assertEqual(data["name"], "Premier Pas")
        self.assertEqual(data["user_username"], "testuser")
        self.assertIn("was_earned_today", data)
        self.assertIn("days_since_earned", data)

    def test_badge_template_serializer_fields(self):
        serializer = BadgeTemplateSerializer(instance=self.badge_template)
        data = serializer.data

        self.assertEqual(data["name"], "Niveau 1")
        self.assertIn("level_number", data)

    def test_badge_template_with_progress_serializer(self):
        serializer = BadgeTemplateWithProgressSerializer(instance=self.badge_template, context={'request': None})
        data = serializer.data

        self.assertIn("progress", data)
        self.assertIn("can_unlock", data)
        self.assertIn("is_unlocked", data)

    def test_badge_serializer_invalid_data(self):
        """Teste que le BadgeSerializer refuse les données invalides."""
        invalid_data = {
            'name': '',  # Le champ obligatoire est vide
            'description': 'Pas de nom de badge',
        }
        serializer = BadgeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
