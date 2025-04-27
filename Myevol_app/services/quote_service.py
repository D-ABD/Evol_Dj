# services/quote_service.py

import hashlib
import random
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Avg

from ..models.quote_model import Quote

def get_random_quote(mood_tag=None):
    """
    Retourne une citation aléatoire, optionnellement filtrée par une étiquette d'humeur.

    Args:
        mood_tag (str, optional): Étiquette d'humeur (ex: 'positive', 'low', 'neutral')

    Returns:
        Quote or None: Une instance aléatoire de Quote, ou None s’il n’en existe aucune
    """
    queryset = Quote.objects.all()
    if mood_tag:
        queryset = queryset.filter(mood_tag=mood_tag)

    count = queryset.count()
    if count == 0:
        return None

    return queryset[random.randint(0, count - 1)]

def get_daily_quote(user=None):
    """
    Retourne la citation du jour, personnalisée selon l'utilisateur s'il est fourni.

    - Utilise la date du jour comme graine pour sélectionner une citation unique et stable chaque jour.
    - Si un utilisateur est fourni, adapte la citation à son humeur moyenne des 3 derniers jours.

    Args:
        user (User, optional): L’utilisateur connecté (pour personnalisation via mood_tag)

    Returns:
        Quote or None: Une citation du jour (filtrée si besoin), ou None si aucune citation disponible
    """
    today = now().date().strftime("%Y%m%d")
    mood_filter = None

    if user:
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

    queryset = Quote.objects.all()
    if mood_filter:
        queryset = queryset.filter(mood_tag=mood_filter)

    count = queryset.count()
    if count == 0:
        return None

    # Hash déterministe basé sur la date
    hash_int = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = hash_int % count
    return queryset[index]
