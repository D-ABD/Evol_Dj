# signals/journal_signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from ..models import JournalEntry, DailyStat, Notification, JournalMedia
from ..services.challenge_service import check_challenges
from ..services.badge_service import update_user_badges

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def handle_journal_entry_created(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une entrée de journal est créée.
    Met à jour les statistiques journalières, vérifie les défis en cours,
    et met à jour les badges de l'utilisateur.
    """
    if created:
        logger.info(f"Nouvelle entrée de journal créée pour {instance.user.username} le {instance.created_at.date()}")
        
        # ➕ Mise à jour des statistiques journalières
        DailyStat.generate_for_user(instance.user, instance.created_at.date())
        
        # ✅ Vérification des défis
        check_challenges(instance.user)
        
        # 🏅 Mise à jour des badges de l'utilisateur
        update_user_badges(instance.user)

        # 🔥 Mise à jour des streaks de l'utilisateur
        instance.user.update_streaks()

        # 🔔 Envoi d'une notification de création
        Notification.objects.create(
            user=instance.user,
            message=f"Votre nouvelle entrée du {instance.created_at.date()} a été enregistrée.",
            notif_type="journal_created"
        )


@receiver(post_save, sender=JournalEntry)
def handle_journal_entry_updated(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une entrée de journal est mise à jour.
    Envoie une notification à l'utilisateur pour l'informer de la mise à jour.
    """
    if not created:
        # On envoie une notification seulement si l'entrée est mise à jour
        logger.info(f"Entrée de journal mise à jour pour {instance.user.username} le {instance.updated_at.date()}")
        
        Notification.objects.create(
            user=instance.user,
            message=f"Votre entrée de journal du {instance.created_at.date()} a été mise à jour.",
            notif_type="journal_update"
        )


@receiver(post_delete, sender=JournalEntry)
def handle_media_cleanup(sender, instance, **kwargs):
    """
    Supprime les médias associés à l'entrée de journal lorsqu'elle est supprimée.
    """
    logger.info(f"Suppression des médias associés à l'entrée de journal pour {instance.user.username}")
    
    # Supprimer les fichiers multimédia associés à cette entrée
    for media in instance.media.all():
        logger.info(f"Suppression du fichier média {media.file.url} associé à l'entrée {instance.id}")
        media.file.delete(save=False)  # Suppression du fichier
        media.delete()  # Suppression de l'objet media

    logger.info(f"Médias supprimés pour l'entrée de journal {instance.id}")

    # 🔔 Envoi d'une notification pour informer l'utilisateur de la suppression
    Notification.objects.create(
        user=instance.user,
        message=f"L'entrée de journal du {instance.created_at.date()} a été supprimée avec succès.",
        notif_type="journal_deleted"
    )

