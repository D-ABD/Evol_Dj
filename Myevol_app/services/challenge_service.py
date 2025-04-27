# Myevol_app/services/challenge_service.py

# services/challenge_service.py

import logging
from ..models import ChallengeProgress, Challenge, Notification
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def update_challenge_progress(progress_instance):
    """
    Met à jour la progression d'un utilisateur sur un défi.
    Cette méthode vérifie si un utilisateur a complété son défi, envoie des notifications,
    et enregistre l'état de complétion.

    Args:
        progress_instance (ChallengeProgress): Instance de progression du défi
    """
    # Vérifie si l'utilisateur a atteint son objectif
    challenge = progress_instance.challenge
    user = progress_instance.user

    if not progress_instance.completed and challenge.is_completed(user):
        progress_instance.completed = True
        progress_instance.completed_at = now()
        progress_instance.save()

        # Notifie l'utilisateur que le défi est terminé
        Notification.objects.create(
            user=user,
            message=f"🎯 Félicitations ! Vous avez complété le défi : {challenge.title}",
            notif_type="objectif"
        )

        logger.info(f"[CHALLENGE] {user.username} a complété le défi '{challenge.title}'")

def check_user_challenges(user):
    """
    Vérifie tous les défis actifs de l'utilisateur et met à jour sa progression.
    Cette fonction peut être appelée régulièrement pour vérifier l'état de tous les défis de l'utilisateur.

    Args:
        user (User): Utilisateur dont les défis doivent être vérifiés
    """
    today = now().date()

    # Récupère tous les défis actifs
    active_challenges = Challenge.objects.filter(start_date__lte=today, end_date__gte=today)

    for challenge in active_challenges:
        # Récupère ou crée une instance de progression pour chaque défi
        progress, created = ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)

        # Si c'est une nouvelle progression, on vérifie si l'utilisateur a déjà atteint l'objectif
        if created:
            logger.info(f"[CHALLENGE] Progression créée pour {user.username} sur le défi '{challenge.title}'")
        else:
            logger.info(f"[CHALLENGE] Progression mise à jour pour {user.username} sur le défi '{challenge.title}'")

        # Met à jour la progression de l'utilisateur
        update_challenge_progress(progress)

def check_challenges(user):
    """
    Vérifie tous les défis actifs de l'utilisateur et met à jour leur progression.
    Cette fonction est appelée après la création d'une entrée de journal.
    
    Args:
        user (User): L'utilisateur dont les défis doivent être vérifiés
    """
    # Pas besoin d'importer check_user_challenges car elle est déjà dans ce module
    return check_user_challenges(user)