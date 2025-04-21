# services/notification_service.py

import logging
from django.utils.timezone import now
from ..models import Notification

logger = logging.getLogger(__name__)

def create_user_notification(user, message, notif_type="info", scheduled_at=None):
    """
    Service qui crée une notification pour un utilisateur.
    
    Args:
        user (User): L'utilisateur auquel la notification est destinée.
        message (str): Le message de la notification.
        notif_type (str): Le type de notification, ex. 'badge', 'objectif'.
        scheduled_at (datetime, optional): Date de programmation de la notification.
        
    Returns:
        Notification: Notification créée et stockée dans la base de données.
    """
    notification = Notification.objects.create(
        user=user,
        message=message,
        notif_type=notif_type,
        scheduled_at=scheduled_at
    )
    
    # Optionnel : Ajouter une logique de notification ici (comme des emails, web push, etc.)
    # par exemple : send_notification_to_user(user, message)

    return notification


def send_scheduled_notifications():
    """
    Service qui envoie les notifications programmées à la date actuelle.
    """
    notifications = Notification.objects.filter(scheduled_at__lte=now(), is_read=False, archived=False)
    
    for notification in notifications:
        # Logique d'envoi de notification (ex : via un service de messagerie, email, etc.)
        # send_notification(notification)
        
        # Marque comme lue la notification envoyée
        notification.mark_as_read()

        logger.info(f"Notification envoyée à {notification.user.username} : {notification.message}")


def archive_user_notifications(user):
    """
    Archive toutes les notifications d'un utilisateur.
    
    Args:
        user (User): L'utilisateur dont les notifications seront archivées.
        
    Returns:
        int: Nombre de notifications archivées.
    """
    notifications = Notification.objects.filter(user=user, archived=False)
    archived_count = notifications.update(archived=True)
    
    logger.info(f"{archived_count} notifications archivées pour {user.username}")
    return archived_count

