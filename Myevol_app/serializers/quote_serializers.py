from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count

from ..models.quote_model import Quote


class QuoteSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Quote.
    
    Expose les citations inspirantes avec leurs métadonnées.
    """
    length = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'text', 'author', 'mood_tag', 'length'
        ]
    
    def get_length(self, obj):
        """Retourne la longueur du texte de la citation."""
        return obj.length()


class QuoteDetailSerializer(QuoteSerializer):
    """
    Serializer pour les détails d'une citation.
    
    Version étendue pour l'affichage détaillé d'une citation.
    """
    author_quote_count = serializers.SerializerMethodField()
    formatted_quote = serializers.SerializerMethodField()
    
    class Meta(QuoteSerializer.Meta):
        fields = QuoteSerializer.Meta.fields + ['author_quote_count', 'formatted_quote']
    
    def get_author_quote_count(self, obj):
        """Retourne le nombre de citations disponibles de cet auteur."""
        if not obj.author:
            return 0
        return Quote.objects.filter(author=obj.author).count()
    
    def get_formatted_quote(self, obj):
        """Retourne la citation formatée pour l'affichage."""
        author = obj.author if obj.author else "Inconnu"
        return {
            'text': obj.text,
            'author': author,
            'display': f'"{obj.text}" — {author}'
        }


class RandomQuoteSerializer(serializers.Serializer):
    """
    Serializer pour obtenir une citation aléatoire.
    
    Prend en charge un filtre de mood_tag optionnel.
    """
    mood_tag = serializers.CharField(required=False, allow_blank=True)
    
    def to_representation(self, instance):
        """
        Retourne une citation aléatoire selon le mood_tag spécifié.
        """
        mood_tag = instance.get('mood_tag')
        quote = Quote.get_random(mood_tag)
        
        if not quote:
            return {
                'success': False,
                'message': f"Aucune citation trouvée{f' avec le tag {mood_tag}' if mood_tag else ''}."
            }
            
        return {
            'success': True,
            'quote': QuoteDetailSerializer(quote).data
        }


class DailyQuoteSerializer(serializers.Serializer):
    """
    Serializer pour obtenir la citation du jour.
    
    Prend en charge une personnalisation selon l'utilisateur.
    """
    def to_representation(self, instance):
        """
        Retourne la citation du jour, potentiellement personnalisée.
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        quote = Quote.get_daily_quote(user if user and getattr(user, 'is_authenticated', False) else None)
        
        if not quote:
            return {
                'success': False,
                'message': "Aucune citation du jour disponible."
            }
            
        return {
            'success': True,
            'date': timezone.now().date().isoformat(),
            'quote': QuoteDetailSerializer(quote).data
        }


class AuthorListSerializer(serializers.Serializer):
    """
    Serializer pour obtenir la liste des auteurs avec leur nombre de citations.
    """
    
    def to_representation(self, instance):
        """
        Retourne la liste des auteurs disponibles avec des statistiques.
        """
        authors = Quote.get_authors_list()
        total_quotes = Quote.objects.count()
        unknown_quotes = Quote.objects.filter(author='').count()
        
        return {
            'success': True,
            'total_quotes': total_quotes,
            'unknown_author_quotes': unknown_quotes,
            'authors_count': len(authors),
            'authors': [{
                'name': author['author'],
                'quotes_count': author['count']
            } for author in authors]
        }


class MoodTagSerializer(serializers.Serializer):
    """
    Serializer pour obtenir la liste des mood_tags avec leur nombre de citations.
    """
    
    def to_representation(self, instance):
        """
        Retourne la liste des mood_tags disponibles avec des statistiques.
        """
        mood_tags = Quote.objects.values('mood_tag').annotate(
            count=Count('id')
        ).order_by('mood_tag')
        
        return {
            'success': True,
            'mood_tags': [{
                'tag': tag['mood_tag'] or 'untagged',
                'count': tag['count']
            } for tag in mood_tags]
        }


class QuoteSearchSerializer(serializers.Serializer):
    """
    Serializer pour rechercher des citations.
    """
    query = serializers.CharField(required=True)
    author = serializers.CharField(required=False, allow_blank=True)
    mood_tag = serializers.CharField(required=False, allow_blank=True)
    
    def to_representation(self, instance):
        """
        Effectue une recherche dans les citations selon les critères fournis.
        """
        query = instance.get('query', '').strip()
        author = instance.get('author', '').strip()
        mood_tag = instance.get('mood_tag', '').strip()
        
        if not query and not author and not mood_tag:
            return {
                'success': False,
                'message': "Veuillez fournir au moins un critère de recherche."
            }
        
        quotes = Quote.objects.all()
        
        if query:
            quotes = quotes.filter(text__icontains=query)
        
        if author:
            quotes = quotes.filter(author__icontains=author)
        
        if mood_tag:
            quotes = quotes.filter(mood_tag=mood_tag)
        
        results = quotes.order_by('author') if quotes.exists() else Quote.objects.none()
        
        return {
            'success': True,
            'count': results.count(),
            'results': QuoteSerializer(results, many=True).data
        }
