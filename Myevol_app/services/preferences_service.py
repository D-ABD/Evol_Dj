# services/preferences_service.py

from ..models.userPreference_model import UserPreference


def create_preferences_for_user(user):
    return UserPreference.objects.get_or_create(user=user)[0]
