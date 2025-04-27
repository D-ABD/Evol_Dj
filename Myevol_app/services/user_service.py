import logging
from ..models.user_model import User
from ..models.userPreference_model import UserPreference
from .badge_service import update_user_badges
from .streak_service import update_user_streak
from .userpreference_service import create_or_update_preferences

logger = logging.getLogger(__name__)


def handle_user_badges(user):
    """
    Met à jour les badges de l'utilisateur via sa méthode de modèle.
    
    Args:
        user (User): L'utilisateur concerné.
    """
    try:
        user.update_badges()
    except Exception as e:
        logger.error(f"[USER] ❌ Erreur lors de la mise à jour des badges pour {user.username} : {e}")


def handle_user_streak(user):
    """
    Met à jour les streaks (séries) de l'utilisateur via sa méthode de modèle.

    Args:
        user (User): L'utilisateur concerné.
    """
    try:
        user.update_streaks()
    except Exception as e:
        logger.error(f"[USER] ❌ Erreur lors de la mise à jour des streaks pour {user.username} : {e}")


def handle_user_preferences(user):
    """
    Crée ou met à jour les préférences par défaut de l'utilisateur via sa méthode de modèle.

    Args:
        user (User): L'utilisateur concerné.
    """
    try:
        user.create_default_preferences()
    except Exception as e:
        logger.error(f"[USER] ❌ Erreur lors de la création des préférences pour {user.username} : {e}")


def initialize_user_profile(user):
    """
    Appelle les routines d'initialisation pour un nouvel utilisateur :
    - Préférences
    - Badges
    - Streaks

    Args:
        user (User): L'utilisateur fraîchement créé.
    """
    logger.info(f"[USER INIT] Initialisation du profil pour {user.username}")
    handle_user_preferences(user)
    handle_user_streak(user)
    handle_user_badges(user)
