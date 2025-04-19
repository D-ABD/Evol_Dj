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