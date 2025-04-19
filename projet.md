from datetime import timedelta
from collections import defaultdict

from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.db.models import Avg, Count

from django.conf import settings
User = settings.AUTH_USER_MODEL



# 🏅 Badge obtenu
class Badge(models.Model):
    """
    Modèle représentant un badge obtenu par un utilisateur.
    Les badges sont des récompenses pour des accomplissements spécifiques.
    
    API Endpoints suggérés:
    - GET /api/badges/ - Liste des badges de l'utilisateur courant
    - GET /api/users/{id}/badges/ - Liste des badges d'un utilisateur spécifique
    - GET /api/badges/recent/ - Badges récemment obtenus
    
    Exemple de sérialisation JSON:
    {
        "id": 1,
        "name": "Niveau 3",
        "description": "Tu as atteint le niveau 3 💪",
        "icon": "🥈",
        "date_obtenue": "2025-04-20",
        "level": 3
    }
    """
    name = models.CharField(max_length=100)  # Nom du badge
    description = models.TextField()         # Description du badge
    icon = models.CharField(max_length=100)  # Icône (chemin ou identifiant)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    date_obtenue = models.DateField(auto_now_add=True)  # Date d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['-date_obtenue']
        unique_together = ('name', 'user')  # Un utilisateur ne peut avoir qu'un badge avec le même nom
        
        """
        Filtres API recommandés:
        - name (exact, contains)
        - date_obtenue (range, gte, lte)
        - level (exact, gte, lte)
        """

    def __str__(self):
        """Représentation en chaîne de caractères du badge"""
        return f"{self.name} ({self.user.username})"

    def was_earned_today(self, reference_date=None):
        """
        Vérifie si le badge a été obtenu aujourd'hui.

        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)

        Returns:
            bool: True si le badge a été obtenu aujourd'hui, False sinon
            
        Utilisation dans l'API:
            Ce champ peut être exposé comme booléen calculé 'is_new' dans la sérialisation
            pour permettre à l'interface d'afficher un indicateur visuel pour les nouveaux badges.
        """
        if reference_date is None:
            reference_date = now().date()
        return self.date_obtenue == reference_date

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour créer automatiquement 
        une notification lorsqu'un badge est attribué.
        
        Note pour l'API:
        Lors de la création d'un badge via l'API, une notification sera également générée.
        Il n'est pas nécessaire de créer explicitement une notification dans la vue API.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # ⏱ Import local pour éviter les imports circulaires
            from .notification_model import Notification
            from .event_log_model import EventLog

            # Crée une notification pour informer l'utilisateur
            Notification.objects.create(
                user=self.user,
                message=f"🏅 Nouveau badge débloqué : {self.name}",
                notif_type="badge"
            )

            # Enregistre l'événement dans les logs du système
            EventLog.objects.create(
                user=self.user,
                action="attribution_badge",
                description=f"Badge '{self.name}' attribué à {self.user.username}"
            )


# 🧩 BadgeTemplate : tous les badges définissables
class BadgeTemplate(models.Model):
    """
    Modèle définissant les différents badges disponibles dans l'application.
    Contient les critères d'attribution des badges aux utilisateurs.
    
    API Endpoints suggérés:
    - GET /api/badges/templates/ - Liste tous les templates de badges
    - GET /api/badges/templates/{id}/ - Détails d'un template spécifique
    - GET /api/badges/templates/categories/ - Templates groupés par catégorie
    - GET /api/badges/templates/{id}/progress/ - Progression de l'utilisateur vers ce badge
    """
    name = models.CharField(max_length=100, unique=True)  # Nom unique du badge
    description = models.TextField()                      # Description du badge
    icon = models.CharField(max_length=100)               # Icône (chemin ou identifiant)
    condition = models.CharField(max_length=255)          # Description de la condition d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)

    class Meta:
        verbose_name = "Modèle de badge"
        verbose_name_plural = "Modèles de badges"
        
        """
        Filtres API recommandés:
        - name (exact, contains)
        - condition (contains)
        - level (exact, gte, lte)
        """

    def __str__(self):
        """Représentation en chaîne de caractères du template de badge"""
        return self.name

    def check_unlock(self, user):
        """
        Vérifie si un utilisateur remplit les conditions pour débloquer ce badge.

        Cette méthode contient la logique détaillée pour chaque type de badge.

        Args:
            user (User): L'utilisateur à vérifier

        Returns:
            bool: True si l'utilisateur remplit les conditions, False sinon
            
        Utilisation dans l'API:
            Cette méthode est idéale pour le calcul de la progression vers les badges:
            
            1. Pour les endpoints /api/badges/progress/ qui montrent tous les badges
               et la progression de l'utilisateur vers leur obtention
            
            2. Pour calculer le pourcentage de progression pour des badges complexes,
               comme les badges de séquence (jours consécutifs)
               
        Exemples d'utilisation:
            # Vérifier si l'utilisateur peut débloquer ce badge
            can_unlock = badge_template.check_unlock(request.user)
            
            # Dans un sérialiseur avec un champ calculé
            @property
            def is_unlocked(self):
                return self.instance.check_unlock(self.context['request'].user)
        """
        total = user.total_entries()
        mood_avg = user.mood_average(7)

        # Dictionnaire des conditions
        conditions = {
            "Première entrée": total >= 1,
            "Régulier": user.has_entries_every_day(5),
            "Discipline": user.has_entries_every_day(10),
            "Résilience": user.has_entries_every_day(15),
            "Légende du Journal": user.has_entries_every_day(30),
            "Ambassadeur d'humeur": mood_avg is not None and mood_avg >= 9,
            "Productivité": user.entries_today() >= 3,
            "Objectif rempli !": user.all_objectives_achieved(),
            "Persévérance": total >= 100,
        }

        # Condition personnalisée
        if self.name in conditions:
            return conditions[self.name]

        # Cas spécial pour les badges de niveau (ex: "Niveau 3")
        if self.name.startswith("Niveau"):
            try:
                level_number = int(self.name.split(" ")[1])
                thresholds = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]
                return total >= thresholds[level_number - 1]
            except (ValueError, IndexError):
                return False

        return False  # Par défaut, on ne débloque pas
    
    def get_progress(self, user):
        """
        Calcule le pourcentage de progression d'un utilisateur vers l'obtention de ce badge.
        
        Args:
            user (User): L'utilisateur dont on veut calculer la progression
            
        Returns:
            dict: Dictionnaire contenant le pourcentage et des informations sur la progression
                {
                    'percent': 70,  # Pourcentage de progression (0-100)
                    'current': 7,   # Valeur actuelle (ex: nombre d'entrées)
                    'target': 10,   # Valeur cible
                    'unlocked': False  # Si le badge est déverrouillé
                }
        
        Utilisation dans l'API:
            Idéal pour un endpoint /api/badges/templates/{id}/progress/
            ou comme champ calculé dans la sérialisation des templates de badge.
        """
        # Si le badge est déjà débloqué, retourner 100%
        if user.badges.filter(name=self.name).exists():
            return {'percent': 100, 'unlocked': True}
            
        total = user.total_entries()
        
        # Logique spécifique par type de badge
        if self.name == "Première entrée":
            return {
                'percent': 100 if total >= 1 else 0,
                'current': min(total, 1),
                'target': 1,
                'unlocked': total >= 1
            }
            
        elif self.name.startswith("Niveau"):
            try:
                level_number = int(self.name.split(" ")[1])
                thresholds = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]
                target = thresholds[level_number - 1]
                previous = thresholds[level_number - 2] if level_number > 1 else 0
                
                # Calcul du pourcentage entre le seuil précédent et le seuil actuel
                if total >= target:
                    percent = 100
                else:
                    percent = ((total - previous) / (target - previous)) * 100
                    percent = max(0, min(99, percent))  # Limite entre 0 et 99%
                
                return {
                    'percent': int(percent),
                    'current': total,
                    'target': target,
                    'unlocked': total >= target
                }
            except (ValueError, IndexError):
                return {'percent': 0, 'unlocked': False}
                
        # Cas par défaut: soit 0% soit 100%
        return {
            'percent': 100 if self.check_unlock(user) else 0,
            'unlocked': self.check_unlock(user)
        }

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from .notification_model import Notification

from django.conf import settings
User = settings.AUTH_USER_MODEL



# 🎯 Modèle principal de défi
class Challenge(models.Model):
    """
    Modèle représentant un défi temporaire proposé aux utilisateurs.
    Les défis encouragent l'engagement en fixant des objectifs à atteindre dans une période donnée.
    
    API Endpoints suggérés:
    - GET /api/challenges/ - Liste tous les défis (avec filtres actifs/inactifs)
    - GET /api/challenges/{id}/ - Détails d'un défi spécifique
    - GET /api/challenges/active/ - Liste uniquement les défis actuellement actifs
    - GET /api/challenges/{id}/participants/ - Liste les utilisateurs participant à un défi
    
    Exemple de sérialisation JSON:
    {
        "id": 1,
        "title": "Marathon d'entrées",
        "description": "Créez 15 entrées en 7 jours !",
        "start_date": "2025-04-15",
        "end_date": "2025-04-22",
        "target_entries": 15,
        "is_active": true,
        "days_remaining": 3,
        "participants_count": 24
    }
    """
    title = models.CharField(max_length=255)  # Titre du défi
    description = models.TextField()          # Description détaillée
    start_date = models.DateField()           # Date de début du défi
    end_date = models.DateField()             # Date de fin du défi
    target_entries = models.PositiveIntegerField(default=5)  # Objectif d'entrées à atteindre

    class Meta:
        """
        Filtres API recommandés:
        - title (exact, contains)
        - start_date, end_date (gte, lte, range)
        - is_active (boolean calculé)
        """
        ordering = ['-end_date']  # Tri par défaut: défis se terminant bientôt en premier
        verbose_name = "Défi"
        verbose_name_plural = "Défis"

    def __str__(self):
        return f"{self.title} ({self.start_date} → {self.end_date})"

    def is_active(self):
        """
        Vérifie si le défi est actuellement actif.

        Returns:
            bool: True si actif aujourd'hui, sinon False.
            
        Utilisation dans l'API:
            Ce champ devrait être inclus comme champ calculé (SerializerMethodField)
            dans la sérialisation pour permettre de filtrer facilement les défis actifs.
            
        Exemple d'implémentation dans un sérialiseur:
            @property
            def is_active(self):
                return self.instance.is_active()
        """
        today = now().date()
        return self.start_date <= today <= self.end_date
        
    def days_remaining(self):
        """
        Calcule le nombre de jours restants avant la fin du défi.
        
        Returns:
            int: Nombre de jours jusqu'à la fin, ou 0 si le défi est terminé
            
        Utilisation dans l'API:
            Utile comme champ calculé pour l'affichage dans l'interface utilisateur.
        """
        today = now().date()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days

    def is_completed(self, user):
        """
        Vérifie si l'utilisateur a atteint l'objectif d'entrées pendant la période du défi.

        Args:
            user (User): L'utilisateur à évaluer

        Returns:
            bool: True si l'objectif est atteint
            
        Utilisation dans l'API:
            Cette méthode peut être utilisée pour créer un champ calculé 'is_completed'
            dans la sérialisation des défis, personnalisée pour chaque utilisateur.
            
        Exemple d'implémentation dans un sérialiseur:
            def get_is_completed(self, obj):
                user = self.context['request'].user
                return obj.is_completed(user)
        """
        return user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count() >= self.target_entries
        
    def get_progress(self, user):
        """
        Calcule la progression de l'utilisateur vers l'accomplissement du défi.
        
        Args:
            user (User): L'utilisateur dont on calcule la progression
            
        Returns:
            dict: Dictionnaire contenant les informations de progression
                {
                    'percent': 60,  # Pourcentage de progression (0-100)
                    'current': 9,   # Nombre actuel d'entrées
                    'target': 15,   # Objectif à atteindre
                    'completed': False  # Si l'objectif est atteint
                }
                
        Utilisation dans l'API:
            Idéal pour un endpoint /api/challenges/{id}/progress/
            ou comme champ calculé dans la sérialisation des défis.
        """
        current = user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count()
        
        completed = current >= self.target_entries
        percent = min(100, int((current / self.target_entries) * 100))
        
        return {
            'percent': percent,
            'current': current,
            'target': self.target_entries,
            'completed': completed
        }


