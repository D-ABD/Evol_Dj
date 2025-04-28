from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, MagicMock
from Myevol_app.models.quote_model import Quote
from Myevol_app.serializers.quote_serializers import (
    QuoteSerializer,
    QuoteDetailSerializer,
    RandomQuoteSerializer,
    DailyQuoteSerializer,
    AuthorListSerializer,
    MoodTagSerializer,
    QuoteSearchSerializer
)

class QuoteSerializerTests(TestCase):
    def setUp(self):
        self.quote = Quote.objects.create(
            text="La vie est belle",
            author="Anonyme",
            mood_tag="positif"
        )

    def test_quote_serializer(self):
        serializer = QuoteSerializer(self.quote)
        data = serializer.data
        self.assertEqual(data['text'], "La vie est belle")
        self.assertEqual(data['author'], "Anonyme")
        self.assertEqual(data['mood_tag'], "positif")
        self.assertEqual(data['length'], len(self.quote.text))

    def test_quote_detail_serializer(self):
        serializer = QuoteDetailSerializer(self.quote)
        data = serializer.data
        self.assertIn('author_quote_count', data)
        self.assertIn('formatted_quote', data)
        self.assertEqual(data['formatted_quote']['text'], self.quote.text)
        self.assertEqual(data['formatted_quote']['author'], self.quote.author)

    @patch('Myevol_app.models.quote_model.Quote.get_random')
    def test_random_quote_serializer_success(self, mock_get_random):
        mock_get_random.return_value = self.quote
        serializer = RandomQuoteSerializer()
        output = serializer.to_representation({'mood_tag': 'positif'})
        self.assertTrue(output['success'])
        self.assertIn('quote', output)

    @patch('Myevol_app.models.quote_model.Quote.get_random')
    def test_random_quote_serializer_failure(self, mock_get_random):
        mock_get_random.return_value = None
        serializer = RandomQuoteSerializer()
        output = serializer.to_representation({'mood_tag': 'unknown'})
        self.assertFalse(output['success'])
        self.assertIn('message', output)

    @patch('Myevol_app.models.quote_model.Quote.get_daily_quote')
    def test_daily_quote_serializer_success(self, mock_get_daily):
        mock_get_daily.return_value = self.quote
        mock_user = MagicMock()
        mock_user.is_authenticated = True

        serializer = DailyQuoteSerializer(context={'request': MagicMock(user=mock_user)})
        output = serializer.to_representation({})
        self.assertTrue(output['success'])
        self.assertIn('quote', output)

    @patch('Myevol_app.models.quote_model.Quote.get_daily_quote')
    def test_daily_quote_serializer_failure(self, mock_get_daily):
        mock_get_daily.return_value = None
        mock_user = MagicMock()
        mock_user.is_authenticated = False

        serializer = DailyQuoteSerializer(context={'request': MagicMock(user=mock_user)})
        output = serializer.to_representation({})
        self.assertFalse(output['success'])
        self.assertIn('message', output)

    @patch('Myevol_app.models.quote_model.Quote.get_authors_list')
    def test_author_list_serializer(self, mock_get_authors_list):
        mock_get_authors_list.return_value = [{'author': 'Anonyme', 'count': 1}]
        serializer = AuthorListSerializer()
        output = serializer.to_representation({})
        self.assertTrue(output['success'])
        self.assertEqual(output['authors'][0]['name'], 'Anonyme')
        self.assertEqual(output['authors'][0]['quotes_count'], 1)

    def test_mood_tag_serializer(self):
        serializer = MoodTagSerializer()
        output = serializer.to_representation({})
        self.assertTrue(output['success'])
        self.assertIn('mood_tags', output)

    def test_quote_search_serializer_by_query(self):
        serializer = QuoteSearchSerializer()
        output = serializer.to_representation({'query': 'vie'})
        self.assertTrue(output['success'])
        self.assertGreaterEqual(output['count'], 1)
        self.assertIn('results', output)

    def test_quote_search_serializer_no_criteria(self):
        serializer = QuoteSearchSerializer()
        output = serializer.to_representation({'query': '', 'author': '', 'mood_tag': ''})
        self.assertFalse(output['success'])
        self.assertIn('message', output)
