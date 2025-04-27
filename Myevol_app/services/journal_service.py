# services/journal_service.py

import logging
from datetime import timedelta
from django.core.exceptions import ValidationError
from ..models import JournalEntry

logger = logging.getLogger(__name__)

def create_journal_entry(user, content, mood, category):
    """
    Crée une entrée de journal pour l'utilisateur avec validation de la note d'humeur.

    Args:
        user (User): L'utilisateur à qui l'entrée est associée
        content (str): Contenu de l'entrée
        mood (int): Note d'humeur (doit être entre 1 et 10)
        category (str): Catégorie de l'entrée

    Returns:
        JournalEntry: L'entrée de journal nouvellement créée

    Raises:
        ValidationError: Si la note d'humeur est invalide
    """
    if not 1 <= mood <= 10:
        raise ValidationError("La note d'humeur doit être comprise entre 1 et 10.")

    normalized_category = category.strip().capitalize()

    entry = JournalEntry.objects.create(
        user=user,
        content=content.strip(),
        mood=mood,
        category=normalized_category
    )

    logger.info(f"[JOURNAL] Entrée créée pour {user.username} (humeur: {mood}, catégorie: {normalized_category})")

    return entry


def get_journal_entries(user, start_date, end_date):
    """
    Récupère les entrées de journal dans une plage de dates.

    Args:
        user (User): L'utilisateur concerné
        start_date (date): Date de début
        end_date (date): Date de fin

    Returns:
        QuerySet: Ensemble des entrées de journal
    """
    logger.debug(f"[JOURNAL] Récupération des entrées de {user.username} entre {start_date} et {end_date}")
    return JournalEntry.get_entries_by_date_range(user, start_date, end_date)
