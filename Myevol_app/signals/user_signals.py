# signals/user_signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models.user_model import User
from ..services.user_service import (
    handle_user_preferences,
    handle_user_badges,
    handle_user_streak,
)

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def initialize_user_after_creation(sender, instance, created, **kwargs):
    """
    Signal déclenché après la création d'un nouvel utilisateur.
    Initialise :
    - ses préférences par défaut,
    - ses badges initiaux,
    - ses streaks.

    Args:
        sender (Model): Le modèle User.
        instance (User): L'utilisateur nouvellement créé.
        created (bool): True si nouvel utilisateur.
    """
    if created:
        logger.info(f"[USER INIT] Création de {instance.username} - Initialisation du profil...")

        # Préférences par défaut
        handle_user_preferences(instance)

        # Attribution initiale des badges
        handle_user_badges(instance)

        # Calcul initial du streak
        handle_user_streak(instance)

        logger.info(f"[USER INIT] ✅ Profil initialisé pour {instance.username}")
