# services/quote_service.py

from datetime import timedelta
import hashlib
import random
from django.utils.timezone import now

from ..models.quote_model import Quote

def get_random_quote(mood_tag=None):
    """
    Retourne une citation aléatoire, optionnellement filtrée par mood_tag.
    
    Args:
        mood_tag (str, optional): Étiquette d'humeur pour filtrer les citations
        
    Returns:
        Quote: Une citation aléatoire ou None si aucune ne correspond
    """
    queryset = Quote.objects.all()
    if mood_tag:
        queryset = queryset.filter(mood_tag=mood_tag)
        
    count = queryset.count()
    if count == 0:
        return None
        
    random_index = random.randint(0, count - 1)
    return queryset[random_index]

def get_daily_quote(user=None):
    """
    Retourne la citation du jour, potentiellement personnalisée selon l'utilisateur.
    
    Args:
        user (User, optional): Utilisateur pour personnalisation basée sur son humeur
        
    Returns:
        Quote: Citation du jour
    """
    today = now().date().strftime("%Y%m%d")

    mood_filter = None
    if user:
        # Logique pour personnaliser la citation selon l'humeur de l'utilisateur
        from django.db.models import Avg
        recent_entries = user.entries.filter(created_at__gte=now() - timedelta(days=3))
        if recent_entries.exists():
            avg_mood = recent_entries.aggregate(avg=Avg('mood'))['avg']
            if avg_mood is not None:
                if avg_mood < 4:
                    mood_filter = 'low'
                elif avg_mood > 7:
                    mood_filter = 'positive'
                else:
                    mood_filter = 'neutral'
    
    quotes = Quote.objects.all()
    if mood_filter:
        quotes = quotes.filter(mood_tag=mood_filter)
        
    count = quotes.count()
    if count == 0:
        return None
    
    # Sélection déterministe de la citation du jour
    hash_obj = hashlib.md5(today.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    index = hash_int % count
    
    return quotes[index]
