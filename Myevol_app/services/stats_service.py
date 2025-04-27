import logging
from collections import defaultdict
from datetime import timedelta
from django.db.models import Avg
from django.utils.timezone import now
from ..models.stats_model import WeeklyStat, MonthlyStat, AnnualStat, DailyStat

logger = logging.getLogger(__name__)


def generate_weekly_stats(user, reference_date=None):
    """
    Génère ou met à jour les statistiques hebdomadaires pour un utilisateur.

    Args:
        user (User): L'utilisateur concerné
        reference_date (date, optional): Date de référence pour déterminer la semaine. 
                                         Si non fourni, la date du jour est utilisée.

    Returns:
        WeeklyStat: Statistique hebdomadaire créée ou mise à jour
    """
    reference_date = reference_date or now().date()
    week_start = reference_date - timedelta(days=reference_date.weekday())
    week_end = week_start + timedelta(days=6)

    entries = user.entries.filter(created_at__date__range=(week_start, week_end))
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = WeeklyStat.objects.update_or_create(
        user=user,
        week_start=week_start,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"📊 Weekly stats CREATED for {user.username} - Week of {week_start}")
    else:
        logger.info(f"📈 Weekly stats UPDATED for {user.username} - Week of {week_start}")

    return stat


def generate_daily_stats(user, date=None):
    """
    Génère ou met à jour les statistiques journalières pour un utilisateur.

    Args:
        user (User): L'utilisateur concerné
        date (date, optional): Date pour laquelle générer les stats. Aujourd’hui par défaut.

    Returns:
        DailyStat: Statistique journalière créée ou mise à jour
    """
    date = date or now().date()
    entries = user.entries.filter(created_at__date=date)
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = DailyStat.objects.update_or_create(
        user=user,
        date=date,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"📊 Daily stats CREATED for {user.username} - {date}")
    else:
        logger.info(f"📈 Daily stats UPDATED for {user.username} - {date}")

    return stat


def generate_monthly_stats(user, reference_date=None):
    """
    Génère ou met à jour les statistiques mensuelles pour un utilisateur.

    Args:
        user (User): L'utilisateur concerné
        reference_date (date, optional): Date servant à identifier le mois cible

    Returns:
        MonthlyStat: Statistique mensuelle créée ou mise à jour
    """
    reference_date = reference_date or now().date()
    month_start = reference_date.replace(day=1)
    next_month = (month_start + timedelta(days=32)).replace(day=1)
    month_end = next_month - timedelta(days=1)

    entries = user.entries.filter(created_at__date__range=(month_start, month_end))
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = MonthlyStat.objects.update_or_create(
        user=user,
        month_start=month_start,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"📊 Monthly stats CREATED for {user.username} - {month_start.strftime('%B %Y')}")
    else:
        logger.info(f"📈 Monthly stats UPDATED for {user.username} - {month_start.strftime('%B %Y')}")

    return stat


def generate_annual_stats(user, reference_date=None):
    """
    Génère ou met à jour les statistiques annuelles pour un utilisateur.

    Args:
        user (User): L'utilisateur concerné
        reference_date (date, optional): Date pour cibler l'année en cours

    Returns:
        AnnualStat: Statistique annuelle créée ou mise à jour
    """
    reference_date = reference_date or now().date()
    year_start = reference_date.replace(month=1, day=1)
    year_end = year_start.replace(month=12, day=31)

    entries = user.entries.filter(created_at__date__range=(year_start, year_end))
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = AnnualStat.objects.update_or_create(
        user=user,
        year_start=year_start,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"📊 Annual stats CREATED for {user.username} - Year {year_start.year}")
    else:
        logger.info(f"📈 Annual stats UPDATED for {user.username} - Year {year_start.year}")

    return stat


def compute_stats_for_period(user, start_date, end_date):
    """
    Calcule les statistiques générales (nombre d'entrées, moyenne des humeurs, répartition des catégories)
    pour une période donnée.

    Args:
        user (User): L'utilisateur pour lequel calculer les statistiques
        start_date (date): Début de la période
        end_date (date): Fin de la période

    Returns:
        dict: Dictionnaire contenant entries_count, mood_average, categories
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
