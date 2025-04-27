import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..models import Badge, JournalEntry, Challenge, ChallengeProgress
from ..services.event_log_service import log_event

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Badge)
def log_badge_creation(sender, instance, created, **kwargs):
    """
    Déclenché à la création d'un badge.

    - Log un événement 'attribution_badge' pour l'utilisateur concerné.
    """
    if created:
        log_event(
            action="attribution_badge",
            description=f"Badge {instance.name} attribué à {instance.user.username}",
            user=instance.user,
            severity="INFO",
            metadata={"badge_name": instance.name, "level": instance.level}
        )
        logger.info(f"[EVENT LOG] Badge '{instance.name}' attribué à {instance.user.username}.")


@receiver(post_save, sender=JournalEntry)
def log_journal_entry_creation(sender, instance, created, **kwargs):
    """
    Déclenché à la création d'une entrée de journal.

    - Log un événement 'ajout_entrée_journal'.
    """
    if created:
        log_event(
            action="ajout_entrée_journal",
            description=f"Nouvelle entrée ajoutée par {instance.user.username}",
            user=instance.user,
            severity="INFO",
            metadata={"journal_entry_id": instance.id}
        )
        logger.info(f"[EVENT LOG] Nouvelle entrée de journal pour {instance.user.username}.")


@receiver(post_save, sender=Challenge)
def log_challenge_creation(sender, instance, created, **kwargs):
    """
    Déclenché à la création d'un défi.

    - Log un événement 'création_défi'.
    """
    if created:
        log_event(
            action="création_défi",
            description=f"Défi créé : {instance.title}",
            severity="INFO",
            metadata={"challenge_id": instance.id}
        )
        logger.info(f"[EVENT LOG] Défi '{instance.title}' créé.")


@receiver(post_delete, sender=ChallengeProgress)
def log_challenge_progress_deletion(sender, instance, **kwargs):
    """
    Déclenché à la suppression d'une progression de défi.

    - Log un événement 'suppression_progression_défi'.
    """
    log_event(
        action="suppression_progression_défi",
        description=f"Progression supprimée pour {instance.user.username} sur le défi '{instance.challenge.title}'",
        user=instance.user,
        severity="WARN",
        metadata={"challenge_id": instance.challenge.id}
    )
    logger.warning(f"[EVENT LOG] Progression de défi supprimée pour {instance.user.username}.")
