# services/journal_service.py

from datetime import timedelta
from ..models import JournalEntry

def create_journal_entry(user, content, mood, category):
    """
    Crée une entrée de journal pour l'utilisateur.
    
    Args:
        user (User): L'utilisateur à qui l'entrée est associée
        content (str): Contenu de l'entrée
        mood (int): Note d'humeur
        category (str): Catégorie de l'entrée
    
    Returns:
        JournalEntry: L'entrée de journal nouvellement créée
    """
    entry = JournalEntry.objects.create(
        user=user,
        content=content,
        mood=mood,
        category=category
    )
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
    return JournalEntry.get_entries_by_date_range(user, start_date, end_date)
