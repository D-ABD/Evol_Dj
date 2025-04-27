# Liste des seuils fixes correspondant aux 10 premiers niveaux de l'utilisateur.
LEVEL_THRESHOLDS = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]

def get_user_level(entry_count: int) -> int:
    """
    Détermine le niveau d’un utilisateur basé sur son nombre total d’entrées de journal.

    Le niveau augmente en fonction des seuils définis dans `LEVEL_THRESHOLDS`.
    Par exemple :
    - < 1 entrée → niveau 0
    - ≥ 1 et < 5 entrées → niveau 1
    - ≥ 5 et < 10 entrées → niveau 2
    - ...
    - ≥ 200 entrées → niveau 10

    Args:
        entry_count (int): Nombre total d’entrées de journal de l'utilisateur.

    Returns:
        int: Niveau actuel de l'utilisateur (entre 0 et 10).
    """
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if entry_count < threshold:
            return i
    return len(LEVEL_THRESHOLDS)  # Niveau maximal atteint


def get_user_progress(entry_count: int) -> dict:
    """
    Calcule les informations de progression de l'utilisateur vers le prochain niveau.

    Cette fonction retourne :
    - le niveau actuel,
    - le pourcentage de progression vers le niveau suivant (entre 0 et 100),
    - le seuil du prochain niveau,
    - le nombre d'entrées totales.

    Args:
        entry_count (int): Nombre total d’entrées de journal de l'utilisateur.

    Returns:
        dict: Un dictionnaire contenant les clés :
            - "level" (int)
            - "progress" (int)
            - "next_threshold" (int)
            - "entries" (int)
    """
    level = get_user_level(entry_count)

    if level == 0:
        current_threshold = 0
        next_threshold = LEVEL_THRESHOLDS[0]
    elif level < len(LEVEL_THRESHOLDS):
        current_threshold = LEVEL_THRESHOLDS[level - 1]
        next_threshold = LEVEL_THRESHOLDS[level]
    else:
        current_threshold = LEVEL_THRESHOLDS[-1]
        next_threshold = current_threshold + 1  # optionnel

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
