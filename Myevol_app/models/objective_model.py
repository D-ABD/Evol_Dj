# MyEvol_app/models/objective_model.py

import logging
from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Création d'un logger
logger = logging.getLogger(__name__)

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
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="objectives")
    title = models.CharField(max_length=255, help_text="Titre de l'objectif.")
    category = models.CharField(max_length=100, help_text="Catégorie de l'objectif.")
    done = models.BooleanField(default=False, help_text="Indique si l'objectif est atteint.")
    target_date = models.DateField(help_text="Date cible pour atteindre l'objectif.")
    target_value = models.PositiveIntegerField(default=1, verbose_name="Objectif à atteindre", validators=[MinValueValidator(1)], help_text="Nombre d'actions nécessaires pour accomplir l'objectif.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'objectif.")

    class Meta:
        verbose_name = "Objectif"
        verbose_name_plural = "Objectifs"
        ordering = ['target_date', 'done']

    def __str__(self):
        """Représentation en chaîne de caractères de l'objectif avec indicateur d'achèvement"""
        return f"{self.title} ({'✅' if self.done else '🕓'})"

    def __repr__(self):
        """Représentation plus détaillée de l'objectif"""
        return f"<Objective id={self.id} title='{self.title}' done={self.done} target_date={self.target_date}>"

    def get_absolute_url(self):
        """Retourne l'URL vers l'objectif spécifique"""
        return f"/api/objectives/{self.id}/"

    def clean(self):
        """Vérifie que la date cible n'est pas dans le passé"""
        if self.target_date < now().date():
            raise ValidationError("La date cible ne peut pas être dans le passé.")

    def entries_done(self):
        """Compte le nombre d'entrées correspondant à la catégorie de cet objectif pour la date cible"""
        return self.user.entries.filter(
            category=self.category,
            created_at__date=self.target_date
        ).count()

    def progress(self):
        """Calcule le pourcentage de progression vers l'objectif"""
        if self.target_value > 0:
            return min(100, int((self.entries_done() / self.target_value) * 100))
        return 0

    def is_achieved(self):
        """Vérifie si l'objectif est atteint"""
        return self.done or self.progress() >= 100
        
    def days_remaining(self):
        """Calcule le nombre de jours restants avant la date cible"""
        return (self.target_date - now().date()).days
        
    def is_overdue(self):
        """Vérifie si l'objectif est en retard"""
        return not self.done and self.target_date < now().date()

    def save(self, *args, **kwargs):
        """
        Surcharge pour mettre à jour l'état 'done' automatiquement si l'objectif est atteint.
        La notification est désormais gérée par un signal externe.
        """
        self.full_clean()  # Appelle clean()

        logger.info(f"Sauvegarde de l'objectif: {self.title} (État: {'Complété' if self.done else 'En cours'})")

        if not self.done and self.progress() >= 100:
            self.done = True  # On le marque comme complété (notification déléguée au signal)

        super().save(*args, **kwargs)


    def is_due_today(self):
        """Vérifie si la date cible de l’objectif est aujourd’hui"""
        return self.target_date == now().date()

    @property
    def progress_percent(self):
        """Renvoie la progression de l’objectif en pourcentage (0 à 100)"""
        return self.progress()

    @classmethod
    def get_upcoming(cls, user, days=7):
        """Récupère les objectifs dont l'échéance approche dans les prochains jours"""
        today = now().date()
        deadline = today + timedelta(days=days)
        
        logger.info(f"Récupération des objectifs à venir pour {user.username}, dans les {days} prochains jours.")
        
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
        
        logger.info(f"Statistiques des objectifs pour {user.username} : Total {total}, Complétés {completed}, Taux de complétion {completion_rate}%")
        
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
