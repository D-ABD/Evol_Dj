# services/badge_service.py

import logging
from typing import List, Optional
from ..models.badge_model import Badge, BadgeTemplate
from ..models.event_log_model import EventLog

logger = logging.getLogger(__name__)

def update_user_badges(user, *, log_events: bool = True, return_new_badges: bool = False) -> Optional[List[Badge]]:
    """
    Vérifie tous les BadgeTemplates et attribue les badges éligibles à l’utilisateur.

    Args:
        user (User): L'utilisateur concerné
        log_events (bool): Active l'enregistrement d'un EventLog (True par défaut)
        return_new_badges (bool): Retourne les badges créés si True

    Returns:
        Optional[List[Badge]]: Liste des badges créés, ou None si aucun n’a été créé
    """
    existing_badge_names = set(user.badges.values_list("name", flat=True))
    new_badges = []

    for template in BadgeTemplate.objects.all():
        if template.name in existing_badge_names:
            continue  # L’utilisateur a déjà ce badge

        if template.check_unlock(user):
            try:
                badge = __create_badge(user, template)
                new_badges.append(badge)

                if log_events:
                    EventLog.objects.create(
                        user=user,
                        action="attribution_auto_badge",
                        description=f"Badge automatique '{template.name}' attribué à {user.username}"
                    )

                logger.info(f"[BADGE] ✅ {user.username} a débloqué : {template.name}")

            except Exception as e:
                logger.error(f"[BADGE] ❌ Erreur pour '{template.name}' → {user.username}: {e}")

    if log_events and not new_badges:
        logger.info(f"[BADGE] Aucun nouveau badge attribué à {user.username}")

    return new_badges if return_new_badges else None

def __create_badge(user, template: BadgeTemplate) -> Badge:
    """
    Crée et retourne un badge à partir d’un modèle.

    Args:
        user (User): Utilisateur cible
        template (BadgeTemplate): Modèle du badge

    Returns:
        Badge: Instance créée et enregistrée
    """
    return Badge.objects.create(
        user=user,
        name=template.name,
        icon=template.icon,
        description=template.description,
        level=template.level,
    )
