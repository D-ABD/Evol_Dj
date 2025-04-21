# services/userPreference_service.py
import logging
from django.shortcuts import get_object_or_404
from ..models.userPreference_model import UserPreference

logger = logging.getLogger(__name__)

def create_or_update_preferences(user, preferences_data=None):
    """
    Crée ou met à jour les préférences de l'utilisateur.
    
    Args:
        user: L'utilisateur pour lequel les préférences doivent être créées ou mises à jour.
        preferences_data: Données de préférences (optionnel, si fourni, cela écrase les préférences existantes).
        
    Returns:
        UserPreference: L'instance mise à jour ou créée des préférences.
        
    Cette fonction interagit directement avec le modèle `UserPreference` pour :
    - Créer ou récupérer les préférences existantes.
    - Mettre à jour les préférences avec de nouvelles valeurs.
    - Enregistrer les changements dans la base de données.
    """
    prefs, created = UserPreference.objects.get_or_create(user=user)
    logger.info(f"{'Création' if created else 'Mise à jour'} des préférences pour l'utilisateur {user.username}.")
    
    if preferences_data:
        # Valider et mettre à jour les préférences
        for key, value in preferences_data.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
            else:
                logger.warning(f"Clé '{key}' non valide pour les préférences de {user.username}.")
        
        prefs.save()
        logger.info(f"Préférences mises à jour pour l'utilisateur {user.username}.")
    else:
        logger.info(f"Aucune mise à jour des préférences pour {user.username}.")

    return prefs


def reset_preferences_to_defaults(user):
    """
    Réinitialise les préférences aux valeurs par défaut pour un utilisateur donné.
    
    Args:
        user: L'utilisateur pour lequel les préférences doivent être réinitialisées.
        
    Returns:
        UserPreference: L'instance réinitialisée des préférences.
        
    Cette fonction utilise la méthode `reset_to_defaults` du modèle `UserPreference` 
    pour réinitialiser les préférences aux valeurs par défaut.
    """
    prefs = get_object_or_404(UserPreference, user=user)
    prefs.reset_to_defaults()
    logger.info(f"Préférences réinitialisées aux valeurs par défaut pour l'utilisateur {user.username}.")
    return prefs
