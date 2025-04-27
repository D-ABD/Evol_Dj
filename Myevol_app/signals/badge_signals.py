import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..services.notification_service import create_user_notification

from ..models import Badge

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Badge)
def notify_user_of_new_badge(sender, instance, created, **kwargs):
    """
    Envoie une notification à l'utilisateur lorsqu'un nouveau badge lui est attribué.

    Ce signal est déclenché automatiquement après la création d'une instance de Badge.
    Une notification de type 'badge' est envoyée via le service de notifications.

    Args:
        sender (Model): Le modèle déclencheur du signal (Badge)
        instance (Badge): L'instance du badge nouvellement créée
        created (bool): Indique si l'instance a été créée (True) ou mise à jour (False)
        **kwargs: Paramètres supplémentaires du signal
    """
    if created:

        try:
            create_user_notification(
                user=instance.user,
                message=f"🏅 Nouveau badge débloqué : {instance.name}",
                notif_type="badge"
            )
            logger.info(
                f"[NOTIFICATION] Badge '{instance.name}' attribué à {instance.user.username} — Notification envoyée"
            )
        except Exception as e:
            logger.error(
                f"[NOTIFICATION] ❌ Erreur lors de la notification du badge pour {instance.user.username} : {e}"
            )
