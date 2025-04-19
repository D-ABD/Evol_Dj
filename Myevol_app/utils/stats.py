from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import timedelta

def get_weekly_entry_stats(user):
    """
    Retourne le nombre d'entrées du journal pour chaque jour de la semaine en cours (Lundi à Dimanche).
    Format de sortie : liste de 7 dicts avec 'day' et 'total'.
    """
    today = now().date()
    week_start = today - timedelta(days=today.weekday())  # Lundi
    week_end = week_start + timedelta(days=6)

    # Récupérer les entrées de la semaine
    entries = user.entries.filter(created_at__date__range=(week_start, week_end))

    # Grouper par jour
    daily_stats = (
        entries.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('id'))
    )

    # Transformation en dict pour un accès rapide
    stats_map = {item["day"]: item["total"] for item in daily_stats}

    # Générer les 7 jours
    result = []
    for i in range(7):
        date = week_start + timedelta(days=i)
        result.append({
            "day": date.strftime('%A'),  # ex : "Lundi"
            "total": stats_map.get(date, 0)
        })

    return result