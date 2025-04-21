# services/user_stats_service.py

from datetime import timedelta
from django.db import models
from django.db.models import Avg, Count
from django.utils.timezone import now
from django.db.models.functions import TruncDate

def compute_mood_average(entries, days=7, reference_date=None):
    """
    Calcule la moyenne d'humeur sur les X derniers jours.

    Args:
        entries: Les entrées de journal de l'utilisateur
        days (int): Nombre de jours à considérer
        reference_date (date): Date de référence

    Returns:
        float: Moyenne d'humeur arrondie à 1 décimale
    """
    if reference_date is None:
        reference_date = now()
        
    entries = entries.filter(created_at__gte=reference_date - timedelta(days=days))
    avg = entries.aggregate(avg=Avg('mood'))['avg']
    return round(avg, 1) if avg is not None else None

def compute_current_streak(entries, reference_date=None):
    """
    Calcule la série actuelle de jours consécutifs avec au moins une entrée.
    
    Args:
        entries: Les entrées de journal de l'utilisateur
        reference_date (date): Date de référence

    Returns:
        int: Nombre de jours consécutifs avec une entrée
    """
    if reference_date is None:
        reference_date = now().date()

    streak = 0
    for i in range(0, 365):
        day = reference_date - timedelta(days=i)
        if entries.filter(created_at__date=day).exists():
            streak += 1
        else:
            break
    return streak

def compute_entries_per_category(entries, days=None):
    """
    Calcule la distribution des entrées par catégorie.

    Args:
        entries: Les entrées de journal de l'utilisateur
        days (int, optional): Limite aux N derniers jours si spécifié

    Returns:
        dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
    """
    if days:
        entries = entries.filter(created_at__gte=now() - timedelta(days=days))
    
    return dict(entries.values('category').annotate(count=Count('id')).values_list('category', 'count'))
