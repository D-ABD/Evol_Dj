# services/badge_service.py

from ..models.badge_model import Badge, BadgeTemplate


def update_user_badges(user):
    existing_badges = set(user.badges.values_list('name', flat=True))
    for template in BadgeTemplate.objects.all():
        if template.name not in existing_badges and template.check_unlock(user):
            Badge.objects.create(
                user=user,
                name=template.name,
                icon=template.icon,
                description=template.description,
                level=template.level,
            )
