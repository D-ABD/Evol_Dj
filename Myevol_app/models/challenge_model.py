# MyEvol_app/models/challenge_model.py

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
import logging
from django.core.exceptions import ValidationError



User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)

class Challenge(models.Model):
    """
    🎯 Modèle représentant un défi temporaire proposé aux utilisateurs.

    Les défis visent à stimuler l'engagement en fixant des objectifs à atteindre 
    dans une période donnée (ex : nombre d’entrées à réaliser en X jours).

    API Endpoints recommandés :
    - GET /api/challenges/ : Liste paginée des défis
    - GET /api/challenges/{id}/ : Détails d’un défi
    - GET /api/challenges/active/ : Liste des défis actifs uniquement
    - GET /api/challenges/{id}/participants/ : Liste des participants

    Champs calculés à exposer dans l’API :
    - is_active (bool) : Indique si le défi est actuellement actif
    - days_remaining (int) : Nombre de jours restants avant la fin du défi
    - participants_count (int) : Nombre de participants inscrits à ce défi
    """
    title = models.CharField(max_length=255, help_text="Titre du défi affiché à l'utilisateur")
    description = models.TextField(help_text="Description du défi et règles à suivre")
    start_date = models.DateField(help_text="Date de début du défi")
    end_date = models.DateField(help_text="Date de fin du défi")
    target_entries = models.PositiveIntegerField(
        default=5,
        help_text="Nombre d'entrées à réaliser pour réussir le défi"
    )

    class Meta:
        ordering = ['-end_date']
        verbose_name = "Défi"
        verbose_name_plural = "Défis"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Challenge title='{self.title}' target={self.target_entries} from={self.start_date} to={self.end_date}>"

    def get_absolute_url(self):
        """Retourne l'URL vers la vue de détail du défi."""
        return reverse('challenge_detail', kwargs={'pk': self.pk})

    @property
    def is_active(self):
        """Retourne True si le défi est actif aujourd’hui (entre start et end)."""
        today = now().date()
        return self.start_date <= today <= self.end_date

    @property
    def days_remaining(self):
        """Retourne le nombre de jours restants avant la fin du défi."""
        today = now().date()
        return max(0, (self.end_date - today).days)

    @property
    def participants_count(self):
        """Retourne le nombre de participants inscrits à ce défi."""
        return self.progresses.count()

    def is_completed(self, user):
        """
        Vérifie si l’utilisateur a complété le défi (atteint l’objectif d’entrées).
        """
        return user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count() >= self.target_entries

    def get_progress(self, user):
        """
        Calcule la progression de l’utilisateur sur ce défi.
        
        Args:
            user (User): Utilisateur pour lequel calculer la progression
        
        Returns:
            dict: Un dictionnaire contenant la progression sous forme de pourcentage
                  et d'informations sur le nombre actuel et le nombre cible d'entrées
        """
        current = user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count()

        completed = current >= self.target_entries
        percent = min(100, int((current / self.target_entries) * 100)) if self.target_entries > 0 else 0

        return {
            'percent': percent,
            'current': current,
            'target': self.target_entries,
            'completed': completed
        }

    def save(self, *args, **kwargs):
        """
        Redéfinition de la méthode save pour logguer la création de chaque défi.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            logger.info(f"Création d'un nouveau défi : {self.title} (ID: {self.id})")
    def clean(self):
        """Validation des contraintes métier du défi."""
        if self.start_date > self.end_date:
            raise ValidationError("La date de début doit précéder la date de fin.")

class ChallengeProgress(models.Model):
    """
    Suivi individuel d’un utilisateur sur un défi.
    Ce modèle est utilisé pour savoir si l'utilisateur a complété un défi et pour stocker
    l'état actuel de la progression sur ce défi.
    
    API recommandée :
    - GET /api/users/me/challenges/ : Liste des défis avec progression
    - GET /api/challenges/{id}/progress/ : Détails de la progression d'un utilisateur
    - POST /api/challenges/{id}/join/ : Rejoindre un défi
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="challenges",
        help_text="Utilisateur lié à ce défi"
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name="progresses",
        help_text="Défi concerné"
    )
    completed = models.BooleanField(default=False, help_text="Statut de complétion du défi")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Date de complétion")

    class Meta:
        unique_together = ('user', 'challenge')
        verbose_name = "Progression de défi"
        verbose_name_plural = "Progressions de défi"

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

    def __repr__(self):
        return f"<ChallengeProgress user='{self.user.username}' challenge='{self.challenge.title}' completed={self.completed}>"

    def get_absolute_url(self):
        """Retourne l’URL vers la vue de détail de la progression du défi."""
        return reverse('challenge_progress_detail', kwargs={'pk': self.pk})

    def get_progress(self):
        """
        Retourne la progression actuelle de l’utilisateur sur ce défi.
        
        Retourne la progression en termes de pourcentage, ainsi que l'état de complétion.
        """
        return self.challenge.get_progress(self.user)

    def save(self, *args, **kwargs):
        """
        Redéfinition de la méthode save pour logguer la mise à jour de la progression du défi.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        from ..models.event_log_model import EventLog

        if not is_new and self.completed and self.completed_at is None:
            self.completed_at = now()
            EventLog.log_action(
                action="defi_termine",
                description=f"{self.user.username} a complété le défi '{self.challenge.title}'",
                user=self.user,
                metadata={"challenge_id": self.challenge.id}
            )
