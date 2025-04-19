# services/streak_service.py

def update_user_streak(user):
    current = user.current_streak()
    if current > user.longest_streak:
        user.longest_streak = current
        user.save(update_fields=['longest_streak'])
