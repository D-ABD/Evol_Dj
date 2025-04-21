# signals/stats_signals.py

from django.db.models.signals import post_save, post_delete
import logging
from django.dispatch import receiver
from ..models.stats_model import WeeklyStat, DailyStat, MonthlyStat, AnnualStat, JournalEntry
from ..services.stats_service import generate_weekly_stats, generate_daily_stats, generate_monthly_stats, generate_annual_stats

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def update_statistics(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de la création d'une entrée de journal.
    Met à jour les statistiques hebdomadaires, journalières, mensuelles et annuelles de l'utilisateur.
    """
    if created:
        # Mise à jour des statistiques pour chaque entrée de journal
        generate_weekly_stats(instance.user)
        generate_daily_stats(instance.user)
        generate_monthly_stats(instance.user)
        generate_annual_stats(instance.user)

@receiver(post_save, sender=WeeklyStat)
def log_weekly_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques hebdomadaires.
    """
    if created:
        logger.info(f"Statistiques hebdomadaires créées pour {instance.user.username} - Semaine du {instance.week_start}")

@receiver(post_delete, sender=WeeklyStat)
def log_weekly_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques hebdomadaires.
    """
    logger.info(f"Statistiques hebdomadaires supprimées pour {instance.user.username} - Semaine du {instance.week_start}")

@receiver(post_save, sender=DailyStat)
def log_daily_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques journalières.
    """
    if created:
        logger.info(f"Statistiques journalières créées pour {instance.user.username} - {instance.date}")

@receiver(post_delete, sender=DailyStat)
def log_daily_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques journalières.
    """
    logger.info(f"Statistiques journalières supprimées pour {instance.user.username} - {instance.date}")

@receiver(post_save, sender=MonthlyStat)
def log_monthly_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques mensuelles.
    """
    if created:
        logger.info(f"Statistiques mensuelles créées pour {instance.user.username} - Mois de {instance.month_start.strftime('%B %Y')}")

@receiver(post_delete, sender=MonthlyStat)
def log_monthly_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques mensuelles.
    """
    logger.info(f"Statistiques mensuelles supprimées pour {instance.user.username} - Mois de {instance.month_start.strftime('%B %Y')}")

@receiver(post_save, sender=AnnualStat)
def log_annual_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques annuelles.
    """
    if created:
        logger.info(f"Statistiques annuelles créées pour {instance.user.username} - Année {instance.year_start.year}")

@receiver(post_delete, sender=AnnualStat)
def log_annual_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques annuelles.
    """
    logger.info(f"Statistiques annuelles supprimées pour {instance.user.username} - Année {instance.year_start.year}")
