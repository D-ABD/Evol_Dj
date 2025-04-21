import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..services.event_log_service import log_event

from ..models.challenge_model import ChallengeProgress
from ..models import EventLog, Challenge, Badge, JournalEntry, User

logger = logging.getLogger(__name__)

# Signal de création d'un badge
@receiver(post_save, sender=Badge)
def log_badge_creation(sender, instance, created, **kwargs):
    """
    Enregistre un événement chaque fois qu'un badge est attribué à un utilisateur.
    """
    if created:
        log_event(
            action="attribution_badge",
            description=f"Badge {instance.name} attribué à {instance.user.username}",
            user=instance.user,
            severity="INFO",
            metadata={"badge_name": instance.name, "level": instance.level}
        )

# Signal de création d'une entrée de journal
@receiver(post_save, sender=JournalEntry)
def log_journal_entry(sender, instance, created, **kwargs):
    """
    Enregistre un événement chaque fois qu'une entrée de journal est ajoutée.
    """
    if created:
        log_event(
            action="ajout_entrée_journal",
            description=f"Nouvelle entrée de journal ajoutée par {instance.user.username}",
            user=instance.user,
            severity="INFO",
            metadata={"journal_entry_id": instance.id}
        )

# Signal de création ou mise à jour de la progression du défi
@receiver(post_save, sender=Challenge)
def log_challenge_creation(sender, instance, created, **kwargs):
    """
    Enregistre un événement chaque fois qu'un défi est créé.
    """
    if created:
        log_event(
            action="création_défi",
            description=f"Nouveau défi créé : {instance.title}",
            severity="INFO",
            metadata={"challenge_id": instance.id}
        )

# Signal de suppression de la progression du défi
@receiver(post_delete, sender=ChallengeProgress)
def log_challenge_progress_removal(sender, instance, **kwargs):
    """
    Enregistre un événement chaque fois qu'une progression de défi est supprimée.
    """
    log_event(
        action="suppression_progression_défi",
        description=f"Progression du défi {instance.challenge.title} supprimée pour {instance.user.username}",
        user=instance.user,
        severity="WARN",
        metadata={"challenge_id": instance.challenge.id}
    )