# 🔁 Modèle de progression utilisateur pour chaque défi
class ChallengeProgress(models.Model):
    """
    Suivi de la progression d'un utilisateur sur un défi.
    Évite les doublons et garde trace de la date de complétion.
    
    API Endpoints suggérés:
    - GET /api/users/me/challenges/ - Liste les défis de l'utilisateur courant avec progression
    - GET /api/challenges/{id}/progress/ - Progression de l'utilisateur sur un défi spécifique
    - PATCH /api/challenges/{id}/join/ - Rejoindre un défi (crée une entrée de progression)
    
    Exemple de sérialisation JSON:
    {
        "id": 5,
        "challenge": {
            "id": 1,
            "title": "Marathon d'entrées",
            "description": "Créez 15 entrées en 7 jours !"
        },
        "completed": true,
        "completed_at": "2025-04-18T14:32:51Z",
        "progress": {
            "percent": 100,
            "current": 15,
            "target": 15
        }
    }
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="challenges")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="progresses")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')  # Un seul lien par utilisateur/défi
        
        """
        Filtres API recommandés:
        - challenge (exact)
        - completed (boolean)
        - completed_at (date, gte, lte)
        """

    def __str__(self):
        return f"{self.user.username} → {self.challenge.title} ({'✅' if self.completed else '⏳'})"
        
    def get_progress(self):
        """
        Calcule la progression actuelle pour cet utilisateur sur ce défi.
        
        Returns:
            dict: Informations de progression (similaire à Challenge.get_progress)
            
        Utilisation dans l'API:
            Cette méthode peut servir à enrichir la sérialisation du modèle.
        """
        return self.challenge.get_progress(self.user)


# 🔎 Vérification globale de tous les défis actifs pour un utilisateur
def check_challenges(user):
    """
    Vérifie tous les défis actifs pour l'utilisateur.
    Si l'utilisateur a complété un défi, il est marqué comme tel,
    une notification est envoyée.

    Args:
        user (User): L'utilisateur à vérifier
        
    Utilisation dans l'API:
        Cette fonction devrait être appelée après toute création d'entrée de journal
        via un signal post_save ou directement dans la vue API qui gère la création d'entrées.
        
    Exemple d'utilisation dans une vue API:
        @action(detail=False, methods=['post'])
        def create_entry(self, request):
            # ... logique de création d'entrée ...
            check_challenges(request.user)
            return Response(...)
    """
    today = now().date()

    # Parcourt tous les défis actifs
    for challenge in Challenge.objects.filter(start_date__lte=today, end_date__gte=today):
        progress, _ = ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)

        if not progress.completed and challenge.is_completed(user):
            # Mise à jour de la progression
            progress.completed = True
            progress.completed_at = now()
            progress.save()

            # Notification à l'utilisateur
            Notification.objects.create(
                user=user,
                message=f"🎯 Tu as terminé le défi : {challenge.title} !",
                notif_type="objectif"
            )

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError


class EventLog(models.Model):
    """
    Modèle pour enregistrer les événements et actions importantes dans l'application.
    Permet de tracer l'activité des utilisateurs et les événements système
    pour l'audit, le débogage ou l'analyse des comportements utilisateurs.
    
    API Endpoints suggérés:
    - GET /api/logs/ - Liste des événements (admin seulement)
    - GET /api/users/{id}/logs/ - Événements d'un utilisateur spécifique
    - GET /api/logs/actions/ - Liste des types d'actions disponibles
    - GET /api/logs/statistics/ - Statistiques agrégées des événements
    
    Exemple de sérialisation JSON:
    {
        "id": 421,
        "user": {
            "id": 8,
            "username": "john_doe"
        },
        "action": "attribution_badge",
        "description": "Badge 'Niveau 3' attribué à john_doe",
        "created_at": "2025-04-19T14:30:25Z"
    }
    """

    # Lien vers l'utilisateur concerné (optionnel pour les événements système)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # ou SET_NULL si on veut garder les logs après suppression
        related_name="event_logs",
        null=True,
        blank=True,  # Permet les logs système sans utilisateur associé
    )

    # Type d'action effectuée (ex: "connexion", "création_entrée", "attribution_badge", etc.)
    action = models.CharField(max_length=255)

    # Détails supplémentaires sur l'événement
    description = models.TextField(blank=True)

    # Horodatage automatique de l'événement
    created_at = models.DateTimeField(auto_now_add=True)

    # Données additionnelles au format JSON (optionnel pour stocker des métadonnées flexibles)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        
        """
        Filtres API recommandés:
        - user (exact)
        - action (exact, contains, in)
        - created_at (date, datetime, range, gte, lte)
        - description (contains)
        
        Sécurité API:
        - Limiter l'accès aux logs aux utilisateurs avec permissions admin
        - Pour les utilisateurs standards, ne montrer que leurs propres logs
        - Pagination obligatoire (max 50-100 items par page)
        """
        
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        """
        Représentation textuelle du log d'événement.
        Ex: "2025-04-19 14:30 - attribution_badge"
        """
        return f"{self.created_at:%Y-%m-%d %H:%M} - {self.action}"
    
    @classmethod
    def log_action(cls, action, description="", user=None, **metadata):
        """
        Méthode utilitaire pour créer facilement un log d'événement.
        
        Args:
            action (str): Type d'action (ex: "connexion", "création_entrée")
            description (str): Description détaillée de l'événement
            user (User, optional): Utilisateur concerné (None pour événement système)
            **metadata: Données supplémentaires à stocker au format JSON
        
        Returns:
            EventLog: L'objet EventLog créé
            
        Utilisation dans l'API:
            Cette méthode simplifie l'enregistrement d'événements dans les vues API.
            
        Exemple:
            @action(detail=True, methods=['post'])
            def complete_challenge(self, request, pk=None):
                challenge = self.get_object()
                # Logique de complétion...
                EventLog.log_action(
                    "challenge_completed",
                    f"Défi '{challenge.title}' complété",
                    user=request.user,
                    challenge_id=challenge.id,
                    time_spent_days=(now().date() - challenge.start_date).days
                )
                return Response(...)
        """
        return cls.objects.create(
            action=action,
            description=description,
            user=user,
            metadata=metadata or None
        )
    
    @classmethod
    def get_action_counts(cls, days=30, user=None):
        """
        Retourne des statistiques sur le nombre d'événements par type d'action.
        
        Args:
            days (int): Nombre de jours à considérer
            user (User, optional): Limiter aux événements d'un utilisateur spécifique
            
        Returns:
            dict: Dictionnaire {action: count} avec les totaux par action
            
        Utilisation dans l'API:
            Parfait pour un endpoint de statistiques ou de tableau de bord.
            
        Exemple API:
            @action(detail=False, methods=['get'])
            def statistics(self, request):
                stats = EventLog.get_action_counts(
                    days=int(request.query_params.get('days', 30)),
                    user=request.user if not request.user.is_staff else None
                )
                return Response(stats)
        """
        from django.db.models import Count
        
        # Filtre de base sur la période
        since = now() - timedelta(days=days)
        query = cls.objects.filter(created_at__gte=since)
        
        # Filtre optionnel par utilisateur
        if user:
            query = query.filter(user=user)
            
        # Agrégation par action
        return dict(
            query.values('action')
                .annotate(count=Count('id'))
                .values_list('action', 'count')
        )
from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.conf import settings
User = settings.AUTH_USER_MODEL

# 📓 Entrée de journal
class JournalEntry(models.Model):
    """
    Modèle représentant une entrée de journal.
    Chaque entrée est liée à un utilisateur, a un contenu, une note d'humeur et une catégorie.
    
    API Endpoints suggérés:
    - GET /api/journal-entries/ - Liste des entrées de l'utilisateur courant
    - POST /api/journal-entries/ - Créer une nouvelle entrée
    - GET /api/journal-entries/{id}/ - Détails d'une entrée spécifique
    - PUT/PATCH /api/journal-entries/{id}/ - Modifier une entrée existante
    - DELETE /api/journal-entries/{id}/ - Supprimer une entrée
    - GET /api/journal-entries/stats/ - Statistiques sur les entrées (par catégorie, humeur, etc.)
    - GET /api/journal-entries/calendar/ - Données pour vue calendrier (dates avec entrées)
    
    Exemple de sérialisation JSON:
    {
        "id": 123,
        "content": "J'ai terminé le projet principal aujourd'hui !",
        "mood": 8,
        "mood_emoji": "😁",  // Champ calculé
        "category": "Travail",
        "created_at": "2025-04-19T15:30:22Z",
        "updated_at": "2025-04-19T15:32:45Z",
        "media": [  // Relation imbriquée
            {
                "id": 45,
                "type": "image",
                "file_url": "/media/journal_media/image123.jpg"
            }
        ]
    }
    """

    # Choix d'humeur de 1 à 10
    MOOD_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]
    
    # Mapping des émojis pour chaque niveau d'humeur (utile pour l'API)
    MOOD_EMOJIS = {
        1: "😡", 2: "😠", 3: "😟", 4: "😐", 
        5: "🙂", 6: "😊", 7: "😃", 8: "😁", 
        9: "🤩", 10: "😍"
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries")
    content = models.TextField(verbose_name="Qu'avez-vous accompli aujourd'hui ?")
    mood = models.IntegerField(
        choices=MOOD_CHOICES,
        verbose_name="Note d'humeur",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    category = models.CharField(max_length=100, verbose_name="Catégorie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entrée de journal"
        verbose_name_plural = "Entrées de journal"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['category']),
        ]
        
        """
        Filtres API recommandés:
        - created_at (date, datetime, range, gte, lte)
        - mood (exact, gte, lte, range)
        - category (exact, in)
        - search (recherche dans le contenu)
        
        Permissions API:
        - Un utilisateur ne doit voir et modifier que ses propres entrées
        - Limiter le nombre de créations par jour si nécessaire
        """

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"
        
    def get_mood_emoji(self):
        """
        Retourne l'emoji correspondant à la note d'humeur.
        
        Returns:
            str: Emoji représentant l'humeur
            
        Utilisation dans l'API:
            Idéal comme champ calculé dans un sérialiseur pour afficher
            visuellement l'humeur dans l'interface utilisateur.
            
        Exemple dans un sérialiseur:
            @property
            def mood_emoji(self):
                return self.instance.get_mood_emoji()
        """
        return self.MOOD_EMOJIS.get(self.mood, "😐")

    def clean(self):
        """
        Validation personnalisée pour s'assurer que le contenu est suffisamment long.
        
        Raises:
            ValidationError: Si le contenu est trop court
            
        Utilisation dans l'API:
            Ces validations doivent être reproduites dans les sérialiseurs
            pour assurer la cohérence des données.
            
        Exemple dans un sérialiseur:
            def validate_content(self, value):
                if len(value.strip()) < 5:
                    raise serializers.ValidationError(
                        'Le contenu doit comporter au moins 5 caractères.'
                    )
                return value
        """
        super().clean()
        if self.content and len(self.content.strip()) < 5:
            raise ValidationError({'content': 'Le contenu doit comporter au moins 5 caractères.'})

    def save(self, *args, **kwargs):
        """
        Surcharge de save : met à jour les stats, badges, streaks, défis.
        
        Utilisation dans l'API:
            La création d'une entrée via l'API déclenchera automatiquement
            toutes ces actions associées. Pas besoin de code supplémentaire
            dans les vues API pour ces fonctionnalités.
            
        Note importante:
            Lors de la sauvegarde d'une entrée depuis l'API, plusieurs 
            événements sont déclenchés en cascade. Cela peut impacter la performance
            pour des requêtes à haut volume. Considérer une tâche asynchrone
            pour la mise à jour des statistiques et badges si nécessaire.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # ⏱ Import local pour éviter les imports circulaires
            from .stats_model import DailyStat
            from .challenge_model import check_challenges

            # ➕ Mise à jour des statistiques journalières
            DailyStat.generate_for_user(self.user, self.created_at.date())

            # ✅ Vérification des défis
            check_challenges(self.user)

            # 🏅 Mise à jour des badges
            self.user.update_badges()

            # 🔥 Mise à jour des séries de jours consécutifs
            self.user.update_streaks()

    @staticmethod
    def count_today(user, reference_date=None):
        """
        Compte les entrées faites aujourd'hui (ou à une date donnée).
        
        Args:
            user (User): L'utilisateur concerné
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre d'entrées à la date spécifiée
            
        Utilisation dans l'API:
            Utile pour les endpoints de statistiques ou pour vérifier
            si l'utilisateur a atteint une limite quotidienne.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def daily_count(self, request):
                count = JournalEntry.count_today(request.user)
                return Response({'count': count})
        """
        if reference_date is None:
            reference_date = now().date()
        return user.entries.filter(created_at__date=reference_date).count()
        
    @classmethod
    def get_entries_by_date_range(cls, user, start_date, end_date):
        """
        Récupère les entrées dans une plage de dates spécifique.
        
        Args:
            user (User): L'utilisateur concerné
            start_date (date): Date de début
            end_date (date): Date de fin
            
        Returns:
            QuerySet: Entrées dans la plage de dates spécifiée
            
        Utilisation dans l'API:
            Parfait pour les endpoints de calendrier ou de rapports périodiques.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def date_range(self, request):
                start = request.query_params.get('start')
                end = request.query_params.get('end')
                entries = JournalEntry.get_entries_by_date_range(
                    request.user, 
                    parse_date(start), 
                    parse_date(end)
                )
                return Response(self.get_serializer(entries, many=True).data)
        """
        return cls.objects.filter(
            user=user,
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )
        
    @classmethod
    def get_category_suggestions(cls, user, limit=10):
        """
        Retourne les catégories les plus utilisées par l'utilisateur.
        
        Args:
            user (User): L'utilisateur concerné
            limit (int): Nombre maximum de suggestions à retourner
            
        Returns:
            list: Liste des catégories les plus utilisées
            
        Utilisation dans l'API:
            Idéal pour un endpoint d'autocomplétion des catégories.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def category_suggestions(self, request):
                suggestions = JournalEntry.get_category_suggestions(request.user)
                return Response(suggestions)
        """
        from django.db.models import Count
        
        return list(cls.objects.filter(user=user)
                   .values('category')
                   .annotate(count=Count('category'))
                   .order_by('-count')
                   .values_list('category', flat=True)[:limit])


