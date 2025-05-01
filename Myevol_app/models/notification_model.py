from django.db import models
from django.conf import settings
from django.utils.timezone import now
import logging
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)

class Notification(models.Model):
    """
    Modèle représentant une notification envoyée à un utilisateur.
    Permet d'informer l'utilisateur d'événements importants, comme des badges obtenus ou des objectifs atteints.
    
    Types de notifications :
    - badge : Notification liée à un badge débloqué
    - objectif : Notification liée à un objectif atteint
    - statistique : Notification sur l'évolution des statistiques
    - info : Notification informative générale
    """

    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif atteint'),
        ('statistique', 'Mise à jour statistique'),
        ('info', 'Information générale'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="Utilisateur concerné par la notification"
    )
    message = models.TextField(help_text="Contenu textuel de la notification à afficher à l'utilisateur")
    notif_type = models.CharField(
        max_length=20,
        choices=NOTIF_TYPES,
        default='info',
        help_text="Type de la notification (ex : badge, statistique, info)"
    )
    is_read = models.BooleanField(default=False, help_text="Indique si la notification a été lue")
    read_at = models.DateTimeField(null=True, blank=True, help_text="Date à laquelle la notification a été lue")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de la notification")
    archived = models.BooleanField(default=False, help_text="Indique si la notification a été archivée")
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text="Date programmée pour afficher la notification")
    temporary_field = models.BooleanField(default=False)  # TEMPORAIRE

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'archived']),
        ]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        """
        Représentation textuelle d'une notification.
        """
        return f"{self.user.username} - {self.message[:50]}"

    @property
    def type_display(self):
        """
        Retourne l’étiquette lisible du type de notification.

        Returns:
            str: Libellé utilisateur du type de notification
        """
        return dict(self.NOTIF_TYPES).get(self.notif_type, "Information générale")

    def archive(self):
        """
        Archive la notification sans la supprimer.

        Effet :
            Met à jour le champ `archived` à True si ce n'est pas déjà fait.
        """
        if not self.archived:
            self.archived = True
            self.save(update_fields=['archived'])
            logger.info(f"[NOTIF] Notification archivée pour {self.user.username}")

    def mark_as_read(self):
        """
        Marque la notification comme lue, enregistre l'heure de lecture.

        Effet :
            - is_read = True
            - read_at = maintenant
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])
            logger.info(f"[NOTIF] Notification lue pour {self.user.username}")

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues d’un utilisateur comme lues.

        Args:
            user (User): Utilisateur cible

        Returns:
            int: Nombre de notifications mises à jour
        """
        unread = cls.objects.filter(user=user, is_read=False, archived=False)
        count = unread.update(is_read=True, read_at=now())
        logger.info(f"[NOTIF] {count} notifications marquées comme lues pour {user.username}")
        return count

    @classmethod
    def create_notification(cls, user, message, notif_type='info', scheduled_at=None):
        """
        Crée une notification pour un utilisateur.

        Args:
            user (User): Utilisateur concerné
            message (str): Contenu de la notification
            notif_type (str): Type de notification parmi : 'badge', 'objectif', 'statistique', 'info'
            scheduled_at (datetime, optional): Date à laquelle afficher la notification

        Returns:
            Notification: Instance créée
        """
        notif = cls.objects.create(
            user=user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )
        logger.info(f"[NOTIF] Nouvelle notification '{notif_type}' créée pour {user.username}")
        return notif

    def clean(self):
        """Validation renforcée pour garantir un type de notification valide."""
        if self.notif_type not in dict(self.NOTIF_TYPES):
            raise ValidationError({'notif_type': f"Type de notification invalide : {self.notif_type}"})
