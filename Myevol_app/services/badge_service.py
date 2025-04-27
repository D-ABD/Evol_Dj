# services/badge_service.py

import logging
from typing import List, Optional
from ..models.badge_model import Badge, BadgeTemplate
from ..models.event_log_model import EventLog

logger = logging.getLogger(__name__)

def update_user_badges(user, *, log_events: bool = True, return_new_badges: bool = False) -> Optional[List[Badge]]:
    """
    Vérifie tous les BadgeTemplates disponibles et attribue les badges éligibles à l’utilisateur.

    Args:
        user (User): L'utilisateur pour lequel vérifier et attribuer les badges.
        log_events (bool, optional): Si True, un EventLog est créé pour chaque badge attribué. (Défaut: True)
        return_new_badges (bool, optional): Si True, retourne la liste des nouveaux badges créés. (Défaut: False)

    Returns:
        Optional[List[Badge]]: Liste des badges nouvellement créés si return_new_badges est True.
        Sinon, retourne None.

    Comportement :
        - Récupère les badges déjà obtenus par l'utilisateur.
        - Parcourt tous les BadgeTemplates :
            - Ignore ceux déjà obtenus.
            - Vérifie si les conditions d'obtention sont remplies.
            - Crée un nouveau Badge si éligible.
            - Logue l'événement et une entrée dans EventLog si demandé.
        - En cas d'erreur à la création d'un badge, retourne une liste vide immédiatement.
        - Si aucun nouveau badge n'est créé, logue une info.

    Exemple d'usage :
        >>> update_user_badges(user, log_events=True, return_new_badges=True)
    """
    existing_badge_names = set(user.badges.values_list("name", flat=True))
    new_badges = []

    for template in BadgeTemplate.objects.all():
        if template.name in existing_badge_names:
            continue  # L'utilisateur a déjà ce badge

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
                return []  # 🔥 Important : retour immédiat si erreur

    if log_events and not new_badges:
        logger.info(f"[BADGE] Aucun nouveau badge attribué à {user.username}")

    if return_new_badges and new_badges:
        logger.debug(f"Badges retournés pour {user.username} : {[b.name for b in new_badges]}")

    return new_badges if return_new_badges else None

    



def __create_badge(user, template: BadgeTemplate) -> Badge:
    """
    Crée un badge pour un utilisateur à partir d’un template.

    Args:
        user (User): Utilisateur à qui le badge est attribué
        template (BadgeTemplate): Modèle de badge (critères, nom, icône, etc.)

    Returns:
        Badge: Le badge nouvellement créé et enregistré
    """
    return Badge.objects.create(
        user=user,
        name=template.name,
        icon=template.icon,
        description=template.description,
        level=template.level,
    )