# 📎 Médias associés à une entrée de journal
class JournalMedia(models.Model):
    """
    Modèle pour stocker les fichiers multimédias associés aux entrées de journal.
    Permet aux utilisateurs d'enrichir leurs entrées avec des images ou des enregistrements audio.
    
    API Endpoints suggérés:
    - POST /api/journal-entries/{id}/media/ - Ajouter un média à une entrée
    - DELETE /api/journal-entries/media/{id}/ - Supprimer un média
    - GET /api/journal-entries/{id}/media/ - Lister les médias d'une entrée
    
    Exemple de sérialisation JSON:
    {
        "id": 45,
        "entry": 123,
        "type": "image",
        "file": "/media/journal_media/image123.jpg",
        "created_at": "2025-04-19T15:31:12Z"
    }
    """
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="journal_media/")
    type = models.CharField(
        max_length=10,
        choices=[("image", "Image"), ("audio", "Audio")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ['created_at']
        
        """
        Permissions API:
        - Un utilisateur ne doit accéder qu'aux médias liés à ses propres entrées
        - Limiter la taille des uploads
        - Valider les types MIME des fichiers
        """

    def __str__(self):
        return f"{self.get_type_display()} pour {self.entry}"
        
    def file_url(self):
        """
        Retourne l'URL complète du fichier.
        
        Returns:
            str: URL du fichier média
            
        Utilisation dans l'API:
            Ce champ doit être inclus dans la sérialisation pour faciliter
            l'affichage direct dans l'interface.
            
        Exemple dans un sérialiseur:
            @property
            def file_url(self):
                return self.instance.file.url if self.instance.file else None
        """
        if self.file:
            return self.file.url
        return None
        
    def file_size(self):
        """
        Retourne la taille du fichier en octets.
        
        Returns:
            int: Taille du fichier en octets
            
        Utilisation dans l'API:
            Utile pour l'affichage dans l'interface ou pour les quotas.
        """
        if self.file:
            return self.file.size
        return 0
        
    def validate_file_type(self):
        """
        Vérifie si le type de fichier correspond au type déclaré.
        
        Raises:
            ValidationError: Si le type de fichier ne correspond pas
            
        Utilisation dans l'API:
            Cette validation doit être reproduite dans le sérialiseur
            pour assurer la cohérence des données.
        """
        import mimetypes
        if not self.file:
            return
            
        mime_type, _ = mimetypes.guess_type(self.file.name)
        
        if self.type == 'image' and not mime_type.startswith('image/'):
            raise ValidationError({'file': 'Le fichier doit être une image.'})
            
        if self.type == 'audio' and not mime_type.startswith('audio/'):
            raise ValidationError({'file': 'Le fichier doit être un audio.'})

from django.db import models
from django.utils.timezone import now
from django.conf import settings

User = settings.AUTH_USER_MODEL

# 🔔 Notification utilisateur
class Notification(models.Model):
    """
    Modèle représentant une notification pour un utilisateur.
    Permet d'informer l'utilisateur d'événements importants dans l'application.
    
    API Endpoints suggérés:
    - GET /api/notifications/ - Liste des notifications de l'utilisateur connecté
    - GET /api/notifications/unread/ - Liste des notifications non lues
    - POST /api/notifications/{id}/read/ - Marquer une notification comme lue
    - POST /api/notifications/read-all/ - Marquer toutes les notifications comme lues
    - POST /api/notifications/{id}/archive/ - Archiver une notification
    - GET /api/notifications/archived/ - Liste des notifications archivées
    - DELETE /api/notifications/{id}/ - Supprimer une notification
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "message": "🏅 Nouveau badge débloqué : Niveau 3 !",
        "notif_type": "badge",
        "type_display": "Badge débloqué",
        "is_read": false,
        "created_at": "2025-04-19T16:42:22Z",
        "archived": false
    }
    """

    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif'),
        ('statistique', 'Statistique'),
        ('info', 'Information'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()  # Contenu de la notification
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info')
    is_read = models.BooleanField(default=False)  # État de lecture
    read_at = models.DateTimeField(null=True, blank=True)  # Date de lecture
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)  # Champ pour archiver la notification
    scheduled_at = models.DateTimeField(null=True, blank=True)  # Pour les notifications programmées

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'archived']),
        ]
        
        """
        Filtres API recommandés:
        - is_read (boolean)
        - archived (boolean)
        - notif_type (exact, in)
        - created_at (date, range)
        
        Pagination:
        - Utiliser la pagination par défaut (généralement 10-20 par page)
        - Considérer une pagination par curseur pour les grandes quantités
        """

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
        
    @property
    def type_display(self):
        """
        Retourne la version lisible du type de notification.
        
        Returns:
            str: Label du type de notification
            
        Utilisation dans l'API:
            À inclure comme champ dans la sérialisation pour l'affichage
            dans l'interface utilisateur.
        """
        return dict(self.NOTIF_TYPES).get(self.notif_type, "Information")

    def archive(self):
        """
        Archive la notification (sans suppression).
        
        Utilisation dans l'API:
            Parfait pour un endpoint dédié avec une action personnalisée.
            
        Exemple dans une vue:
            @action(detail=True, methods=['post'])
            def archive(self, request, pk=None):
                notification = self.get_object()
                notification.archive()
                return Response(status=status.HTTP_204_NO_CONTENT)
        """
        if not self.archived:
            self.archived = True
            self.save(update_fields=['archived'])

    def mark_as_read(self):
        """
        Marque une seule notification comme lue si ce n'est pas déjà fait.
        Enregistre également la date de lecture.
        
        Utilisation dans l'API:
            Idéal pour un endpoint dédié qui marque une notification spécifique comme lue.
            
        Exemple dans une vue:
            @action(detail=True, methods=['post'])
            def mark_read(self, request, pk=None):
                notification = self.get_object()
                notification.mark_as_read()
                return Response(self.get_serializer(notification).data)
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues d'un utilisateur comme lues.

        Args:
            user (User): L'utilisateur concerné.

        Returns:
            int: Nombre de notifications marquées comme lues.
            
        Utilisation dans l'API:
            Parfait pour un endpoint qui permet de marquer toutes les notifications comme lues.
            
        Exemple dans une vue:
            @action(detail=False, methods=['post'])
            def mark_all_read(self, request):
                count = Notification.mark_all_as_read(request.user)
                return Response({'marked_read': count})
        """
        unread = cls.objects.filter(user=user, is_read=False)
        return unread.update(is_read=True, read_at=now())

    @classmethod
    def get_unread(cls, user):
        """
        Récupère toutes les notifications non lues et non archivées d'un utilisateur.

        Args:
            user: L'utilisateur dont on veut récupérer les notifications

        Returns:
            QuerySet: Ensemble des notifications non lues et non archivées
            
        Utilisation dans l'API:
            Utile pour afficher un compteur de notifications ou une liste des
            notifications non lues.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def unread(self, request):
                notifications = Notification.get_unread(request.user)
                page = self.paginate_queryset(notifications)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = self.get_serializer(notifications, many=True)
                return Response(serializer.data)
        """
        return cls.objects.filter(user=user, is_read=False, archived=False)

    @classmethod
    def get_inbox(cls, user):
        """
        Récupère toutes les notifications non archivées d'un utilisateur.

        Args:
            user: L'utilisateur dont on veut récupérer les notifications

        Returns:
            QuerySet: Ensemble des notifications non archivées
            
        Utilisation dans l'API:
            Cette méthode est idéale pour l'endpoint principal des notifications
            qui affiche la "boîte de réception" de l'utilisateur.
        """
        return cls.objects.filter(user=user, archived=False)

    @classmethod
    def get_archived(cls, user):
        """
        Récupère toutes les notifications archivées d'un utilisateur.

        Args:
            user: L'utilisateur dont on veut récupérer les notifications archivées

        Returns:
            QuerySet: Ensemble des notifications archivées
            
        Utilisation dans l'API:
            Parfait pour un endpoint qui affiche les notifications archivées,
            généralement accessible via un onglet "Archivées" dans l'interface.
        """
        return cls.objects.filter(user=user, archived=True)
        
    @classmethod
    def create_notification(cls, user, message, notif_type='info', scheduled_at=None):
        """
        Crée une nouvelle notification pour un utilisateur.
        
        Args:
            user (User): Destinataire de la notification
            message (str): Contenu de la notification
            notif_type (str): Type de notification (badge, objectif, etc.)
            scheduled_at (datetime, optional): Date programmée pour afficher la notification
            
        Returns:
            Notification: L'objet notification créé
            
        Utilisation dans l'API:
            Cette méthode facilite la création de notifications depuis les vues API.
            
        Exemple dans une vue:
            @action(detail=True, methods=['post'])
            def complete(self, request, pk=None):
                objective = self.get_object()
                # Logique de complétion...
                Notification.create_notification(
                    request.user,
                    f"🎯 Objectif atteint : {objective.title}",
                    notif_type="objectif"
                )
                return Response(...)
        """
        return cls.objects.create(
            user=user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )
        
    @classmethod
    def get_notification_count(cls, user):
        """
        Retourne un dictionnaire avec le nombre de notifications par état.
        
        Args:
            user (User): L'utilisateur concerné
            
        Returns:
            dict: Statistiques des notifications
                {
                    'unread': 5,   # Nombre de notifications non lues
                    'total': 42,   # Nombre total de notifications (non archivées)
                    'archived': 10  # Nombre de notifications archivées
                }
                
        Utilisation dans l'API:
            Parfait pour afficher des badges de compteur dans l'interface.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def counts(self, request):
                return Response(Notification.get_notification_count(request.user))
        """
        return {
            'unread': cls.objects.filter(user=user, is_read=False, archived=False).count(),
            'total': cls.objects.filter(user=user, archived=False).count(),
            'archived': cls.objects.filter(user=user, archived=True).count()
        }

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .notification_model import Notification

from django.conf import settings
User = settings.AUTH_USER_MODEL


