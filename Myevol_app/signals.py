from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JournalEntry, Badge, Notification
from .utils.levels import get_user_level
from django.utils.timezone import now
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def check_badges(sender, instance, created, **kwargs):
    user = instance.user

    # Badge : 1re entrée
    if created and user.entries.count() == 1:
        badge, created_badge = Badge.objects.get_or_create(
            user=user,
            name="Première entrée",
            defaults={
                "description": "Bravo pour ta première entrée 🎉",
                "icon": "🌱"
            }
        )
        if created_badge:
            Notification.objects.create(
                user=user,
                message=f"🎉 Nouveau badge : {badge.name} !"
            )
            logger.info(f"[BADGE] {user.username} a débloqué : {badge.name}")

    # Badge : 7 jours d'activité
    last_7 = user.entries.filter(created_at__gte=now() - timedelta(days=7)).count()
    if last_7 >= 7:
        badge, created_badge = Badge.objects.get_or_create(
            user=user,
            name="7 jours d'activité",
            defaults={
                "description": "1 semaine d'activité, continue comme ça 🚀",
                "icon": "🔥"
            }
        )
        if created_badge:
            Notification.objects.create(
                user=user,
                message=f"🔥 Nouveau badge : {badge.name} !"
            )
            logger.info(f"[BADGE] {user.username} a débloqué : {badge.name}")

    # Badge de niveau
    level = get_user_level(user.entries.count())
    badge_name = f"Niveau {level}"
    if level > 0 and not user.badges.filter(name=badge_name).exists():
        badge = Badge.objects.create(
            user=user,
            name=badge_name,
            description=f"Tu as atteint le niveau {level} 💪",
            icon="🏆"
        )
        Notification.objects.create(
            user=user,
            message=f"🏆 Félicitations, tu as atteint le {badge.name} !"
        )
        logger.info(f"[BADGE] {user.username} a débloqué : {badge.name}")
