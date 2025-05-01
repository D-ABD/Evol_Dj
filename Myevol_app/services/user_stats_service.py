from datetime import timedelta
from collections import defaultdict
from django.db.models import Avg, Count
from django.utils.timezone import now


def compute_mood_average(user, days=7, category=None, reference_date=None):
    """
    Calcule la moyenne d'humeur d'un utilisateur sur une période donnée.

    Args:
        user (User): L'utilisateur concerné.
        days (int or None): Nombre de jours à considérer. Si None, prend toutes les entrées.
        category (str, optional): Catégorie à filtrer.
        reference_date (datetime, optional): Date de référence (par défaut : maintenant).

    Returns:
        float or None: Moyenne d'humeur arrondie à 1 décimale, ou None si aucune entrée.
    """
    reference_date = reference_date or now()
    entries = user.entries.all()

    if days is not None:
        since = reference_date - timedelta(days=days)
        entries = entries.filter(created_at__gte=since)

    if category:
        entries = entries.filter(category=category)

    avg = entries.aggregate(avg=Avg('mood'))['avg']
    return round(avg, 1) if avg is not None else None



def compute_current_streak(user, reference_date=None):
    """
    Calcule la série actuelle de jours consécutifs avec au moins une entrée.

    Args:
        user (User): Utilisateur concerné
        reference_date (date, optional): Date de référence (aujourd'hui par défaut)

    Returns:
        int: Nombre de jours consécutifs avec des entrées
    """
    reference_date = reference_date or now().date()
    entries = user.entries.all()

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
    Calcule la répartition des entrées par catégorie.

    Args:
        entries (QuerySet): Entrées de journal
        days (int, optional): Limite aux N derniers jours

    Returns:
        dict: {catégorie: nombre d'entrées}
    """
    if days:
        entries = entries.filter(created_at__gte=now() - timedelta(days=days))
    return dict(entries.values('category').annotate(count=Count('id')).values_list('category', 'count'))


def compute_stats_for_period(user, start_date, end_date):
    """
    Calcule les statistiques entre deux dates pour un utilisateur :
    - Nombre total d'entrées
    - Moyenne des humeurs
    - Répartition par catégorie

    Args:
        user (User): Utilisateur concerné
        start_date (date): Début de la période
        end_date (date): Fin de la période

    Returns:
        dict: Résultat des statistiques (entries_count, mood_average, categories)
    """
    entries = user.entries.filter(created_at__date__range=(start_date, end_date))
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    return {
        "entries_count": entries_count,
        "mood_average": mood_avg,
        "categories": dict(categories),
    }