# 🎯 Objectif utilisateur
class Objective(models.Model):
    """
    Modèle représentant un objectif défini par l'utilisateur.
    Permet de suivre les progrès vers des objectifs spécifiques.
    
    API Endpoints suggérés:
    - GET /api/objectives/ - Liste des objectifs de l'utilisateur
    - POST /api/objectives/ - Créer un nouvel objectif
    - GET /api/objectives/{id}/ - Détails d'un objectif spécifique
    - PUT/PATCH /api/objectives/{id}/ - Modifier un objectif existant
    - DELETE /api/objectives/{id}/ - Supprimer un objectif
    - POST /api/objectives/{id}/complete/ - Marquer un objectif comme complété
    - GET /api/objectives/stats/ - Statistiques sur les objectifs (par catégorie, par état)
    - GET /api/objectives/upcoming/ - Objectifs dont l'échéance approche
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "title": "Faire 5 séances de sport",
        "category": "Santé",
        "done": false,
        "target_date": "2025-04-25",
        "target_value": 5,
        "created_at": "2025-04-19T17:30:10Z",
        "progress": 60,
        "entries_done": 3,
        "days_remaining": 6,
        "is_overdue": false
    }
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="objectives")
    title = models.CharField(max_length=255)  # Titre de l'objectif
    category = models.CharField(max_length=100)  # Catégorie de l'objectif
    done = models.BooleanField(default=False)  # État de complétion
    target_date = models.DateField()  # Date cible pour atteindre l'objectif
    target_value = models.PositiveIntegerField(default=1, verbose_name="Objectif à atteindre", validators=[MinValueValidator(1)])  # Valeur à atteindre
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    class Meta:
        verbose_name = "Objectif"
        verbose_name_plural = "Objectifs"
        ordering = ['target_date', 'done']
        
        """
        Filtres API recommandés:
        - done (boolean)
        - category (exact, in)
        - target_date (gte, lte, range)
        - is_overdue (boolean calculé: target_date < today && !done)
        
        Permissions API:
        - Un utilisateur ne doit voir et modifier que ses propres objectifs
        """

    def __str__(self):
        """Représentation en chaîne de caractères de l'objectif avec indicateur d'achèvement"""
        return f"{self.title} ({'✅' if self.done else '🕓'})"

    def entries_done(self):
        """
        Compte le nombre d'entrées correspondant à la catégorie de cet objectif
        pour la date cible.

        Returns:
            int: Nombre d'entrées correspondant aux critères
            
        Utilisation dans l'API:
            Ce champ devrait être inclus comme champ calculé dans la sérialisation
            pour afficher la progression de l'utilisateur vers cet objectif.
        """
        return self.user.entries.filter(
            category=self.category,
            created_at__date=self.target_date
        ).count()

    def progress(self):
        """
        Calcule le pourcentage de progression vers l'objectif.

        Returns:
            int: Pourcentage de progression (0-100)
            
        Utilisation dans l'API:
            Idéal pour afficher une barre de progression dans l'interface.
            Inclure ce champ calculé dans la sérialisation.
            
        Exemple dans un sérialiseur:
            def get_progress(self, obj):
                return obj.progress()
        """
        if self.target_value > 0:
            return min(100, int((self.entries_done() / self.target_value) * 100))
        return 0

    def is_achieved(self):
        """
        Vérifie si l'objectif est atteint (marqué comme fait ou progression à 100%).

        Returns:
            bool: True si l'objectif est atteint, False sinon
            
        Utilisation dans l'API:
            Ce champ peut être utilisé comme champ calculé pour déterminer
            si un objectif devrait être automatiquement marqué comme complété.
        """
        return self.done or self.progress() >= 100
        
    def days_remaining(self):
        """
        Calcule le nombre de jours restants avant la date cible.
        
        Returns:
            int: Nombre de jours jusqu'à la date cible (négatif si dépassée)
            
        Utilisation dans l'API:
            Utile pour afficher le temps restant et pour trier les objectifs
            par urgence dans l'interface utilisateur.
        """
        return (self.target_date - now().date()).days
        
    def is_overdue(self):
        """
        Vérifie si l'objectif est en retard (date cible dépassée sans être complété).
        
        Returns:
            bool: True si l'objectif est en retard, False sinon
            
        Utilisation dans l'API:
            Ce champ calculé permet d'afficher des indicateurs visuels
            pour les objectifs en retard dans l'interface.
        """
        return not self.done and self.target_date < now().date()

    def save(self, *args, **kwargs):
        """
        Surcharge pour mettre à jour l'état 'done' automatiquement si l'objectif est atteint.
        Une notification est créée uniquement si l'objectif vient d'être complété.
        
        Utilisation dans l'API:
            La logique de notification est automatiquement gérée lors de la sauvegarde,
            mais le paramètre create_notification peut être utilisé pour désactiver ce comportement.
            
        Exemple dans une vue API:
            @action(detail=True, methods=['post'])
            def complete(self, request, pk=None):
                objective = self.get_object()
                objective.done = True
                objective.save()  # Notification créée automatiquement
                return Response(self.get_serializer(objective).data)
        """
        was_not_done = self.pk is not None and not self.done
        is_achievement = not self.done and self.is_achieved()
        
        if is_achievement:
            self.done = True

            # Crée une notification si ce n'est pas désactivé explicitement
            create_notification = kwargs.pop('create_notification', True)
            if create_notification:
                Notification.objects.create(
                    user=self.user,
                    message=f"🎯 Objectif atteint : {self.title}",
                    notif_type="objectif"
                )

        super().save(*args, **kwargs)
        
    @classmethod
    def get_upcoming(cls, user, days=7):
        """
        Récupère les objectifs dont l'échéance approche dans les prochains jours.
        
        Args:
            user (User): L'utilisateur concerné
            days (int): Nombre de jours à anticiper
            
        Returns:
            QuerySet: Objectifs à échéance dans la période spécifiée
            
        Utilisation dans l'API:
            Parfait pour un endpoint qui affiche les objectifs urgents
            ou pour envoyer des rappels.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def upcoming(self, request):
                days = int(request.query_params.get('days', 7))
                objectives = Objective.get_upcoming(request.user, days)
                return Response(self.get_serializer(objectives, many=True).data)
        """
        today = now().date()
        deadline = today + timedelta(days=days)
        
        return cls.objects.filter(
            user=user,
            done=False,
            target_date__gte=today,
            target_date__lte=deadline
        ).order_by('target_date')
        
    @classmethod
    def get_statistics(cls, user):
        """
        Calcule des statistiques sur les objectifs de l'utilisateur.
        
        Args:
            user (User): L'utilisateur concerné
            
        Returns:
            dict: Statistiques calculées sur les objectifs
                {
                    'total': 42,
                    'completed': 28,
                    'completion_rate': 66.7,
                    'overdue': 5,
                    'by_category': {
                        'Santé': {'total': 15, 'completed': 10},
                        'Travail': {'total': 12, 'completed': 8},
                        ...
                    }
                }
                
        Utilisation dans l'API:
            Idéal pour un dashboard ou un endpoint de statistiques.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def statistics(self, request):
                return Response(Objective.get_statistics(request.user))
        """
        from django.db.models import Count, Case, When, IntegerField
        
        # Statistiques globales
        objectives = cls.objects.filter(user=user)
        total = objectives.count()
        completed = objectives.filter(done=True).count()
        
        # Statistiques par catégorie
        by_category = objectives.values('category').annotate(
            total=Count('id'),
            completed=Count(Case(When(done=True, then=1), output_field=IntegerField()))
        ).order_by('-total')
        
        # Objectifs en retard
        overdue = objectives.filter(
            done=False,
            target_date__lt=now().date()
        ).count()
        
        # Calcul du taux de complétion
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'completed': completed,
            'completion_rate': round(completion_rate, 1),
            'overdue': overdue,
            'by_category': {
                item['category']: {'total': item['total'], 'completed': item['completed']} 
                for item in by_category
            }
        }

from django.db import models


class Quote(models.Model):
    """
    Modèle pour stocker des citations inspirantes ou motivantes.
    Ces citations peuvent être affichées aux utilisateurs en fonction de leur humeur
    ou à des moments stratégiques dans l'application.
    
    API Endpoints suggérés:
    - GET /api/quotes/ - Liste de toutes les citations
    - GET /api/quotes/random/ - Retourne une citation aléatoire
    - GET /api/quotes/random/?mood_tag=positive - Citation aléatoire filtrée par étiquette
    - GET /api/quotes/daily/ - Citation du jour
    - GET /api/quotes/authors/ - Liste des auteurs disponibles
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "text": "La vie est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.",
        "author": "Albert Einstein",
        "mood_tag": "positive",
        "length": 75  // Champ calculé optionnel
    }
    """

    # Le texte de la citation
    text = models.TextField()

    # L'auteur de la citation (optionnel)
    author = models.CharField(max_length=255, blank=True)

    # Étiquette d'humeur associée pour le ciblage contextuel
    mood_tag = models.CharField(
        max_length=50,
        blank=True,
        help_text="Étiquette d'humeur associée (ex: 'positive', 'low', 'neutral')"
    )

    class Meta:
        verbose_name = "Citation"
        verbose_name_plural = "Citations"
        ordering = ['author']
        
        """
        Filtres API recommandés:
        - author (exact, contains)
        - mood_tag (exact, in)
        - text (contains)
        - length (calculé, pour filtrer par taille)
        """
        
        indexes = [
            models.Index(fields=['mood_tag']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        """
        Représentation textuelle de la citation.
        
        Returns:
            str: Citation avec son auteur si disponible
        """
        if self.author:
            return f'"{self.text}" — {self.author}'
        return f'"{self.text}"'
    
    def length(self):
        """
        Retourne la longueur du texte de la citation.
        
        Returns:
            int: Nombre de caractères dans la citation
            
        Utilisation dans l'API:
            Peut être utilisé comme champ calculé pour filtrer les citations
            par longueur (courtes pour notifications, longues pour affichage principal).
        """
        return len(self.text)
    
    @classmethod
    def get_random(cls, mood_tag=None):
        """
        Retourne une citation aléatoire, optionnellement filtrée par mood_tag.
        
        Args:
            mood_tag (str, optional): Étiquette d'humeur pour filtrer les citations
            
        Returns:
            Quote: Une citation aléatoire ou None si aucune ne correspond
            
        Utilisation dans l'API:
            Parfait pour un endpoint qui affiche une citation aléatoire
            dans le dashboard ou les notifications.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def random(self, request):
                mood_tag = request.query_params.get('mood_tag')
                quote = Quote.get_random(mood_tag)
                if not quote:
                    return Response(
                        {"detail": "Aucune citation trouvée."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                return Response(self.get_serializer(quote).data)
        """
        import random
        
        queryset = cls.objects.all()
        if mood_tag:
            queryset = queryset.filter(mood_tag=mood_tag)
            
        count = queryset.count()
        if count == 0:
            return None
            
        random_index = random.randint(0, count - 1)
        return queryset[random_index]
    
    @classmethod
    def get_daily_quote(cls, user=None):
        """
        Retourne la citation du jour, potentiellement personnalisée selon l'utilisateur.
        
        Args:
            user (User, optional): Utilisateur pour personnalisation basée sur son humeur
            
        Returns:
            Quote: Citation du jour
            
        Utilisation dans l'API:
            Idéal pour un widget de citation du jour sur le dashboard.
            
        Note technique:
            Cette méthode assure que tous les utilisateurs voient la même citation le même jour,
            à moins qu'un filtre d'humeur spécifique ne soit appliqué selon leur profil.
        """
        import datetime
        import hashlib
        
        # Date du jour comme seed pour la sélection
        today = datetime.date.today().strftime("%Y%m%d")
        
        # Si un utilisateur est fourni, on peut personnaliser selon son humeur récente
        mood_filter = None
        if user:
            from django.db.models import Avg
            # Calcul de l'humeur moyenne sur les 3 derniers jours
            recent_entries = user.entries.filter(
                created_at__gte=datetime.datetime.now() - datetime.timedelta(days=3)
            )
            if recent_entries.exists():
                avg_mood = recent_entries.aggregate(avg=Avg('mood'))['avg']
                # Définition du filtre selon l'humeur
                if avg_mood is not None:
                    if avg_mood < 4:
                        mood_filter = 'low'
                    elif avg_mood > 7:
                        mood_filter = 'positive'
                    else:
                        mood_filter = 'neutral'
        
        # Récupération des citations correspondant au filtre d'humeur
        quotes = cls.objects.all()
        if mood_filter:
            filtered_quotes = quotes.filter(mood_tag=mood_filter)
            # Si aucune citation ne correspond, on revient à toutes les citations
            if filtered_quotes.exists():
                quotes = filtered_quotes
                
        count = quotes.count()
        if count == 0:
            return None
            
        # Utiliser le hashage pour assurer la même sélection pour tous les utilisateurs le même jour
        hash_obj = hashlib.md5(today.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # Sélection déterministe basée sur la date
        index = hash_int % count
        return quotes[index]
    
    @classmethod
    def get_authors_list(cls):
        """
        Retourne la liste des auteurs disponibles avec leur nombre de citations.
        
        Returns:
            list: Liste de dictionnaires {author, count}
            
        Utilisation dans l'API:
            Utile pour construire un filtre ou un menu déroulant des auteurs.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def authors(self, request):
                return Response(Quote.get_authors_list())
        """
        from django.db.models import Count
        
        authors = cls.objects.exclude(author='').values('author').annotate(
            count=Count('id')
        ).order_by('author')
        
        return list(authors)

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from collections import defaultdict
from django.db.models import Avg

from django.conf import settings
User = settings.AUTH_USER_MODEL


class WeeklyStat(models.Model):
    """
    Modèle pour stocker les statistiques hebdomadaires d'un utilisateur.
    Agrège les données d'entrées pour fournir des insights sur une période d'une semaine.
    Permet de suivre les tendances et l'évolution sur une échelle de temps plus large que les stats quotidiennes.
    
    API Endpoints suggérés:
    - GET /api/stats/weekly/ - Liste des statistiques hebdomadaires de l'utilisateur
    - GET /api/stats/weekly/current/ - Statistiques de la semaine en cours
    - GET /api/stats/weekly/{date}/ - Statistiques de la semaine contenant la date spécifiée
    - GET /api/stats/weekly/trends/ - Évolution des statistiques sur plusieurs semaines
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "week_start": "2025-04-14",
        "week_end": "2025-04-20",  // Champ calculé
        "entries_count": 12,
        "mood_average": 7.5,
        "categories": {
            "Travail": 5,
            "Sport": 3,
            "Famille": 4
        },
        "top_category": "Travail",  // Champ calculé
        "week_number": 16           // Champ calculé
    }
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_stats")
    week_start = models.DateField()  # Premier jour de la semaine (lundi)
    entries_count = models.PositiveIntegerField()  # Nombre total d'entrées
    mood_average = models.FloatField(null=True, blank=True)  # Moyenne d'humeur
    categories = models.JSONField(default=dict, blank=True)  # Répartition par catégorie

    class Meta:
        unique_together = ('user', 'week_start')
        ordering = ['-week_start']
        verbose_name = "Statistique hebdomadaire"
        verbose_name_plural = "Statistiques hebdomadaires"
        
        """
        Filtres API recommandés:
        - week_start (date, gte, lte)
        - entries_count (gte, lte)
        - mood_average (gte, lte)
        """

    def __str__(self):
        return f"{self.user.username} - semaine du {self.week_start}"
        
    def week_end(self):
        """
        Calcule le dernier jour de la semaine.
        
        Returns:
            date: Date du dimanche de cette semaine
            
        Utilisation dans l'API:
            Utile comme champ calculé pour l'affichage de la période complète.
        """
        return self.week_start + timedelta(days=6)
        
    def week_number(self):
        """
        Retourne le numéro de semaine dans l'année.
        
        Returns:
            int: Numéro de la semaine (1-53)
            
        Utilisation dans l'API:
            Pratique pour l'affichage et le regroupement des données par semaine.
        """
        return self.week_start.isocalendar()[1]
        
    def top_category(self):
        """
        Détermine la catégorie la plus fréquente de la semaine.
        
        Returns:
            str: Nom de la catégorie la plus fréquente, ou None si aucune entrée
            
        Utilisation dans l'API:
            Utile pour l'affichage de résumés ou de badges dans l'interface.
        """
        if not self.categories:
            return None
            
        return max(self.categories.items(), key=lambda x: x[1])[0]

    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Génère ou met à jour les statistiques hebdomadaires pour un utilisateur.

        Args:
            user: L'utilisateur concerné
            reference_date: Date de référence (par défaut aujourd'hui)

        Returns:
            (obj, created): Statistique mise à jour ou créée
            
        Utilisation dans l'API:
            Cette méthode devrait être appelée en arrière-plan après chaque
            ajout/modification/suppression d'entrée, ou via une tâche périodique.
            
        Exemple d'utilisation dans une vue:
            @action(detail=False, methods=['post'])
            def refresh(self, request):
                date_param = request.data.get('date')
                date = parse_date(date_param) if date_param else None
                stat, created = WeeklyStat.generate_for_user(request.user, date)
                return Response(self.get_serializer(stat).data)
        """
        if not reference_date:
            reference_date = now().date()

        week_start = reference_date - timedelta(days=reference_date.weekday())
        week_end = week_start + timedelta(days=6)

        entries = user.entries.filter(created_at__date__range=(week_start, week_end))
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1

        return cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        
    @classmethod
    def get_trends(cls, user, weeks=10):
        """
        Récupère l'évolution des statistiques sur plusieurs semaines.
        
        Args:
            user: L'utilisateur concerné
            weeks: Nombre de semaines à inclure
            
        Returns:
            dict: Données de tendances structurées pour visualisation
                {
                    'weeks': ['2025-W15', '2025-W16', ...],
                    'entries': [8, 12, ...],
                    'mood': [6.5, 7.2, ...]
                }
                
        Utilisation dans l'API:
            Parfait pour générer des graphiques d'évolution.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def trends(self, request):
                weeks = int(request.query_params.get('weeks', 10))
                return Response(WeeklyStat.get_trends(request.user, weeks))
        """
        # Calculer le début de la période
        current_week_start = now().date() - timedelta(days=now().date().weekday())
        start_date = current_week_start - timedelta(weeks=weeks)
        
        # Récupérer les statistiques hebdomadaires existantes
        stats = cls.objects.filter(
            user=user,
            week_start__gte=start_date
        ).order_by('week_start')
        
        # Préparer les données de tendances
        weeks_labels = []
        entries_data = []
        mood_data = []
        
        # Remplir les semaines manquantes
        for i in range(weeks + 1):
            week_date = start_date + timedelta(weeks=i)
            week_label = f"{week_date.year}-W{week_date.isocalendar()[1]}"
            weeks_labels.append(week_label)
            
            # Chercher la stat correspondante
            stat = next((s for s in stats if s.week_start == week_date), None)
            
            entries_data.append(stat.entries_count if stat else 0)
            mood_data.append(stat.mood_average if stat and stat.mood_average else None)
        
        return {
            'weeks': weeks_labels,
            'entries': entries_data,
            'mood': mood_data
        }


class DailyStat(models.Model):
    """
    Modèle pour stocker les statistiques journalières d'un utilisateur.
    Agrège les données d'entrées de journal pour une analyse et un affichage efficaces.
    
    API Endpoints suggérés:
    - GET /api/stats/daily/ - Liste des statistiques journalières de l'utilisateur
    - GET /api/stats/daily/today/ - Statistiques du jour
    - GET /api/stats/daily/{date}/ - Statistiques d'une date spécifique
    - GET /api/stats/daily/range/?start={date}&end={date} - Statistiques sur une période
    - GET /api/stats/daily/calendar/ - Données pour la vue calendrier (heatmap)
    
    Exemple de sérialisation JSON:
    {
        "id": 123,
        "date": "2025-04-19",
        "entries_count": 3,
        "mood_average": 8.0,
        "categories": {
            "Travail": 1,
            "Sport": 1,
            "Loisirs": 1
        },
        "day_of_week": "Samedi",  // Champ calculé
        "is_weekend": true        // Champ calculé
    }
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_stats")
    date = models.DateField()
    entries_count = models.PositiveIntegerField(default=0)
    mood_average = models.FloatField(null=True, blank=True)
    categories = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
        verbose_name = "Statistique journalière"
        verbose_name_plural = "Statistiques journalières"
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
        
        """
        Filtres API recommandés:
        - date (exact, gte, lte, range)
        - entries_count (gte, lte)
        - mood_average (gte, lte)
        - is_weekend (boolean calculé)
        """

    def __str__(self):
        return f"{self.user.username} - {self.date}"
        
    def day_of_week(self):
        """
        Retourne le jour de la semaine en format lisible.
        
        Returns:
            str: Nom du jour de la semaine (Lundi, Mardi, etc.)
            
        Utilisation dans l'API:
            Utile pour l'affichage dans l'interface utilisateur.
        """
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return days[self.date.weekday()]
        
    def is_weekend(self):
        """
        Vérifie si la date tombe un weekend.
        
        Returns:
            bool: True si samedi ou dimanche
            
        Utilisation dans l'API:
            Permet de filtrer ou d'afficher différemment les weekends.
        """
        return self.date.weekday() >= 5  # 5=Samedi, 6=Dimanche

    @classmethod
    def generate_for_user(cls, user, date=None):
        """
        Génère ou met à jour les statistiques journalières pour une date donnée.

        Args:
            user: L'utilisateur concerné
            date: Date à analyser (par défaut aujourd'hui)

        Returns:
            DailyStat: Statistique mise à jour ou créée
            
        Utilisation dans l'API:
            Cette méthode devrait être appelée automatiquement via un signal
            après chaque ajout/modification/suppression d'entrée de journal.
            
        Exemple dans une vue:
            @action(detail=False, methods=['post'])
            def refresh_today(self, request):
                stat = DailyStat.generate_for_user(request.user)
                return Response(self.get_serializer(stat).data)
        """
        if not date:
            date = now().date()

        entries = user.entries.filter(created_at__date=date)
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        cat_stats = defaultdict(int)
        for entry in entries:
            cat_stats[entry.category] += 1

        obj, created = cls.objects.update_or_create(
            user=user,
            date=date,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(cat_stats),
            }
        )

        return obj
        
    @classmethod
    def get_calendar_data(cls, user, month=None, year=None):
        """
        Génère des données pour une visualisation de type calendrier heatmap.
        
        Args:
            user: L'utilisateur concerné
            month: Mois (1-12, None=tous les mois)
            year: Année (None=année en cours)
            
        Returns:
            list: Liste de dictionnaires pour chaque jour avec données
                [
                    {
                        "date": "2025-04-01",
                        "count": 2,
                        "mood": 7.5,
                        "intensity": 0.4  // Valeur normalisée pour la heatmap
                    },
                    ...
                ]
                
        Utilisation dans l'API:
            Idéal pour générer des visualisations de type "GitHub contributions"
            montrant l'activité quotidienne sur un calendrier.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def calendar(self, request):
                month = request.query_params.get('month')
                year = request.query_params.get('year')
                if month:
                    month = int(month)
                if year:
                    year = int(year)
                return Response(DailyStat.get_calendar_data(
                    request.user, month, year
                ))
        """
        import calendar
        from datetime import datetime
        
        # Paramètres par défaut
        if year is None:
            year = now().year
        
        # Construire le filtre de date
        date_filter = {'user': user, 'date__year': year}
        if month is not None:
            date_filter['date__month'] = month
        
        # Récupérer les statistiques
        stats = cls.objects.filter(**date_filter).order_by('date')
        
        # Déterminer les valeurs max pour normalisation
        max_count = max([stat.entries_count for stat in stats], default=1)
        
        # Générer les données pour chaque jour
        result = []
        for stat in stats:
            # Calculer une intensité normalisée pour la heatmap (0-1)
            intensity = stat.entries_count / max_count if max_count > 0 else 0
            
            result.append({
                'date': stat.date.isoformat(),
                'count': stat.entries_count,
                'mood': stat.mood_average,
                'intensity': round(intensity, 2)
            })
            
        return result

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from collections import defaultdict
from django.conf import settings
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

# Services métiers externalisés (bonne pratique)
from ..services.badge_service import update_user_badges
from ..services.preferences_service import create_preferences_for_user
from ..services.streak_service import update_user_streak
from ..services.user_stats_service import (
    mood_average as compute_mood_average,
    current_streak as compute_current_streak,
    has_entries_every_day as compute_entries_every_day,
    entries_by_category as compute_entries_by_category,
    entries_last_n_days as compute_entries_last_n_days,
    entries_per_day as compute_entries_per_day,
    mood_trend as compute_mood_trend,
    days_with_entries as compute_days_with_entries,
    entries_per_category_last_n_days as compute_entries_per_category_last_n_days,
)

# 👤 Utilisateur personnalisé
class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé héritant de AbstractUser de Django.
    Étend le modèle utilisateur standard avec des fonctionnalités supplémentaires
    pour l'application de suivi personnel.
    
    API Endpoints suggérés:
    - GET /api/users/me/ - Profil de l'utilisateur connecté
    - PUT/PATCH /api/users/me/ - Mise à jour du profil
    - GET /api/users/me/stats/ - Statistiques personnelles
    - GET /api/users/me/streaks/ - Information sur les séries de jours consécutifs
    - GET /api/users/me/dashboard/ - Données consolidées pour le tableau de bord
    - POST /api/auth/register/ - Création d'un nouvel utilisateur
    - POST /api/auth/login/ - Authentification par email/mot de passe
    - POST /api/auth/refresh/ - Rafraîchissement du token JWT
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-03-15T10:30:00Z",
        "stats": {
            "total_entries": 125,
            "current_streak": 8,
            "longest_streak": 15,
            "mood_average": 7.5,
            "level": 3
        }
    }
    """
    email = models.EmailField(unique=True)  # Assure que chaque email est unique
    longest_streak = models.PositiveIntegerField(default=0, editable=False)  # Plus longue série de jours consécutifs

    # 🔐 Utilisation de l'email comme identifiant principal
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username reste requis mais pas utilisé pour l'authentification

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']
        
        """
        Permissions API:
        - Un utilisateur ne peut accéder qu'à ses propres données
        - Seuls les admins peuvent accéder à la liste complète des utilisateurs
        - Les emails et autres informations sensibles ne doivent pas être exposés publiquement
        """

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Retourne le nom complet de l'utilisateur.
        
        Returns:
            str: Nom complet (prénom + nom)
            
        Utilisation dans l'API:
            À inclure comme champ dans la sérialisation du profil utilisateur.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Retourne le prénom ou le username si le prénom est vide.
        
        Returns:
            str: Prénom ou nom d'utilisateur
            
        Utilisation dans l'API:
            Utile pour les affichages compacts ou les notifications.
        """
        return self.first_name or self.username

    def to_dict(self):
        """
        Représentation de l'utilisateur sous forme de dictionnaire (utile pour les API).
        
        Returns:
            dict: Données utilisateur formatées
            
        Utilisation dans l'API:
            Cette méthode peut servir de base pour la sérialisation,
            mais préférez utiliser les sérialiseurs DRF pour plus de flexibilité.
            
        Note:
            Pour les API REST avec Django REST Framework, utilisez plutôt
            un sérialiseur dédié qui étend cette logique et gère les permissions.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.get_full_name(),
            "entries": self.total_entries(),
            "current_streak": self.current_streak(),
            "mood_average": self.mood_average(),
        }

    def total_entries(self):
        """
        Retourne le nombre total d'entrées de journal de l'utilisateur.
        
        Returns:
            int: Nombre total d'entrées
            
        Utilisation dans l'API:
            Ce champ devrait être inclus dans les statistiques utilisateur
            et dans le résumé du profil.
        """
        return self.entries.count()

    def mood_average(self, days=7, reference_date=None):
        """
        Calcule la moyenne d'humeur sur les X derniers jours.
        Délégué à user_stats_service.
        
        Args:
            days (int): Nombre de jours à considérer
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            float: Moyenne d'humeur arrondie à 1 décimale, ou None si aucune entrée
            
        Utilisation dans l'API:
            Idéal pour les endpoints de statistiques et le dashboard.
            Permet de filtrer par période en ajoutant un paramètre ?days=N.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def mood_stats(self, request):
                days = int(request.query_params.get('days', 7))
                return Response({
                    'average': request.user.mood_average(days)
                })
        """
        return compute_mood_average(self, days, reference_date)

    def current_streak(self, reference_date=None):
        """
        Calcule la série actuelle de jours consécutifs avec au moins une entrée.
        Utilise le service user_stats.
        
        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre de jours consécutifs avec entrées
            
        Utilisation dans l'API:
            Cette métrique est essentielle pour l'engagement utilisateur
            et devrait être mise en avant dans le dashboard.
        """
        return compute_current_streak(self, reference_date)

    def has_entries_every_day(self, last_n_days=7, reference_date=None):
        """
        Vérifie si l'utilisateur a écrit au moins une entrée chaque jour 
        sur une période donnée.
        
        Args:
            last_n_days (int): Nombre de jours à vérifier
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            bool: True si l'utilisateur a une entrée pour chaque jour de la période
            
        Utilisation dans l'API:
            Utile pour vérifier l'admissibilité à certains badges
            ou pour des indicateurs de régularité.
        """
        return compute_entries_every_day(self, last_n_days, reference_date)

    def all_objectives_achieved(self):
        """
        Vérifie si tous les objectifs de l'utilisateur sont cochés comme 'done'.
        
        Returns:
            bool: True si tous les objectifs sont achevés, False sinon
            
        Utilisation dans l'API:
            Peut être utilisé pour afficher une bannière de félicitations
            ou débloquer un badge spécial.
            
        Exemple dans un sérialiseur de profil:
            @property
            def all_objectives_complete(self):
                return self.instance.all_objectives_achieved()
        """
        return not self.objectives.filter(done=False).exists()

    def entries_today(self, reference_date=None):
        """
        Retourne le nombre d'entrées faites aujourd'hui.
        
        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre d'entrées d'aujourd'hui
            
        Utilisation dans l'API:
            Parfait pour les widgets de résumé quotidien dans l'interface.
        """
        if reference_date is None:
            reference_date = now().date()
        return self.entries.filter(created_at__date=reference_date).count()

    def entries_by_category(self, days=None):
        """
        Renvoie une répartition des entrées par catégorie.
        Délégué à user_stats_service.
        
        Args:
            days (int, optional): Limite aux N derniers jours si spécifié
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
            
        Utilisation dans l'API:
            Idéal pour générer des graphiques de répartition (camembert, barres).
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def category_breakdown(self, request):
                days = request.query_params.get('days')
                days = int(days) if days else None
                return Response(request.user.entries_by_category(days))
        """
        return compute_entries_by_category(self, days)

    def entries_last_n_days(self, n=7):
        """
        Retourne les entrées des N derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            QuerySet: Entrées des n derniers jours
            
        Utilisation dans l'API:
            Cette méthode devrait être utilisée dans une vue qui liste
            les entrées récentes de l'utilisateur.
            
        Note:
            Pour l'API, considérez d'ajouter de la pagination à cette méthode
            car elle peut retourner un grand nombre d'entrées.
        """
        return compute_entries_last_n_days(self, n)

    def entries_per_day(self, n=7):
        """
        Calcule le nombre d'entrées par jour pour les N derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec dates comme clés et nombre d'entrées comme valeurs
            
        Utilisation dans l'API:
            Parfait pour générer des graphiques d'activité journalière.
        """
        return compute_entries_per_day(self, n)

    def mood_trend(self, n=7):
        """
        Renvoie l'évolution moyenne de l'humeur par jour sur les N derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec dates comme clés et moyennes d'humeur comme valeurs
            
        Utilisation dans l'API:
            Idéal pour les graphiques linéaires montrant l'évolution de l'humeur.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def mood_evolution(self, request):
                days = int(request.query_params.get('days', 7))
                return Response(request.user.mood_trend(days))
        """
        return compute_mood_trend(self, n)

    def days_with_entries(self, n=30):
        """
        Liste des jours ayant au moins une entrée sur les N derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            list: Liste des dates avec au moins une entrée
            
        Utilisation dans l'API:
            Parfait pour générer des visualisations de type calendrier
            ou des heatmaps d'activité.
        """
        return compute_days_with_entries(self, n)

    def entries_per_category_last_n_days(self, n=7):
        """
        Répartition des entrées par catégorie sur les N derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
            
        Utilisation dans l'API:
            Utile pour des comparaisons de répartition sur une période spécifique.
        """
        return compute_entries_per_category_last_n_days(self, n)

    def update_badges(self):
        """
        Met à jour les badges débloqués pour l'utilisateur.
        Logique déportée dans badge_service.
        
        Utilisation dans l'API:
            Cette méthode devrait être appelée après certaines actions utilisateur
            (nouvelle entrée, objectif atteint, etc.) via un signal ou dans la vue.
            
        Exemple dans une vue d'ajout d'entrée:
            def perform_create(self, serializer):
                entry = serializer.save(user=self.request.user)
                self.request.user.update_badges()
                return entry
        """
        update_user_badges(self)

    def update_streaks(self):
        """
        Met à jour la plus longue série d'entrées consécutives si nécessaire.
        Utilise streak_service.
        
        Utilisation dans l'API:
            À appeler après chaque ajout ou suppression d'entrée,
            idéalement via un signal pour maintenir la cohérence des données.
        """
        update_user_streak(self)

    def create_default_preferences(self):
        """
        Crée les préférences utilisateur par défaut si elles n'existent pas.
        Appelle preferences_service.
        
        Returns:
            UserPreference: L'objet de préférences (créé ou existant)
            
        Utilisation dans l'API:
            Cette méthode devrait être appelée dans le signal post_save
            du modèle User pour garantir que chaque utilisateur a des préférences.
            
        Note technique:
            Dans Django REST Framework, c'est une bonne pratique d'inclure
            cette logique dans un signal plutôt que dans les vues.
        """
        return create_preferences_for_user(self)
        
    @property
    def level(self):
        """
        Calcule le niveau actuel de l'utilisateur basé sur le nombre d'entrées.
        
        Returns:
            int: Niveau utilisateur (1-N)
            
        Utilisation dans l'API:
            Ce champ calculé devrait être inclus dans le profil utilisateur
            et potentiellement dans les en-têtes ou la navigation.
            
        Exemple dans un sérialiseur:
            class UserProfileSerializer(serializers.ModelSerializer):
                level = serializers.ReadOnlyField()
                
                class Meta:
                    model = User
                    fields = ['username', 'email', 'level', ...]
        """
        # Niveau basé sur le nombre d'entrées
        entries = self.total_entries()
        
        # Seuils pour chaque niveau
        thresholds = [0, 5, 10, 20, 35, 50, 75, 100, 150, 200, 300, 500]
        
        # Déterminer le niveau
        for level, min_entries in enumerate(thresholds):
            if entries < min_entries:
                return max(1, level)  # Minimum niveau 1
                
        # Si au-delà du dernier seuil
        return len(thresholds)
        
    def get_dashboard_data(self):
        """
        Rassemble les données principales pour le tableau de bord utilisateur.
        
        Returns:
            dict: Données consolidées pour le dashboard
                {
                    "total_entries": 125,
                    "current_streak": 8,
                    "longest_streak": 15,
                    "mood_average": 7.5,
                    "level": 3,
                    "today_entries": 2,
                    "objectives": {
                        "total": 10,
                        "completed": 6,
                        "pending": 4
                    },
                    "badges": {
                        "unlocked": 8,
                        "total": 15,
                        "recent": [...]
                    },
                    "mood_trend": {...},
                    "categories": {...}
                }
                
        Utilisation dans l'API:
            Idéal pour un endpoint unique qui alimente le tableau de bord principal.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def dashboard(self, request):
                return Response(request.user.get_dashboard_data())
        """
        # Statistiques de base
        total_entries = self.total_entries()
        current_streak = self.current_streak()
        
        # Objectifs
        objectives = self.objectives.all()
        total_objectives = objectives.count()
        completed_objectives = objectives.filter(done=True).count()
        
        # Badges récemment débloqués (3 derniers)
        recent_badges = self.badges.order_by('-date_obtenue')[:3].values(
            'name', 'description', 'icon', 'date_obtenue'
        )
        
        # Données consolidées
        return {
            "total_entries": total_entries,
            "current_streak": current_streak,
            "longest_streak": self.longest_streak,
            "mood_average": self.mood_average(7),
            "level": self.level,
            "today_entries": self.entries_today(),
            "objectives": {
                "total": total_objectives,
                "completed": completed_objectives,
                "pending": total_objectives - completed_objectives
            },
            "badges": {
                "unlocked": self.badges.count(),
                "total": 15,  # Idéalement calculé dynamiquement
                "recent": list(recent_badges)
            },
            "mood_trend": self.mood_trend(7),
            "categories": self.entries_by_category(7)
        }

from datetime import timedelta
from django.db import models
from django.utils.timezone import now

from django.conf import settings
User = settings.AUTH_USER_MODEL


class UserPreference(models.Model):
    """
    Modèle pour stocker les préférences personnalisées de chaque utilisateur.
    Permet de contrôler les notifications et l'apparence de l'application.
    Chaque utilisateur a exactement une instance de ce modèle (relation one-to-one).
    
    API Endpoints suggérés:
    - GET /api/preferences/ - Récupérer les préférences de l'utilisateur courant
    - PUT/PATCH /api/preferences/ - Mettre à jour les préférences
    - POST /api/preferences/reset/ - Réinitialiser les préférences aux valeurs par défaut
    - GET /api/preferences/appearance/ - Récupérer uniquement les paramètres d'apparence
    - GET /api/preferences/notifications/ - Récupérer uniquement les paramètres de notification
    
    Exemple de sérialisation JSON:
    {
        "appearance": {
            "dark_mode": false,
            "accent_color": "#6C63FF",
            "font_choice": "Roboto",
            "enable_animations": true
        },
        "notifications": {
            "badge": true,
            "objectif": true,
            "info": true,
            "statistique": true
        }
    }
    """

    # Relation one-to-one avec l'utilisateur (un utilisateur a exactement une préférence)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")

    # Préférences de notifications par type
    notif_badge = models.BooleanField(default=True)        # Notifications pour les badges débloqués
    notif_objectif = models.BooleanField(default=True)     # Notifications liées aux objectifs
    notif_info = models.BooleanField(default=True)         # Notifications informatives générales
    notif_statistique = models.BooleanField(default=True)  # Notifications de statistiques

    # Préférences d'apparence
    dark_mode = models.BooleanField(default=False)                    # Mode sombre activé ou désactivé
    accent_color = models.CharField(max_length=20, default="#6C63FF")  # Couleur principale pour personnaliser l'interface
    font_choice = models.CharField(max_length=50, default="Roboto")     # Police de caractères préférée
    enable_animations = models.BooleanField(default=True)              # Option pour activer/désactiver les animations

    class Meta:
        verbose_name = "Préférence utilisateur"
        verbose_name_plural = "Préférences utilisateur"
        ordering = ["user"]
        
        """
        Permissions API:
        - Un utilisateur ne peut accéder et modifier que ses propres préférences
        - Adapter les préférences lors des requêtes en fonction de l'utilisateur authentifié
        """

    def __str__(self):
        """
        Représentation textuelle de l'objet de préférences.
        
        Returns:
            str: Chaîne indiquant à quel utilisateur appartiennent ces préférences
        """
        return f"Préférences de {self.user.username}"

    def to_dict(self):
        """
        Renvoie les préférences sous forme de dictionnaire.
        Pratique pour l'affichage ou l'utilisation dans une API.
        
        Returns:
            dict: Préférences utilisateur structurées
            
        Utilisation dans l'API:
            Cette méthode peut servir de base pour la sérialisation,
            mais privilégiez les sérialiseurs DRF pour plus de contrôle.
            
        Exemple dans un sérialiseur:
            class UserPreferenceSerializer(serializers.ModelSerializer):
                class Meta:
                    model = UserPreference
                    exclude = ['user']  # L'utilisateur est implicite
        """
        return {
            "dark_mode": self.dark_mode,
            "accent_color": self.accent_color,
            "font_choice": self.font_choice,
            "enable_animations": self.enable_animations,
            "notifications": {
                "badge": self.notif_badge,
                "objectif": self.notif_objectif,
                "info": self.notif_info,
                "statistique": self.notif_statistique,
            }
        }
        
    def get_appearance_settings(self):
        """
        Récupère uniquement les paramètres d'apparence.
        
        Returns:
            dict: Paramètres d'apparence de l'interface
            
        Utilisation dans l'API:
            Utile pour un endpoint dédié à l'apparence ou pour
            la récupération rapide des préférences visuelles au chargement.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def appearance(self, request):
                prefs = request.user.preferences
                return Response(prefs.get_appearance_settings())
        """
        return {
            "dark_mode": self.dark_mode,
            "accent_color": self.accent_color,
            "font_choice": self.font_choice,
            "enable_animations": self.enable_animations
        }
        
    def get_notification_settings(self):
        """
        Récupère uniquement les paramètres de notification.
        
        Returns:
            dict: Préférences de notifications par type
            
        Utilisation dans l'API:
            Idéal pour vérifier rapidement si un type de notification
            est activé avant d'en envoyer une.
            
        Exemple d'utilisation dans une autre partie du code:
            if user.preferences.get_notification_settings()['badge']:
                # Envoyer une notification de badge
        """
        return {
            "badge": self.notif_badge,
            "objectif": self.notif_objectif,
            "info": self.notif_info,
            "statistique": self.notif_statistique
        }
    
    def reset_to_defaults(self):
        """
        Réinitialise toutes les préférences aux valeurs par défaut.
        
        Utilisation dans l'API:
            Parfait pour un endpoint permettant à l'utilisateur de
            réinitialiser toutes ses préférences d'un coup.
            
        Exemple dans une vue:
            @action(detail=False, methods=['post'])
            def reset(self, request):
                prefs = request.user.preferences
                prefs.reset_to_defaults()
                return Response(self.get_serializer(prefs).data)
        """
        self.dark_mode = False
        self.accent_color = "#6C63FF"
        self.font_choice = "Roboto"
        self.enable_animations = True
        self.notif_badge = True
        self.notif_objectif = True
        self.notif_info = True
        self.notif_statistique = True
        self.save()
        
    @classmethod
    def get_or_create_for_user(cls, user):
        """
        Récupère les préférences d'un utilisateur ou les crée si elles n'existent pas.
        
        Args:
            user: L'utilisateur pour lequel récupérer/créer les préférences
            
        Returns:
            UserPreference: Instance de préférences
            
        Utilisation dans l'API:
            Très utile dans les vues pour s'assurer que l'utilisateur
            a toujours des préférences définies.
            
        Exemple dans une vue:
            def get_object(self):
                return UserPreference.get_or_create_for_user(self.request.user)
        """
        prefs, created = cls.objects.get_or_create(
            user=user,
            defaults={
                # Valeurs par défaut définies ici pour être sûr
                "dark_mode": False,
                "accent_color": "#6C63FF",
                "font_choice": "Roboto",
                "enable_animations": True,
                "notif_badge": True,
                "notif_objectif": True,
                "notif_info": True,
                "notif_statistique": True
            }
        )
        return prefs
        
    def should_send_notification(self, notif_type):
        """
        Vérifie si un type spécifique de notification est activé.
        
        Args:
            notif_type (str): Type de notification ('badge', 'objectif', etc.)
            
        Returns:
            bool: True si ce type de notification est activé
            
        Utilisation dans l'API:
            Idéal pour les services de notification pour vérifier
            les préférences de l'utilisateur avant d'envoyer une notification.
            
        Exemple:
            if user.preferences.should_send_notification('badge'):
                send_badge_notification(user, badge)
        """
        mapping = {
            'badge': self.notif_badge,
            'objectif': self.notif_objectif,
            'info': self.notif_info,
            'statistique': self.notif_statistique
        }
        return mapping.get(notif_type, False)
    




    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------


[
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 1",
      "description": "Tu as atteint le niveau 1 💪",
      "icon": "🥉",
      "condition": "Atteindre 1 entrée"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 2",
      "description": "Tu as atteint le niveau 2 💪",
      "icon": "🥉",
      "condition": "Atteindre 5 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 3",
      "description": "Tu as atteint le niveau 3 💪",
      "icon": "🥈",
      "condition": "Atteindre 10 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 4",
      "description": "Tu as atteint le niveau 4 💪",
      "icon": "🥈",
      "condition": "Atteindre 20 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 5",
      "description": "Tu as atteint le niveau 5 💪",
      "icon": "🥇",
      "condition": "Atteindre 35 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 6",
      "description": "Tu as atteint le niveau 6 💪",
      "icon": "🥇",
      "condition": "Atteindre 50 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 7",
      "description": "Tu as atteint le niveau 7 💪",
      "icon": "🏆",
      "condition": "Atteindre 75 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 8",
      "description": "Tu as atteint le niveau 8 💪",
      "icon": "🏆",
      "condition": "Atteindre 100 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 9",
      "description": "Tu as atteint le niveau 9 💪",
      "icon": "🏅",
      "condition": "Atteindre 150 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 10",
      "description": "Tu as atteint le niveau 10 💪",
      "icon": "🎖️",
      "condition": "Atteindre 200 entrées"
    }
  },

  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Première entrée",
      "description": "Bravo pour ta première entrée 🎉",
      "icon": "🌱",
      "condition": "Créer une première entrée de journal"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Régulier",
      "description": "Bravo pour ta régularité sur 5 jours consécutifs !",
      "icon": "📅",
      "condition": "5 jours consécutifs avec au moins une entrée"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Discipline",
      "description": "La discipline est ta force, continue comme ça !",
      "icon": "🧘‍♂️",
      "condition": "10 jours consécutifs d’entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Résilience",
      "description": "Ta constance forge ta progression",
      "icon": "💎",
      "condition": "15 jours consécutifs d’entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Légende du Journal",
      "description": "Une légende est née : 30 jours d’affilée !",
      "icon": "🔥",
      "condition": "30 jours consécutifs d’entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Ambassadeur d’humeur",
      "description": "Tu rayonnes de positivité !",
      "icon": "😄",
      "condition": "Moyenne d’humeur ≥ 9 sur les 7 derniers jours"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Productivité",
      "description": "Journée ultra-productive !",
      "icon": "⚡",
      "condition": "Ajouter 3 entrées en une seule journée"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Objectif rempli !",
      "description": "Tu avances avec clarté et détermination.",
      "icon": "✅",
      "condition": "Tous les objectifs actuels sont atteints"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Persévérance",
      "description": "Tu montes pas à pas vers les sommets.",
      "icon": "🏔️",
      "condition": "Atteindre 100 entrées"
    }
  }
]
    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------

# services/badge_service.py

from ..models.badge_model import Badge, BadgeTemplate


def update_user_badges(user):
    existing_badges = set(user.badges.values_list('name', flat=True))
    for template in BadgeTemplate.objects.all():
        if template.name not in existing_badges and template.check_unlock(user):
            Badge.objects.create(
                user=user,
                name=template.name,
                icon=template.icon,
                description=template.description,
                level=template.level,
            )

# services/preferences_service.py

from ..models.userPreference_model import UserPreference


def create_preferences_for_user(user):
    return UserPreference.objects.get_or_create(user=user)[0]

# services/streak_service.py

def update_user_streak(user):
    current = user.current_streak()
    if current > user.longest_streak:
        user.longest_streak = current
        user.save(update_fields=['longest_streak'])

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from collections import defaultdict
from django.conf import settings
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from ..services.badge_service import update_user_badges
from ..services.preferences_service import create_preferences_for_user
from ..services.streak_service import update_user_streak


def mood_average(self, days=7, reference_date=None):
        """
        Calcule la moyenne d'humeur sur les X derniers jours.
        
        Args:
            days (int): Nombre de jours à considérer pour le calcul
            reference_date (date, optional): Date de référence (maintenant par défaut)
            
        Returns:
            float: Moyenne d'humeur arrondie à 1 décimale, ou None si aucune entrée
        """
        if reference_date is None:
            reference_date = now()
            
        entries = self.entries.filter(created_at__gte=reference_date - timedelta(days=days))
        avg = entries.aggregate(avg=Avg('mood'))['avg']
        return round(avg, 1) if avg is not None else None

def current_streak(self, reference_date=None):
        """
        Calcule la série actuelle de jours consécutifs avec au moins une entrée.
        Vérifie jusqu'à 365 jours en arrière.
        
        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre de jours consécutifs avec une entrée
        """
        if reference_date is None:
            reference_date = now().date()
            
        streak = 0
        for i in range(0, 365):
            day = reference_date - timedelta(days=i)
            if self.entries.filter(created_at__date=day).exists():
                streak += 1
            else:
                break
        return streak

def has_entries_every_day(self, last_n_days=7, reference_date=None):
        """
        Vérifie si l'utilisateur a fait au moins une entrée chaque jour
        pendant les n derniers jours.
        
        Args:
            last_n_days (int): Nombre de jours à vérifier
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            bool: True si l'utilisateur a une entrée pour chaque jour de la période
        """
        if reference_date is None:
            reference_date = now().date()
            
        start_date = reference_date - timedelta(days=last_n_days - 1)
        days_with_entry = self.entries.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=reference_date
        ).values_list("created_at__date", flat=True).distinct()
        
        expected_days = {start_date + timedelta(days=i) for i in range(last_n_days)}
        return len(expected_days) == len(set(days_with_entry))

@cached_property
def level(self):
        """
        Calcule le niveau de l'utilisateur basé sur le nombre d'entrées.
        Le niveau augmente tous les 10 entrées.
        
        Returns:
            int: Niveau actuel de l'utilisateur
        """
        return (self.total_entries() // 10) + 1

def total_entries(self):
        """
        Retourne le nombre total d'entrées de journal pour cet utilisateur.
        Utilise la relation inverse 'entries' définie dans JournalEntry.
        """
        return self.entries.count()




def all_objectives_achieved(self):
        """
        Vérifie si tous les objectifs de l'utilisateur sont achevés.
        
        Returns:
            bool: True si tous les objectifs sont achevés, False sinon
        """
        return not self.objectives.filter(done=False).exists()

def entries_today(self, reference_date=None):
        """
        Compte le nombre d'entrées faites aujourd'hui.
        
        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre d'entrées d'aujourd'hui
        """
        if reference_date is None:
            reference_date = now().date()
            
        return self.entries.filter(created_at__date=reference_date).count()
    
def entries_by_category(self, days=None):
        """
        Calcule la distribution des entrées par catégorie.
        
        Args:
            days (int, optional): Limite aux N derniers jours si spécifié
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
        """
        entries = self.entries.all()
        if days:
            entries = entries.filter(created_at__gte=now() - timedelta(days=days))
            
        return dict(entries.values('category').annotate(count=Count('id')).values_list('category', 'count'))

def entries_last_n_days(self, n=7):
        """
        Retourne les entrées des n derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            QuerySet: Entrées des n derniers jours
        """
        since = now() - timedelta(days=n)
        return self.entries.filter(created_at__gte=since)

def entries_per_day(self, n=7):
        """
        Calcule le nombre d'entrées par jour sur les n derniers jours.
        Utilise les fonctions d'agrégation de Django pour optimiser la requête.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec dates comme clés et nombre d'entrées comme valeurs
        """
        from django.db.models.functions import TruncDate
        
        since = now() - timedelta(days=n)
        entries = self.entries.filter(created_at__gte=since)
        data = entries.annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day')
        return {d['day']: d['count'] for d in data}

def mood_trend(self, n=7):
        """
        Calcule la moyenne d'humeur par jour sur les n derniers jours.
        Utilise les fonctions d'agrégation de Django pour optimiser la requête.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec dates comme clés et moyennes d'humeur comme valeurs
        """
        from django.db.models.functions import TruncDate
        
        since = now() - timedelta(days=n)
        entries = self.entries.filter(created_at__gte=since)
        data = entries.annotate(day=TruncDate('created_at')).values('day').annotate(moyenne=Avg('mood')).order_by('day')
        return {d['day']: round(d['moyenne'], 1) for d in data}

def days_with_entries(self, n=30):
        """
        Retourne la liste des jours avec au moins une entrée dans les n derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            list: Liste des dates avec au moins une entrée
        """
        since = now().date() - timedelta(days=n)
        return list(
            self.entries.filter(created_at__date__gte=since)
            .values_list("created_at__date", flat=True)
            .distinct()
        )

def entries_per_category_last_n_days(self, n=7):
        """
        Calcule la distribution des entrées par catégorie pour les n derniers jours.
        Optimisé avec agrégation Django.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
        """
        since = now() - timedelta(days=n)
        return dict(
            self.entries.filter(created_at__gte=since)
            .values('category')
            .annotate(count=Count('id'))
            .values_list('category', 'count')
        )
def update_badges(self):
        update_user_badges(self)

def update_streaks(self):
        update_user_streak(self)

def create_default_preferences(self):
        return create_preferences_for_user(self)

from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import timedelta

def get_weekly_entry_stats(user):
    """
    Retourne le nombre d'entrées du journal pour chaque jour de la semaine en cours (Lundi à Dimanche).
    Format de sortie : liste de 7 dicts avec 'day' et 'total'.
    """
    today = now().date()
    week_start = today - timedelta(days=today.weekday())  # Lundi
    week_end = week_start + timedelta(days=6)

    # Récupérer les entrées de la semaine
    entries = user.entries.filter(created_at__date__range=(week_start, week_end))

    # Grouper par jour
    daily_stats = (
        entries.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('id'))
    )

    # Transformation en dict pour un accès rapide
    stats_map = {item["day"]: item["total"] for item in daily_stats}

    # Générer les 7 jours
    result = []
    for i in range(7):
        date = week_start + timedelta(days=i)
        result.append({
            "day": date.strftime('%A'),  # ex : "Lundi"
            "total": stats_map.get(date, 0)
        })

    return result


    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
import logging
from django.db.models.signals import post_delete

from .models.badge_model import Badge
from .models.journal_model import JournalEntry
from .models.notification_model import Notification
from .models.stats_model import DailyStat
from .models.userPreference_model import UserPreference
from .models.user_model import User

from .utils.levels import get_user_level  # Cette fonction calcule le niveau d'un utilisateur

# Configuration du logger pour tracer les événements importants
logger = logging.getLogger(__name__)


# 🏅 Fonction générique pour créer un badge, une notification et un log
def award_badge(user, name, description, icon):
    """
    Fonction utilitaire pour attribuer un badge à un utilisateur.
    Crée également une notification pour informer l'utilisateur.
    
    Args:
        user: L'utilisateur à qui attribuer le badge
        name: Nom du badge
        description: Description du badge
        icon: Icône représentant le badge (emoji)
        
    Returns:
        bool: True si le badge a été nouvellement créé, False s'il existait déjà
    """
    badge, created = Badge.objects.get_or_create(
        user=user,
        name=name,
        defaults={
            "description": description,
            "icon": icon,
        }
    )
    # Si le badge vient d'être créé, on notifie l'utilisateur
    if created:
        Notification.objects.create(
            user=user,
            message=f"{icon} Nouveau badge : {name} !"
        )
        # Journalisation de l'événement pour le suivi administratif
        logger.info(f"[BADGE] {user.username} a débloqué : {name}")
    return created


@receiver(post_save, sender=JournalEntry)
def check_badges_and_stats(sender, instance, created, **kwargs):
    """
    Signal déclenché à la sauvegarde d'une JournalEntry.
    Gère deux aspects principaux :
    1. Mise à jour des statistiques journalières
    2. Attribution des badges en fonction des accomplissements
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (JournalEntry)
        instance: Instance du modèle qui a été sauvegardée
        created: Booléen indiquant si l'instance vient d'être créée (True) ou mise à jour (False)
        **kwargs: Arguments supplémentaires du signal
    """
    user = instance.user

    # 🔄 Met à jour ou crée les statistiques journalières pour la date de l'entrée
    DailyStat.generate_for_user(user=user, date=instance.created_at.date())

    # ⚠️ On ne vérifie les badges que si c'est une nouvelle entrée
    # Évite de dupliquer les badges lors des mises à jour d'entrées existantes
    if not created:
        return

    # Récupère le nombre total d'entrées de l'utilisateur
    total = user.entries.count()

    # ✅ Badge : première entrée
    # Décerné lorsque l'utilisateur crée sa toute première entrée
    if total == 1:
        award_badge(
            user,
            name="Première entrée",
            description="Bravo pour ta première entrée 🎉",
            icon="🌱"
        )

    # ✅ Badge : 7 jours d'activité consécutifs
    # Vérifie si l'utilisateur a au moins une entrée pour chacun des 7 derniers jours
    streak_days = 7
    today = now().date()
    # Vérifie l'existence d'au moins une entrée pour chaque jour de la période
    has_streak = all(
        user.entries.filter(created_at__date=today - timedelta(days=i)).exists()
        for i in range(streak_days)
    )
    if has_streak:
        award_badge(
            user,
            name="7 jours d'activité",
            description="1 semaine d'activité, continue comme ça 🚀",
            icon="🔥"
        )

    # ✅ Badge : Niveau
    # Attribue un badge lorsque l'utilisateur atteint un nouveau niveau
    # La fonction get_user_level détermine le niveau en fonction du nombre total d'entrées
    level = get_user_level(total)
    if level > 0:
        badge_name = f"Niveau {level}"
        # Vérifie si l'utilisateur n'a pas déjà ce badge
        if not user.badges.filter(name=badge_name).exists():
            award_badge(
                user,
                name=badge_name,
                description=f"Tu as atteint le niveau {level} 💪",
                icon="🏆"
            )


@receiver(post_delete, sender=JournalEntry)
def update_stats_on_delete(sender, instance, **kwargs):
    """
    Signal déclenché à la suppression d'une JournalEntry.
    Assure que les statistiques journalières restent cohérentes après la suppression d'une entrée.
    
    Deux cas possibles :
    1. S'il reste des entrées pour cette date : recalcule les statistiques
    2. S'il n'y a plus d'entrées pour cette date : supprime les statistiques
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (JournalEntry)
        instance: Instance du modèle qui a été supprimée
        **kwargs: Arguments supplémentaires du signal
    """
    user = instance.user
    date = instance.created_at.date()

    # 🔄 Vérifie s'il reste des entrées pour cette date
    entries = user.entries.filter(created_at__date=date)
    if entries.exists():
        # S'il reste des entrées, recalcule les statistiques
        DailyStat.generate_for_user(user=user, date=date)
    else:
        # S'il n'y a plus d'entrées, supprime les statistiques pour cette date
        DailyStat.objects.filter(user=user, date=date).delete()
        # Journalise l'événement pour le suivi administratif
        logger.info(f"[STATS] Statistiques supprimées pour {user.username} - {date}")

@receiver(post_save, sender=Notification)
def mark_other_notifications_as_read(sender, instance, created, **kwargs):
    """
    Quand une notification est créée, marque les autres comme lues.
    """
    if created:
        # Marquer toutes les autres notifications de l'utilisateur comme lues
        Notification.objects.filter(
            user=instance.user,
            is_read=False
        ).exclude(id=instance.id).update(is_read=True)

@receiver(post_save, sender=Notification)
def limit_notifications(sender, instance, **kwargs):
    """
    Signal déclenché après la sauvegarde d'une notification.
    Limite le nombre maximum de notifications par utilisateur pour éviter une surcharge de la base de données.
    
    Fonctionnement :
    - Récupère toutes les notifications de l'utilisateur, triées par date (plus récentes d'abord)
    - Si le nombre dépasse la limite, supprime les plus anciennes
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (Notification)
        instance: Instance de notification qui vient d'être sauvegardée
        **kwargs: Arguments supplémentaires du signal
    """
    max_notifs = 100  # Nombre maximum de notifications à conserver par utilisateur
    
    # Récupère les notifications de l'utilisateur, triées des plus récentes aux plus anciennes
    qs = Notification.objects.filter(user=instance.user).order_by('-created_at')
    
    # Si le nombre dépasse la limite
    if qs.count() > max_notifs:
        # Sélectionne les notifications à supprimer (les plus anciennes au-delà de la limite)
        to_delete = qs[max_notifs:]
        # Supprime ces notifications
        to_delete.delete()
        

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Signal déclenché après la création d'un utilisateur.
    Crée automatiquement un objet de préférences par défaut pour chaque nouvel utilisateur.
    
    Cette fonction garantit que chaque utilisateur dispose immédiatement de préférences configurées
    avec les valeurs par défaut, ce qui simplifie le reste du code de l'application.
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (User)
        instance: L'utilisateur qui vient d'être créé ou modifié
        created: Booléen indiquant si l'utilisateur vient d'être créé (True) ou mis à jour (False)
        **kwargs: Arguments supplémentaires du signal
    """
    # Vérifie s'il s'agit d'un nouvel utilisateur
    if created:
        # Crée un objet de préférences par défaut pour cet utilisateur
        UserPreference.objects.create(user=instance)

    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------

from celery import shared_task
from django.utils.timezone import now
from .models import Notification

@shared_task
def send_scheduled_notifications():
    """
    Tâche périodique pour envoyer les notifications programmées.
    
    Cette tâche est exécutée par Celery selon une planification définie dans les paramètres.
    Elle identifie toutes les notifications programmées dont la date d'échéance est atteinte
    et n'ont pas encore été lues, puis effectue les actions nécessaires pour les envoyer.
    
    Returns:
        str: Message indiquant le nombre de notifications traitées
    """
    # Récupère toutes les notifications programmées dont la date d'envoi est arrivée
    # et qui n'ont pas encore été lues
    qs = Notification.objects.filter(scheduled_at__lte=now(), is_read=False)
    
    count = 0  # Compteur pour suivre le nombre de notifications traitées
    
    for notif in qs:
        # Ici, implémentez la logique d'envoi appropriée selon le type de notification
        # Par exemple : envoi d'email, notification push, SMS, etc.
        # Exemple : send_push_notification(notif.user.device_token, notif.message)
        
        notif.mark_as_read()  # Marque la notification comme lue après l'envoi
        count += 1
    
    # Retourne un message descriptif pour les logs Celery
    return f"{count} notifications envoyées"










    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------
    --------------------------------------------------