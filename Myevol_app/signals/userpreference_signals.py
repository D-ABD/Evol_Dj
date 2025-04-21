# signals/userPreference_signals.py

import logging
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from ..models.userPreference_model import UserPreference
from ..services.userpreference_service import create_or_update_preferences

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserPreference)
def handle_user_preference_update(sender, instance, created, **kwargs):
    """
    Signal qui gère la mise à jour des préférences après la création ou la modification d'un objet UserPreference.
    
    Args:
        sender: Le modèle ayant envoyé le signal (UserPreference).
        instance: L'instance de l'objet UserPreference créé ou mis à jour.
        created: Boolean indiquant si l'instance est nouvellement créée.
        **kwargs: Autres arguments du signal.
    """
    if created:
        logger.info(f"Préférences créées pour l'utilisateur {instance.user.username}")
    else:
        logger.info(f"Préférences mises à jour pour l'utilisateur {instance.user.username}")
    
    # Action supplémentaire après la création ou mise à jour (par exemple, notifications)
    try:
        instance.user.update_badges()
    except ValidationError as e:
        logger.error(f"Erreur lors de la mise à jour des badges pour {instance.user.username}: {e}")

@receiver(post_save, sender=UserPreference)
def create_default_preferences(sender, instance, created, **kwargs):
    """
    Crée les préférences par défaut pour l'utilisateur si elles n'ont pas été créées automatiquement.
    """
    if created:
        logger.info(f"Préférences créées pour l'utilisateur {instance.user.username}")
        instance.create_default_preferences()
    else:
        logger.info(f"Préférences mises à jour pour l'utilisateur {instance.user.username}")


@receiver(pre_save, sender=UserPreference)
def validate_preferences(sender, instance, **kwargs):
    """
    Valider les préférences avant leur enregistrement.
    """
    if len(instance.accent_color) > 7:
        logger.warning(f"Couleur accent trop longue pour {instance.user.username}, modification nécessaire.")
        instance.accent_color = instance.accent_color[:7]  # Couper à la longueur correcte
    if instance.xp < 0:
        raise ValidationError("XP ne peut pas être négatif.")
    logger.info(f"Préférences validées avant l'enregistrement pour {instance.user.username}.")

def send_preference_update_notification(user):
    """
    Envoie une notification par email à l'utilisateur lorsque ses préférences sont modifiées.
    """
    subject = "Mise à jour de vos préférences"
    message = f"Bonjour {user.username},\n\nVos préférences d'application ont été mises à jour avec succès.\n\nCordialement,\nL'équipe de MyEvol."
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [user.email])
        logger.info(f"Email de notification envoyé à {user.email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email de notification à {user.email}: {e}")

@receiver(post_save, sender=UserPreference)
def send_notification_on_preference_change(sender, instance, created, **kwargs):
    """
    Envoie une notification à l'utilisateur lorsque ses préférences sont mises à jour.
    """
    if not created:
        # Exemple d'envoi d'email de notification sur mise à jour des préférences
        logger.info(f"Envoi de notification à {instance.user.username} après mise à jour des préférences.")
        # L'appel à la méthode de notification (ex: email ou enregistrement dans une file d'attente de notification)
        send_preference_update_notification(instance.user)

@receiver(post_save, sender=UserPreference)
def log_preferences_change(sender, instance, created, **kwargs):
    """
    Log les modifications des préférences d'un utilisateur pour un suivi.
    """
    if not created:
        logger.info(f"Changement de préférence pour l'utilisateur {instance.user.username}.")
        logger.info(f"Paramètre changé: {instance.accent_color}, Mode sombre: {instance.dark_mode}.")
