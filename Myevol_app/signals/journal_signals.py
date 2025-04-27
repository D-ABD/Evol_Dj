import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from ..models import JournalEntry, DailyStat, Notification, JournalMedia
from ..services.challenge_service import check_challenges
from ..services.badge_service import update_user_badges

logger = logging.getLogger(__name__)


@receiver(post_save, sender=JournalEntry)
def handle_journal_entry_created_or_updated(sender, instance, created, **kwargs):
    """
    Déclenché à la création ou mise à jour d'une entrée de journal.

    - Si créée ➔ met à jour les stats journalières, défis, badges, streaks et notifie la création.
    - Si mise à jour ➔ envoie une notification de mise à jour.
    """
    if created:
        logger.info(f"[JOURNAL] Nouvelle entrée pour {instance.user.username} le {instance.created_at.date()}.")
        
        # ➕ Statistiques journalières
        DailyStat.generate_for_user(instance.user, instance.created_at.date())
        
        # ✅ Défis
        check_challenges(instance.user)
        
        # 🏅 Badges
        update_user_badges(instance.user)

        # 🔥 Streaks
        instance.user.update_streaks()

        # 🔔 Notification de création
        Notification.objects.create(
            user=instance.user,
            message=f"Votre nouvelle entrée du {instance.created_at.date()} a été enregistrée.",
            notif_type="journal_created"
        )
    else:
        logger.info(f"[JOURNAL] Entrée mise à jour pour {instance.user.username} le {instance.updated_at.date()}.")
        
        # 🔔 Notification de mise à jour
        Notification.objects.create(
            user=instance.user,
            message=f"Votre entrée de journal du {instance.created_at.date()} a été mise à jour.",
            notif_type="journal_update"
        )


@receiver(post_delete, sender=JournalEntry)
def handle_journal_entry_deletion(sender, instance, **kwargs):
    """
    Déclenché lors de la suppression d'une entrée de journal.

    - Supprime les médias associés.
    - Envoie une notification de suppression.
    """
    logger.info(f"[JOURNAL] Suppression de l'entrée {instance.id} pour {instance.user.username}.")

    # Supprimer tous les médias liés à l'entrée
    for media in instance.media.all():
        logger.info(f"[MEDIA] Suppression du fichier média {media.file.url} lié à l'entrée {instance.id}.")
        media.file.delete(save=False)
        media.delete()

    # 🔔 Notification de suppression
    Notification.objects.create(
        user=instance.user,
        message=f"L'entrée de journal du {instance.created_at.date()} a été supprimée.",
        notif_type="journal_deleted"
    )
    logger.info(f"[NOTIFICATION] Suppression notifiée à {instance.user.username}.")
