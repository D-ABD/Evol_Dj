# MyEvol_app/models/notification_model.py

from django.db import models
from django.conf import settings
from django.utils.timezone import now
import logging

User = settings.AUTH_USER_MODEL

logger = logging.getLogger(__name__)

class Notification(models.Model):
    """
    Modèle représentant une notification pour un utilisateur.
    Permet d'informer l'utilisateur d'événements importants dans l'application.
    """

    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif atteint'),
        ('statistique', 'Mise à jour statistique'),
        ('info', 'Information générale'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(help_text="Contenu de la notification")
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info', help_text="Type de notification")
    is_read = models.BooleanField(default=False, help_text="Indique si la notification a été lue")
    read_at = models.DateTimeField(null=True, blank=True, help_text="Date de lecture de la notification")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de la notification")
    archived = models.BooleanField(default=False, help_text="Indique si la notification est archivée")
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text="Date programmée pour l'envoi de la notification")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'archived']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

    @property
    def type_display(self):
        """
        Retourne le label lisible du type de notification.
        """
        return dict(self.NOTIF_TYPES).get(self.notif_type, "Information générale")

    def archive(self):
        """
        Archive la notification sans suppression.
        """
        if not self.archived:
            self.archived = True
            self.save(update_fields=['archived'])

    def mark_as_read(self):
        """
        Marque la notification comme lue et enregistre la date de lecture.
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues d'un utilisateur comme lues.
        """
        unread = cls.objects.filter(user=user, is_read=False, archived=False)
        return unread.update(is_read=True, read_at=now())

    @classmethod
    def create_notification(cls, user, message, notif_type='info', scheduled_at=None):
        """
        Crée une nouvelle notification pour un utilisateur.
        """
        return cls.objects.create(
            user=user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )

# Signal : créer une notification lorsque l'utilisateur atteint un objectif
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def notify_user_of_new_goal(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de l'atteinte d'un objectif par un utilisateur.
    Crée une notification pour informer l'utilisateur de cet accomplissement.
    """
    if created:
        # Exemple d'objectif atteint
        Notification.create_notification(
            user=instance,
            message="Félicitations, vous avez atteint un nouvel objectif !",
            notif_type="objectif"
        )
        logger.info(f"Notification de succès d'objectif envoyée à {instance.username}")
