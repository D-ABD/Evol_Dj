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
    """
    ...
    Ajouts personnalisés :
    - avatar_url : URL de l’avatar (image de profil)
    - xp : nombre de points d’expérience accumulés
    - level : calculé automatiquement en fonction des entrées (property)

    API Endpoints recommandés :
    - /api/users/me/
    - /api/users/me/dashboard/
    - /api/users/me/stats/
    - /api/users/me/xp/
    - /api/users/me/avatar/
    
    """
    email = models.EmailField(unique=True)  # Assure que chaque email est unique
    longest_streak = models.PositiveIntegerField(default=0, editable=False)  # Plus longue série de jours consécutifs
    avatar_url = models.URLField(blank=True, null=True, help_text="Lien vers l'image de l'avatar")
    xp = models.PositiveIntegerField(default=0, help_text="Points d'expérience cumulés")

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
    
    def add_xp(self, amount):
        """
        Ajoute des points d’expérience à l’utilisateur.

        Args:
            amount (int): Nombre de points à ajouter.

        Utilisation dans l’API :
            À appeler après certaines actions utilisateurs (ex: ajout d’entrée, objectif atteint).
            Permet de créer un système de progression basé sur le comportement utilisateur.
        
        Exemple :
            user.add_xp(10)
        """
        self.xp += amount
        self.save(update_fields=['xp'])

