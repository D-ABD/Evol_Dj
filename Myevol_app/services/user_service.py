# services/user_service.py

from ..models.userPreference_model import UserPreference
from ..models.user_model import User
from .badge_service import update_user_badges
from .streak_service import update_user_streak
from .userpreference_service import create_preferences_for_user
import logging

logger = logging.getLogger(__name__)

def handle_user_badges(user):
    """
    Met à jour les badges pour l'utilisateur.
    """
    try:
        update_user_badges(user)
        logger.info(f"Badges mis à jour pour {user.username}.")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des badges pour {user.username}: {e}")

def handle_user_streak(user):
    """
    Met à jour les streaks de l'utilisateur.
    """
    try:
        update_user_streak(user)
        logger.info(f"Streaks mis à jour pour {user.username}.")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des streaks pour {user.username}: {e}")

def handle_user_preferences(user):
    """
    Crée les préférences par défaut pour l'utilisateur si elles n'existent pas.
    """
    try:
        create_preferences_for_user(user)
        logger.info(f"Préférences par défaut créées pour {user.username}.")
    except Exception as e:
        logger.error(f"Erreur lors de la création des préférences pour {user.username}: {e}")
