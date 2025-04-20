from django.test import TestCase
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from Myevol_app.models.quote_model import Quote
from Myevol_app.models.journal_model import JournalEntry

User = get_user_model()

class QuoteModelTests(TestCase):
    def setUp(self):
        # Créer quelques citations pour les tests
        self.quote1 = Quote.objects.create(
            text="La vie est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.",
            author="Albert Einstein",
            mood_tag="positive"
        )
        
        self.quote2 = Quote.objects.create(
            text="Le succès, c'est d'aller d'échec en échec sans perdre son enthousiasme.",
            author="Winston Churchill",
            mood_tag="neutral"
        )
        
        self.quote3 = Quote.objects.create(
            text="Il n'y a pas de problèmes, il n'y a que des solutions.",
            author="André Gide",
            mood_tag="positive"
        )
        
        self.quote4 = Quote.objects.create(
            text="La vie est trop courte pour être petite.",
            author="",  # Auteur vide pour tester
            mood_tag="neutral"
        )
        
        # Créer un utilisateur pour tester get_daily_quote
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

    def test_str_representation_with_author(self):
        """Test de la représentation en chaîne pour citation avec auteur"""
        self.assertEqual(str(self.quote1), '"La vie est comme une bicyclette, il faut avancer pour ne pas perdre l\'équilibre." — Albert Einstein')

    def test_str_representation_without_author(self):
        """Test de la représentation en chaîne pour citation sans auteur"""
        self.assertEqual(str(self.quote4), '"La vie est trop courte pour être petite."')

    def test_length_calculation(self):
        """Test du calcul de la longueur de la citation"""
        self.assertEqual(self.quote1.length(), len(self.quote1.text))
        self.assertEqual(self.quote4.length(), len(self.quote4.text))

    def test_get_random_no_filter(self):
        """Test de l'obtention d'une citation aléatoire sans filtre"""
        quote = Quote.get_random()
        self.assertIsNotNone(quote)
        self.assertIn(quote, Quote.objects.all())

    def test_get_random_with_mood_filter(self):
        """Test de l'obtention d'une citation aléatoire avec filtre d'humeur"""
        quote = Quote.get_random(mood_tag="positive")
        self.assertIsNotNone(quote)
        self.assertEqual(quote.mood_tag, "positive")

    def test_get_random_with_nonexistent_mood(self):
        """Test avec un filtre d'humeur qui ne correspond à aucune citation"""
        quote = Quote.get_random(mood_tag="nonexistent")
        self.assertIsNone(quote)

    def test_get_daily_quote_consistency(self):
        """Test que la citation du jour est consistante pour une même date"""
        quote1 = Quote.get_daily_quote()
        quote2 = Quote.get_daily_quote()
        self.assertEqual(quote1, quote2)

    def test_daily_quote_with_user_no_entries(self):
        """Test de la citation du jour avec un utilisateur sans entrées"""
        quote = Quote.get_daily_quote(user=self.user)
        self.assertIsNotNone(quote)

    def test_daily_quote_with_user_mood(self):
        """Test de la citation du jour personnalisée selon l'humeur de l'utilisateur"""
        # Créer des entrées avec humeur élevée
        for _ in range(3):
            JournalEntry.objects.create(
                user=self.user,
                content="Test entry",
                mood=9,  # Humeur élevée > 7
                category="Test"
            )
        
        # La citation devrait avoir un mood_tag "positive"
        quote = Quote.get_daily_quote(user=self.user)
        
        # Si des citations avec mood_tag "positive" existent, celle retournée devrait être positive
        if Quote.objects.filter(mood_tag="positive").exists():
            self.assertEqual(quote.mood_tag, "positive")

    def test_get_authors_list(self):
        """Test de l'obtention de la liste des auteurs"""
        authors = Quote.get_authors_list()
        
        # Vérifier que la structure est correcte
        self.assertIsInstance(authors, list)
        self.assertTrue(len(authors) > 0)
        
        # Vérifier que chaque élément a les champs attendus
        for author_info in authors:
            self.assertIn('author', author_info)
            self.assertIn('count', author_info)
        
        # Vérifier que Einstein et Churchill sont présents
        einstein = next((a for a in authors if a['author'] == 'Albert Einstein'), None)
        churchill = next((a for a in authors if a['author'] == 'Winston Churchill'), None)
        
        self.assertIsNotNone(einstein)
        self.assertIsNotNone(churchill)
        self.assertEqual(einstein['count'], 1)
        self.assertEqual(churchill['count'], 1)
        
        # Vérifier que les auteurs vides ne sont pas inclus
        empty_authors = [a for a in authors if a['author'] == '']
        self.assertEqual(len(empty_authors), 0)