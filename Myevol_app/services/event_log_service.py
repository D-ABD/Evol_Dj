# services/event_log_service.py

from datetime import timedelta
import logging
from django.utils.timezone import now
from ..models import EventLog

logger = logging.getLogger(__name__)

def log_event(action, description="", user=None, severity="INFO", **metadata):
    """
    Enregistre un événement dans le modèle EventLog en déléguant à la méthode `log_action`.

    Args:
        action (str): Type d'action (ex : "connexion", "attribution_badge", etc.)
        description (str): Détails supplémentaires sur l'événement
        user (User, optional): Utilisateur concerné par l'événement
        severity (str): Niveau de gravité de l'événement ('INFO', 'WARN', 'ERROR', 'CRITICAL')
        **metadata (dict): Données supplémentaires liées à l'événement

    Returns:
        EventLog: Instance de l'événement créé, ou None en cas d'erreur
    """
    try:
        return EventLog.log_action(
            action=action,
            description=description,
            user=user,
            severity=severity,
            **metadata
        )
    except Exception as e:
        username = getattr(user, 'username', 'System')
        logger.error(f"❌ Erreur lors de la création de l'événement '{action}' pour {username}: {str(e)}")
        return None

def get_event_statistics(days=30, user=None):
    """
    Récupère des statistiques agrégées des événements sur une période donnée.

    Args:
        days (int): Nombre de jours à considérer depuis aujourd’hui
        user (User, optional): Filtrer par utilisateur

    Returns:
        dict: Statistiques des événements sous forme {action: count}
    """
    from django.db.models import Count

    since = now() - timedelta(days=days)
    events = EventLog.objects.filter(created_at__gte=since)

    if user:
        events = events.filter(user=user)

    return dict(
        events.values("action")
              .annotate(count=Count("id"))
              .values_list("action", "count")
    )
