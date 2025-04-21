# signals/badge_signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from ..services.notification_service import create_user_notification
from ..models import Badge, JournalEntry, Notification, DailyStat, UserPreference, User
from ..services.badge_service import update_user_badges
from ..services.challenge_service import check_user_challenges

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def check_badges_and_stats(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque création d’entrée de journal :
    - Met à jour les stats journalières
    - Vérifie les badges débloqués
    - Vérifie les défis en cours
    """
    user = instance.user
    date = instance.created_at.date()

    # 🔁 Mise à jour ou création des statistiques du jour
    DailyStat.generate_for_user(user=user, date=date)

    # ❌ Ne continue pas si ce n’est pas une nouvelle entrée
    if not created:
        return

    total = user.entries.count()

    # Vérifie les badges via le service
    try:
        new_badges = update_user_badges(user, log_events=True, return_new_badges=True)

        if new_badges:
            # Envoi d'une notification pour chaque nouveau badge débloqué
            for badge in new_badges:
                Notification.objects.create(
                    user=user,
                    message=f"🏅 Félicitations ! Tu as débloqué le badge : {badge.name}",
                    notif_type="badge"
                )
                logger.info(f"[BADGE] {user.username} a débloqué le badge '{badge.name}' (ID: {badge.id})")

    except Exception as e:
        logger.error(f"[BADGE] Erreur lors de la vérification des badges pour {user.username}: {e}")

    # Vérifie les défis en cours (centralisé)
    try:
        check_user_challenges(user)
    except Exception as e:
        logger.error(f"[CHALLENGE] Erreur lors de la vérification des défis pour {user.username}: {e}")

@receiver(post_delete, sender=JournalEntry)
def update_stats_on_delete(sender, instance, **kwargs):
    """
    Recalcule ou supprime les statistiques journalières après suppression d’une entrée.
    """
    user = instance.user
    date = instance.created_at.date()

    remaining_entries = user.entries.filter(created_at__date=date)

    if remaining_entries.exists():
        # Si des entrées restent pour cette date, recalculer les stats
        DailyStat.generate_for_user(user=user, date=date)
    else:
        # Si plus d'entrées, supprimer les stats de cette date
        DailyStat.objects.filter(user=user, date=date).delete()
        logger.info(f"[STATS] Statistiques supprimées pour {user.username} - {date}")

@receiver(post_save, sender=Badge)
def notify_user_of_new_badge(sender, instance, created, **kwargs):
    """
    Signal qui est déclenché lors de la création d'un badge.
    Crée une notification pour informer l'utilisateur de l'attribution du badge.
    """
    if created:
        try:
            # Créer une notification pour l'utilisateur à propos du badge
            create_user_notification(
                user=instance.user,
                message=f"🏅 Nouveau badge débloqué : {instance.name}",
                notif_type="badge"
            )
            logger.info(f"[NOTIFICATION] Notification envoyée à {instance.user.username} pour le badge '{instance.name}' (ID: {instance.id})")

        except Exception as e:
            logger.error(f"[NOTIFICATION] Erreur lors de la création de la notification pour {instance.user.username}: {e}")
