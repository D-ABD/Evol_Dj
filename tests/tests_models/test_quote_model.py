# tests/tests_models/test_quote_model.py
from django.test import TestCase
from django.utils.timezone import now
from datetime import datetime
from unittest.mock import patch
import hashlib

from Myevol_app.models import Quote

class QuoteModelTests(TestCase):
    def setUp(self):
        self.quote1 = Quote.objects.create(
            text="La vie est belle",
            author="Un philosophe",
            mood_tag="positive"
        )
        self.quote2 = Quote.objects.create(
            text="C'est compliqué",
            author="Un autre philosophe",
            mood_tag="neutral"
        )
        
    def test_str_method(self):
        expected = '"La vie est belle" — Un philosophe'
        self.assertEqual(str(self.quote1), expected)
        
    def test_length(self):
        self.assertEqual(self.quote1.length(), len("La vie est belle"))
        
    def test_get_random(self):
        # Test sans filtre
        random_quote = Quote.get_random()
        self.assertIn(random_quote, [self.quote1, self.quote2])
        
        # Test avec filtre
        positive_quote = Quote.get_random(mood_tag="positive")
        self.assertEqual(positive_quote, self.quote1)
        
    def test_get_random_empty(self):
        # Test avec un tag inexistant
        none_quote = Quote.get_random(mood_tag="inexistant")
        self.assertIsNone(none_quote)
        
    def test_get_daily_quote(self):
        # Sans filtre d'utilisateur
        with patch('datetime.date') as mock_date:
            # Fixe la date pour un hash déterministe
            mock_date.today.return_value = datetime(2025, 4, 21).date()
            
            daily_quote = Quote.get_daily_quote()
            # On ne peut pas prédire exactement lequel sera choisi, mais on sait qu'il devrait être dans notre ensemble
            self.assertIn(daily_quote, [self.quote1, self.quote2])
            
            # Vérifier la consistence (même hash = même citation chaque jour)
            second_call = Quote.get_daily_quote()
            self.assertEqual(daily_quote, second_call)

    def test_get_authors_list(self):
        authors = Quote.get_authors_list()
        self.assertEqual(len(authors), 2)  # 2 auteurs distincts créés
        author_names = [author['author'] for author in authors]
        self.assertIn("Un philosophe", author_names)
        self.assertIn("Un autre philosophe", author_names)
