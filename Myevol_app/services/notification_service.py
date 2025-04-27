# services/notification_service.py

import logging
from django.utils.timezone import now
from django.conf import settings

from ..models.notification_model import Notification
from ..models.user_model import User  # ✅ Correction ici : importer User du bon fichier

logger = logging.getLogger(__name__)


def create_user_notification(user, message, notif_type="info", scheduled_at=None):
    """
    Crée une notification pour l'utilisateur, en respectant ses préférences.

    Args:
        user (User): L'utilisateur concerné.
        message (str): Le contenu du message à envoyer.
        notif_type (str): Le type de notification ('badge', 'objectif', 'info', 'statistique').
        scheduled_at (datetime, optional): Date/heure à laquelle afficher la notification.

    Returns:
        Notification | None: La notification créée, ou None si bloquée par les préférences.
    """
    if hasattr(user, 'preferences') and not user.preferences.should_send_notification(notif_type):
        logger.debug(f"[NOTIF] 🚫 Notification '{notif_type}' ignorée pour {user.username} selon les préférences.")
        return None

    notif = Notification.objects.create(
        user=user,
        message=message,
        notif_type=notif_type,
        scheduled_at=scheduled_at
    )

    logger.info(f"[NOTIF] ✅ Notification '{notif_type}' créée pour {user.username}")
    return notif


def create_admin_notification(message, notif_type="info", scheduled_at=None):
    """
    Crée une notification destinée à l'administrateur principal.

    Args:
        message (str): Contenu du message de notification.
        notif_type (str): Type de notification ('info', 'erreur', etc.).
        scheduled_at (datetime, optional): Date/heure planifiée pour l'envoi de la notification.

    Returns:
        Notification | None: La notification créée, ou None si problème.
    """
    try:
        admin_email = getattr(settings, "DEFAULT_ADMIN_EMAIL", None)

        if not admin_email:
            logger.warning("[NOTIF] Aucun email admin configuré dans settings (DEFAULT_ADMIN_EMAIL manquant).")
            return None

        # Utiliser get() pour récupérer un utilisateur unique
        admin_user = User.objects.get(email=admin_email)

        notif = Notification.objects.create(
            user=admin_user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )

        logger.info(f"[NOTIF] ✅ Notification '{notif_type}' envoyée à l'admin {admin_user.username}")
        return notif

    except User.DoesNotExist:
        logger.error(f"[NOTIF] ❌ Aucun utilisateur trouvé avec l'email '{admin_email}'")
        return None
    except Exception as e:
        logger.error(f"[NOTIF] ❌ Erreur lors de la création d'une notification admin: {str(e)}")
        return None


def send_scheduled_notifications():
    """
    Parcourt et envoie les notifications programmées dont la date est atteinte.

    Effet :
        - Marque les notifications comme lues
        - Peut être appelé par une tâche CRON ou Celery

    Returns:
        int: Nombre de notifications envoyées
    """
    notifications = Notification.objects.filter(
        scheduled_at__lte=now(),
        is_read=False,
        archived=False
    )

    count = 0
    for notif in notifications:
        # ICI : possibilité d'envoyer un email ou une web notification
        notif.mark_as_read()
        count += 1
        logger.info(f"[NOTIF] ⏰ Notification programmée envoyée à {notif.user.username} : {notif.message}")

    return count


def archive_user_notifications(user):
    """
    Archive toutes les notifications actives de l'utilisateur.

    Args:
        user (User): Utilisateur concerné.

    Returns:
        int: Nombre de notifications archivées.
    """
    notifications = Notification.objects.filter(user=user, archived=False)
    count = notifications.update(archived=True)
    logger.info(f"[NOTIF] 🗃️ {count} notifications archivées pour {user.username}")
    return count
