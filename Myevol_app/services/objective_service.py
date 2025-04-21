# services/objective_service.py

import logging
from django.db import IntegrityError
from ..models.objective_model import Objective, Notification
from django.utils.timezone import now

logger = logging.getLogger(__name__)

class ObjectiveService:
    """
    Classe de service pour gérer la logique métier associée aux objectifs utilisateurs.
    """

    @staticmethod
    def create_objective(user, title, category, target_date, target_value):
        """
        Crée un nouvel objectif pour un utilisateur.
        
        Args:
            user (User): L'utilisateur qui crée l'objectif.
            title (str): Titre de l'objectif.
            category (str): Catégorie de l'objectif.
            target_date (date): La date cible pour accomplir l'objectif.
            target_value (int): La valeur à atteindre pour accomplir l'objectif.

        Returns:
            Objective: L'objectif créé.
        """
        try:
            objective = Objective.objects.create(
                user=user,
                title=title,
                category=category,
                target_date=target_date,
                target_value=target_value
            )
            logger.info(f"Objectif créé pour {user.username}: {title}")
            return objective
        except IntegrityError as e:
            logger.error(f"Erreur lors de la création de l'objectif pour {user.username}: {e}")
            raise

    @staticmethod
    def update_objective(objective, title=None, category=None, target_date=None, target_value=None):
        """
        Met à jour un objectif existant.

        Args:
            objective (Objective): L'objectif à mettre à jour.
            title (str, optional): Nouveau titre de l'objectif.
            category (str, optional): Nouvelle catégorie.
            target_date (date, optional): Nouvelle date cible.
            target_value (int, optional): Nouvelle valeur cible.
        
        Returns:
            Objective: L'objectif mis à jour.
        """
        if title:
            objective.title = title
        if category:
            objective.category = category
        if target_date:
            objective.target_date = target_date
        if target_value:
            objective.target_value = target_value
        
        objective.save(create_notification=False)  # Ne pas créer de notification lors de la mise à jour
        logger.info(f"Objectif mis à jour pour {objective.user.username}: {objective.title}")
        return objective

    @staticmethod
    def mark_as_complete(objective):
        """
        Marque un objectif comme complété et envoie une notification.

        Args:
            objective (Objective): L'objectif à marquer comme complété.
        
        Returns:
            Objective: L'objectif mis à jour.
        """
        if not objective.done:
            objective.done = True
            objective.save(create_notification=True)  # Crée une notification lors de la complétion
            logger.info(f"Objectif complété pour {objective.user.username}: {objective.title}")
        return objective

    @staticmethod
    def get_user_objectives(user):
        """
        Récupère tous les objectifs d'un utilisateur.

        Args:
            user (User): L'utilisateur concerné.
        
        Returns:
            QuerySet: Ensemble des objectifs de l'utilisateur.
        """
        return Objective.objects.filter(user=user).order_by('target_date')

    @staticmethod
    def get_statistics(user):
        """
        Calcule des statistiques globales pour les objectifs d'un utilisateur.

        Args:
            user (User): L'utilisateur concerné.

        Returns:
            dict: Statistiques des objectifs de l'utilisateur.
        """
        objectives = Objective.objects.filter(user=user)
        total = objectives.count()
        completed = objectives.filter(done=True).count()
        overdue = objectives.filter(done=False, target_date__lt=now().date()).count()

        completion_rate = (completed / total * 100) if total > 0 else 0

        logger.info(f"Statistiques des objectifs pour {user.username}: Total: {total}, Complétés: {completed}, Taux de complétion: {completion_rate}%")
        return {
            'total': total,
            'completed': completed,
            'completion_rate': round(completion_rate, 1),
            'overdue': overdue
        }
