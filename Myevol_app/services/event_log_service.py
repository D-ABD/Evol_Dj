# services/event_log_service.py

from datetime import timedelta
import logging
from ..models import EventLog
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def log_event(action, description="", user=None, severity="INFO", **metadata):
    """
    Enregistre un événement dans le modèle EventLog. Cette méthode est utilisée pour tous les types d'événements.
    
    Args:
        action (str): Type d'action (ex : "connexion", "attribution_badge", etc.)
        description (str): Détails supplémentaires sur l'événement
        user (User, optional): Utilisateur concerné par l'événement
        severity (str): Niveau de gravité de l'événement ('INFO', 'WARN', 'ERROR', 'CRITICAL')
        **metadata (dict): Données supplémentaires liées à l'événement
    
    Returns:
        EventLog: Instance de l'événement créé
    """
    try:
        # Crée un log dans la base de données
        event = EventLog.objects.create(
            action=action,
            description=description,
            user=user,
            severity=severity,
            metadata=metadata or None
        )
        logger.info(f"[LOG] {user.username if user else 'System'} > {action} > {description} > Severity: {severity}")
        return event
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'événement {action} pour {user.username if user else 'System'}: {str(e)}")
        return None

def get_event_statistics(days=30, user=None):
    """
    Récupère des statistiques agrégées des événements sur une période donnée.
    
    Args:
        days (int): Nombre de jours à considérer depuis aujourd’hui
        user (User, optional): Filtrer par utilisateur
    
    Returns:
        dict: Statistiques des événements {action: count}
    """
    from django.db.models import Count
    
    # Filtre des événements pour les derniers 'days' jours
    since = now() - timedelta(days=days)
    events = EventLog.objects.filter(created_at__gte=since)
    
    # Si un utilisateur est spécifié, filtre par utilisateur
    if user:
        events = events.filter(user=user)

    return dict(events.values('action')
                .annotate(count=Count('id'))
                .values_list('action', 'count'))
