# signals/user_signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from ..models.user_model import User
from ..services.user_service import handle_user_badges, handle_user_streak, handle_user_preferences

# Initialisation du logger pour la gestion des logs
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def handle_user_creation(sender, instance, created, **kwargs):
    """
    Signal appelé après la création d'un utilisateur pour :
    - Créer ses préférences par défaut
    - Mettre à jour ses badges
    - Mettre à jour sa série d'entrées consécutives (streak)
    
    Ce signal est déclenché uniquement lors de la création d'un nouvel utilisateur.
    """

    # Vérifie si l'utilisateur vient d'être créé
    if created:
        # Crée les préférences utilisateur par défaut
        handle_user_preferences(instance)

        # Met à jour les badges de l'utilisateur
        handle_user_badges(instance)

        # Met à jour la série d'entrées consécutives de l'utilisateur
        handle_user_streak(instance)

        # Ajout d'une entrée de log pour indiquer que l'initialisation a été effectuée avec succès
        logger.info(f"Utilisateur {instance.username} créé. Initialisation des préférences, badges et streaks.")
