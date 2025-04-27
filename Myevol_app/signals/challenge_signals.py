import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from ..models import Challenge, ChallengeProgress
from ..services.challenge_service import update_challenge_progress
from ..services.badge_service import update_user_badges
from ..services.notification_service import create_user_notification

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Challenge)
def handle_challenge_creation(sender, instance, created, **kwargs):
    """
    Déclenché à la création d'un défi.

    - Log l'événement de création.
    - (Optionnel) Notification ou autre traitement métier.
    """
    if created:
        logger.info(f"[CHALLENGE] Nouveau défi créé : {instance.title} (ID: {instance.id})")
        # Exemple : envoyer une notification aux administrateurs ou au public via un autre système


@receiver(post_save, sender=ChallengeProgress)
def handle_challenge_progress_update(sender, instance, created, **kwargs):
    """
    Déclenché lors de la création ou mise à jour d'une progression sur un défi.

    - Vérifie la progression de l'utilisateur.
    - Met à jour les badges si nécessaire.
    """
    if created:
        logger.info(
            f"[CHALLENGE PROGRESS] Progression créée pour {instance.user.username} sur {instance.challenge.title}"
        )
    else:
        logger.info(
            f"[CHALLENGE PROGRESS] Progression mise à jour pour {instance.user.username} sur {instance.challenge.title}"
        )

    update_challenge_progress(instance)
    update_user_badges(instance.user)


@receiver(post_delete, sender=ChallengeProgress)
def handle_challenge_progress_deletion(sender, instance, **kwargs):
    """
    Déclenché lors de la suppression d'une progression de défi.

    - Log l'événement.
    - (Optionnel) Mettre à jour les statistiques de l'utilisateur.
    """
    logger.info(
        f"[CHALLENGE PROGRESS] Progression supprimée pour {instance.user.username} sur {instance.challenge.title}"
    )
    # Optionnel : recalcul des statistiques ici si tu le souhaites
