# signals/objective_signals.py

import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from ..models.objective_model import Objective
from ..models.notification_model import Notification
from django.utils.timezone import now

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Objective)
def handle_objective_creation(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de la création d'un objectif.
    Envoie une notification si l'objectif est marqué comme complété.
    """
    if created:
        logger.info(f"Création d'un nouvel objectif pour {instance.user.username}: {instance.title}")
    
    if instance.done:
        # Si l'objectif est marqué comme fait lors de la création
        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Objectif atteint : {instance.title}",
            notif_type="objectif"
        )
        logger.info(f"Objectif complété : {instance.title} pour {instance.user.username}")


@receiver(post_save, sender=Objective)
def handle_objective_update(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de la mise à jour d'un objectif.
    Si l'objectif est marqué comme complété, envoie une notification.
    """
    if not created:
        if instance.done:
            Notification.objects.create(
                user=instance.user,
                message=f"🎯 Objectif atteint : {instance.title}",
                notif_type="objectif"
            )
            logger.info(f"Objectif mis à jour comme complété : {instance.title} pour {instance.user.username}")


@receiver(pre_delete, sender=Objective)
def handle_objective_delete(sender, instance, **kwargs):
    """
    Signal déclenché avant la suppression d'un objectif.
    Log de la suppression.
    """
    logger.info(f"Suppression de l'objectif {instance.title} pour {instance.user.username}")
