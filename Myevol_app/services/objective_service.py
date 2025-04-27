# services/objective_service.py

import logging
from django.db import IntegrityError
from django.utils.timezone import now
from ..models.objective_model import Objective
from ..services.notification_service import create_user_notification

logger = logging.getLogger(__name__)

class ObjectiveService:
    """
    Service métier dédié à la gestion des objectifs des utilisateurs.
    Fournit des méthodes pour la création, la mise à jour, la complétion
    et les statistiques d'objectifs.
    """

    @staticmethod
    def create_objective(user, title, category, target_date, target_value):
        """
        Crée un nouvel objectif utilisateur.

        Args:
            user (User): Utilisateur concerné
            title (str): Titre de l’objectif
            category (str): Catégorie liée
            target_date (date): Date cible d’achèvement
            target_value (int): Valeur cible à atteindre

        Returns:
            Objective: L’instance créée
        """
        try:
            objective = Objective.objects.create(
                user=user,
                title=title,
                category=category,
                target_date=target_date,
                target_value=target_value
            )
            logger.info(f"[OBJECTIF] Objectif créé : '{title}' pour {user.username}")
            return objective
        except IntegrityError as e:
            logger.error(f"[OBJECTIF] ❌ Erreur création pour {user.username} : {e}")
            raise

    @staticmethod
    def update_objective(objective, title=None, category=None, target_date=None, target_value=None):
        """
        Met à jour un objectif existant.

        Args:
            objective (Objective): Objectif cible
            title (str, optional): Nouveau titre
            category (str, optional): Nouvelle catégorie
            target_date (date, optional): Nouvelle date
            target_value (int, optional): Nouvelle valeur cible

        Returns:
            Objective: Objectif mis à jour
        """
        if title:
            objective.title = title
        if category:
            objective.category = category
        if target_date:
            objective.target_date = target_date
        if target_value:
            objective.target_value = target_value

        objective.save()
        logger.info(f"[OBJECTIF] Objectif mis à jour : '{objective.title}' pour {objective.user.username}")
        return objective

    @staticmethod
    def mark_as_complete(objective):
        """
        Marque un objectif comme complété (si non déjà fait),
        et notifie l’utilisateur.

        Args:
            objective (Objective): Objectif à compléter

        Returns:
            Objective: L’objectif mis à jour
        """
        if not objective.done:
            objective.done = True
            objective.save()
            logger.info(f"[OBJECTIF] ✅ Objectif complété : '{objective.title}' pour {objective.user.username}")
            create_user_notification(
                user=objective.user,
                message=f"🎯 Objectif atteint : {objective.title}",
                notif_type="objectif"
            )
        return objective

    @staticmethod
    def get_user_objectives(user):
        """
        Retourne tous les objectifs d’un utilisateur.

        Args:
            user (User): L’utilisateur concerné

        Returns:
            QuerySet: Objectifs classés par date
        """
        return Objective.objects.filter(user=user).order_by('target_date')

    @staticmethod
    def get_statistics(user):
        """
        Calcule des statistiques globales sur les objectifs d’un utilisateur.

        Args:
            user (User): L’utilisateur cible

        Returns:
            dict: Données agrégées sur les objectifs
        """
        objectives = Objective.objects.filter(user=user)
        total = objectives.count()
        completed = objectives.filter(done=True).count()
        overdue = objectives.filter(done=False, target_date__lt=now().date()).count()

        completion_rate = (completed / total * 100) if total > 0 else 0

        logger.info(f"[OBJECTIF] Stats pour {user.username} : {completed}/{total} terminés")
        return {
            'total': total,
            'completed': completed,
            'completion_rate': round(completion_rate, 1),
            'overdue': overdue
        }
