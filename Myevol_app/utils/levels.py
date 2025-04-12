def get_user_level(entry_count: int) -> int:
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
        # Progression tous les 15 journaux après niveau 5
        return 5 + ((entry_count - 35) // 15)

def get_user_progress(entry_count: int) -> dict:
    level = get_user_level(entry_count)
    thresholds = [1, 5, 10, 20, 35]
    next_threshold = 50 if level >= 5 else thresholds[min(level, len(thresholds)-1)]

    current_threshold = thresholds[level - 1] if level > 0 and level <= len(thresholds) else 35
    progress = min(100, int((entry_count - current_threshold) / (next_threshold - current_threshold) * 100)) if next_threshold > current_threshold else 100

    return {
        "level": level,
        "progress": progress,
        "next_threshold": next_threshold,
        "entries": entry_count,
    }
