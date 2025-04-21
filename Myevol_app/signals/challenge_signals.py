# signals/challenge_signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from ..models import Challenge, ChallengeProgress, Notification
from ..services.challenge_service import update_challenge_progress
from ..services.badge_service import update_user_badges

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Challenge)
def log_challenge_creation(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque fois qu'un défi est créé.
    Enregistre un log pour l'événement de création et envoie une notification.
    """
    if created:
        logger.info(f"Défi créé : {instance.title} (ID: {instance.id})")
        # Envoi de notification à l'utilisateur ou à un groupe
        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Nouveau défi créé : {instance.title}",
            notif_type="defi"
        )

@receiver(post_save, sender=ChallengeProgress)
def update_progress(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque fois que la progression d'un utilisateur sur un défi est mise à jour.
    Appelle la méthode de mise à jour de la progression et vérifie si l'utilisateur a complété le défi.
    """
    if created:
        logger.info(f"Progression ajoutée pour l'utilisateur {instance.user.username} sur le défi {instance.challenge.title}")
        # On vérifie la progression de l'utilisateur sur ce défi
        update_challenge_progress(instance)
        
        # Vérification des badges et mise à jour si nécessaire
        update_user_badges(instance.user)

@receiver(post_delete, sender=ChallengeProgress)
def remove_progress(sender, instance, **kwargs):
    """
    Signal déclenché lors de la suppression d'une progression de défi.
    Met à jour les statistiques et enregistre un log de l'événement.
    """
    logger.info(f"Progression supprimée pour l'utilisateur {instance.user.username} sur le défi {instance.challenge.title}")
    
    # Mettre à jour les statistiques après suppression
    # Vous pouvez ajouter une logique pour recalculer les statistiques des utilisateurs ici, si nécessaire.
    # Exemple : DailyStat.update_user_stats(instance.user)

@receiver(post_save, sender=Challenge)
def check_challenge_end(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsque la date de fin d'un défi est atteinte.
    Ce signal peut être utilisé pour effectuer des actions comme attribuer des badges,
    envoyer une notification à l'utilisateur ou effectuer des calculs statistiques.
    """
    today = now().date()
    if not created and instance.end_date == today:
        logger.info(f"Le défi '{instance.title}' a pris fin aujourd'hui.")
        
        # Exemple : Attribuer un badge ou envoyer une notification à l'utilisateur
        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Le défi '{instance.title}' est terminé. Félicitations !",
            notif_type="defi_achèvement"
        )

        # Vous pouvez ajouter un service pour gérer la logique de fin de défi (par exemple, attribuer des badges)
        # update_user_badges(instance.user)
