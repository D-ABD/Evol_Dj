
# signals/quote_signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models.quote_model import Quote
from ..services.notification_service import create_user_notification

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Quote)
def notify_user_of_new_quote(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une nouvelle citation est créée.
    Crée une notification pour informer l'utilisateur de la nouvelle citation.
    """
    if created:
        logger.info(f"Nouvelle citation créée : '{instance.text}'")
        
        # Crée une notification pour chaque nouvelle citation (par exemple, pour l'administrateur)
        create_user_notification(
            user=instance.user,  # Vous pouvez définir un utilisateur ou un admin pour recevoir la notification
            message=f"Une nouvelle citation a été ajoutée : {instance.text}",
            notif_type="info"
        )
