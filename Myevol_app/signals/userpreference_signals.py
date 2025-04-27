# signals/userPreference_signals.py

import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

from ..models.user_model import User
from ..models.userPreference_model import UserPreference

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=UserPreference)
def validate_user_preferences(sender, instance, **kwargs):
    """
    Valide certaines contraintes avant la sauvegarde des préférences utilisateur.

    Par exemple, limite la longueur de la couleur accentuée.
    """
    if len(instance.accent_color) > 7:
        logger.warning(f"[PREF] Couleur accent trop longue pour {instance.user.username}, ajustement automatique.")
        instance.accent_color = instance.accent_color[:7]
    logger.debug(f"[PREF] Préférences validées pour {instance.user.username}.")

@receiver(post_save, sender=UserPreference)
def handle_user_preferences_save(sender, instance, created, **kwargs):
    """
    Signal déclenché après la création ou mise à jour d'une instance de UserPreference.

    - Logue l'action
    - Met à jour les badges si nécessaire
    - Envoie une notification par e-mail si modifié
    """
    if created:
        logger.info(f"[PREF] Préférences créées pour {instance.user.username}.")
    else:
        logger.info(f"[PREF] Préférences mises à jour pour {instance.user.username}.")
        logger.info(f"[PREF] Mode sombre: {instance.dark_mode}, Couleur accent: {instance.accent_color}")

        # Envoi d'un e-mail de confirmation
        send_preference_update_notification(instance.user)

    # Mise à jour des badges liée aux préférences
    try:
        instance.user.update_badges()
    except ValidationError as e:
        logger.error(f"[PREF] Erreur lors de la mise à jour des badges de {instance.user.username}: {e}")

def send_preference_update_notification(user):
    """
    Envoie un e-mail à l'utilisateur pour confirmer la mise à jour de ses préférences.
    """
    subject = "📱 Mise à jour de vos préférences sur MyEvol"
    message = (
        f"Bonjour {user.username},\n\n"
        "Vos préférences ont été mises à jour avec succès.\n"
        "Merci d'utiliser MyEvol !\n\n"
        "— L'équipe MyEvol"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [user.email])
        logger.info(f"[MAIL] Notification envoyée à {user.email}")
    except Exception as e:
        logger.error(f"[MAIL] Échec d'envoi à {user.email}: {e}")

@receiver(post_save, sender=User)
def sync_user_preferences(sender, instance, **kwargs):
    """
    Synchronise certains champs de préférences utilisateur après mise à jour du profil.
    """
    prefs = getattr(instance, "preferences", None)
    if prefs:
        # Exemple : synchroniser une langue ou un thème
        prefs.save()
