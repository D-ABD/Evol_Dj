import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models.quote_model import Quote
from ..services.notification_service import create_admin_notification

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Quote)
def handle_quote_post_save(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une citation est créée.
    - Log la création.
    - Envoie une notification à l'admin (via create_admin_notification).

    Args:
        sender (Model): Le modèle émetteur (Quote).
        instance (Quote): Instance de la citation.
        created (bool): True si nouvellement créée, False si mise à jour.
    """
    if created:
        preview = instance.text[:50]
        author = instance.author or "Inconnu"
        logger.info(f"[QUOTE] Nouvelle citation créée : '{preview}...' — {author}")

        # Notification admin
        create_admin_notification(
            message=f"📝 Nouvelle citation ajoutée : '{preview}...' — {author}",
            notif_type="info"
        )


@receiver(post_delete, sender=Quote)
def handle_quote_post_delete(sender, instance, **kwargs):
    """
    Signal déclenché lors de la suppression d'une citation.
    Log l'événement.

    Args:
        sender (Model): Le modèle émetteur (Quote).
        instance (Quote): Instance supprimée.
    """
    preview = instance.text[:50]
    author = instance.author or "Inconnu"
    logger.info(f"[QUOTE] Citation supprimée : '{preview}...' — {author}")
