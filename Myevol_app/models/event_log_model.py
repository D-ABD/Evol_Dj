# MyEvol_app/models/event_log_model.py

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)
User = settings.AUTH_USER_MODEL


class EventLog(models.Model):
    """
    📋 Journalisation des événements système ou utilisateur.
    
    Ce modèle trace toutes les actions notables de l'application, que ce soit côté utilisateur
    (ex : "connexion", "attribution_badge") ou côté système (ex : "nettoyage_quotidien").

    ✅ Objectifs :
    - Faciliter l’audit et le debug
    - Offrir des statistiques d’usage
    - Suivre les événements critiques

    🔗 Endpoints API recommandés :
    - GET /api/logs/
    - GET /api/users/{id}/logs/
    - GET /api/logs/statistics/

    🔧 Champs calculés à exposer :
    - temps_écoulé (depuis l’événement)
    - résumé (action + date)
    
    📦 Services liés :
    - Peut être appelé depuis n’importe quel service via `EventLog.log_action(...)`
    """
    
    SEVERITY_CHOICES = [
        ('INFO', 'Information'),
        ('WARN', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="event_logs",
        help_text="Utilisateur concerné par l’événement (optionnel pour les logs système)"
    )
    action = models.CharField(
        max_length=255,
        help_text="Type d'action enregistrée (ex : 'connexion', 'attribution_badge')"
    )
    description = models.TextField(
        blank=True,
        help_text="Détail ou message libre sur l'événement"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Horodatage de l’événement (généré automatiquement)"
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Données additionnelles liées à l’événement (ex : id d’un badge, durée, etc.)"
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='INFO',
        help_text="Niveau de gravité de l'événement"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        indexes = [
            models.Index(fields=["user", "action"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} - {self.action}"

    def __repr__(self):
        return f"<EventLog id={self.id} action='{self.action}' user='{self.user}' at='{self.created_at}'>"

    def get_absolute_url(self):
        return reverse("eventlog-detail", kwargs={"pk": self.pk})

    @classmethod
    def log_action(cls, action, description="", user=None, severity="INFO", **metadata):
        """
        ✅ Crée un log d’événement, appelé depuis services/signaux/vues.

        Args:
            action (str): Type d’action enregistrée
            description (str): Détail complémentaire de l’événement
            user (User, optional): Utilisateur concerné
            severity (str): Gravité de l'événement (INFO, WARN, ERROR, CRITICAL)
            **metadata (dict): Données personnalisées stockées en JSON

        Returns:
            EventLog: Instance sauvegardée
        """
        log = cls.objects.create(
            action=action,
            description=description,
            user=user,
            severity=severity,
            metadata=metadata or None
        )
        username = getattr(user, 'username', 'System')
        logger.info(f"[LOG] {username} > {action} > {description} > Severity: {severity}")
        return log

    @classmethod
    def get_action_counts(cls, days=30, user=None):
        """
        📊 Statistiques agrégées des événements.

        Args:
            days (int): Nombre de jours à considérer depuis aujourd’hui
            user (User, optional): Filtrer les événements par utilisateur

        Returns:
            dict: Clés = action, Valeurs = nombre d’occurrences

        Exemple :
            {'connexion': 31, 'attribution_badge': 12}
        """
        since = now() - timedelta(days=days)
        qs = cls.objects.filter(created_at__gte=since)
        if user:
            qs = qs.filter(user=user)
        return dict(qs.values("action").annotate(count=Count("id")).values_list("action", "count"))

    def has_metadata(self):
        return bool(self.metadata)
