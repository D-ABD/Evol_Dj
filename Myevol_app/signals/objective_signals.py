import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.timezone import now

from ..models.objective_model import Objective

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Objective)
def handle_objective_save(sender, instance, created, **kwargs):
    """
    Déclenché à la création ou à la mise à jour d'un objectif.

    - Si créé ➔ Log de création.
    - Si `done=True` ➔ Notification d'objectif atteint.
    """
    if created:
        logger.info(f"[OBJECTIF] Création d'un nouvel objectif '{instance.title}' pour {instance.user.username}.")

    if instance.done:
        from ..models.notification_model import Notification

        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Objectif atteint : {instance.title}",
            notif_type="objectif"
        )
        logger.info(f"[OBJECTIF] Objectif '{instance.title}' complété par {instance.user.username}.")


@receiver(pre_delete, sender=Objective)
def handle_objective_deletion(sender, instance, **kwargs):
    """
    Déclenché avant la suppression d'un objectif.
    Loggue la suppression.
    """
    logger.info(f"[OBJECTIF] Suppression de l'objectif '{instance.title}' pour {instance.user.username}.")
