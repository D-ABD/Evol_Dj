
#: Liste des seuils fixes correspondant aux 5 premiers niveaux de l'utilisateur.
#: Utilisée pour calculer la progression jusqu'au niveau 5.
#: Au-delà, la progression se fait par palier de 15 entrées par niveau.
LEVEL_THRESHOLDS = [1, 5, 10, 20, 35]

def get_user_level(entry_count: int) -> int:
    """
    Calcule le niveau d’un utilisateur en fonction du nombre d’entrées.
    Le niveau augmente selon un palier fixe puis par incrément après le niveau 5.
    """
    if entry_count < 1:
        return 0
    elif entry_count < 5:
        return 1
    elif entry_count < 10:
        return 2
    elif entry_count < 20:
        return 3
    elif entry_count < 35:
        return 4
    else:
        # Progression régulière tous les 15 journaux après le niveau 4
        return 5 + ((entry_count - 35) // 15)
LEVEL_THRESHOLDS = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]


def get_user_progress(entry_count: int) -> dict:
    """
    Retourne un dictionnaire contenant :
    - le niveau actuel,
    - la progression en pourcentage vers le niveau suivant,
    - le seuil du niveau suivant,
    - le nombre total d’entrées.
    """
    level = get_user_level(entry_count)

    # Liste des seuils fixes jusqu’au niveau 5
    thresholds = [1, 5, 10, 20, 35]

    # Définition des seuils actuel et suivant
    if level < 5:
        current_threshold = thresholds[level - 1] if level > 0 else 0
        next_threshold = thresholds[level]
    else:
        current_threshold = 35 + (level - 5) * 15
        next_threshold = current_threshold + 15

    # Calcul de la progression (0-100 %)
    if next_threshold > current_threshold:
        raw_progress = (entry_count - current_threshold) / (next_threshold - current_threshold)
        progress = min(100, max(0, int(raw_progress * 100)))
    else:
        progress = 100

    return {
        "level": level,
        "progress": progress,
        "next_threshold": next_threshold,
        "entries": entry_count,
    }