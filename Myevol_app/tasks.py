# tasks.py
from celery import shared_task
from django.utils.timezone import now
from .models import Notification, User
from .services import stats_service, streak_service, notification_service
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task
def send_scheduled_notifications():
    """
    Tâche pour envoyer toutes les notifications programmées.
    """
    logger.info("Scheduled notifications task executed.")
    return "Scheduled notifications sent."

@shared_task
def generate_all_daily_stats():
    """
    Génère les statistiques journalières pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_daily_stats(user)
    return "Statistiques journalières générées."

@shared_task
def generate_all_weekly_stats():
    """
    Génère les statistiques hebdomadaires pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_weekly_stats(user)
    return "Statistiques hebdomadaires générées."

@shared_task
def generate_all_monthly_stats():
    """
    Génère les statistiques mensuelles pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_monthly_stats(user)
    return "Statistiques mensuelles générées."

@shared_task
def generate_all_annual_stats():
    """
    Génère les statistiques annuelles pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_annual_stats(user)
    return "Statistiques annuelles générées."

@shared_task
def recalculate_all_streaks():
    """
    Recalcule les streaks (séries d'entrées consécutives) de tous les utilisateurs.
    """
    for user in User.objects.all():
        streak_service.update_user_streak(user)
    return "Séries (streaks) mises à jour."

@shared_task
def remind_inactive_users():
    """
    Envoie un rappel aux utilisateurs sans activité récente.
    """
    threshold = now() - timedelta(days=2)  # Ex : pas d'entrée depuis 2 jours
    for user in User.objects.all():
        if not user.entries.filter(created_at__gte=threshold).exists():
            notification_service.create_user_notification(
                user=user,
                message="N'oubliez pas d'écrire dans votre journal aujourd'hui 📖",
                notif_type="journal_reminder"
            )
    return "Rappels envoyés aux utilisateurs inactifs."

@shared_task
def clean_old_notifications():
    """
    Supprime les anciennes notifications de plus de 90 jours.
    """
    cutoff = now() - timedelta(days=90)
    count, _ = Notification.objects.filter(created_at__lt=cutoff).delete()
    return f"{count} anciennes notifications supprimées."

@shared_task
def ask_user_daily_activity():
    """
    Demande quotidienne aux utilisateurs de réfléchir à leur journée à 19h.
    """
    for user in User.objects.all():
        notification_service.create_user_notification(
            user=user,
            message="Qu'avez-vous accompli aujourd'hui ? Prenez un moment pour écrire dans votre journal. ✍️",
            notif_type="journal_prompt"
        )
    return "Notifications de réflexion journalière envoyées."
