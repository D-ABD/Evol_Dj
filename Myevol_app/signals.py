from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
import logging
from django.db.models.signals import post_delete

from .models import JournalEntry, Badge, Notification, DailyStat, User, UserPreference
from .utils.levels import get_user_level  # Cette fonction calcule le niveau d'un utilisateur

# Configuration du logger pour tracer les événements importants
logger = logging.getLogger(__name__)


# 🏅 Fonction générique pour créer un badge, une notification et un log
def award_badge(user, name, description, icon):
    """
    Fonction utilitaire pour attribuer un badge à un utilisateur.
    Crée également une notification pour informer l'utilisateur.
    
    Args:
        user: L'utilisateur à qui attribuer le badge
        name: Nom du badge
        description: Description du badge
        icon: Icône représentant le badge (emoji)
        
    Returns:
        bool: True si le badge a été nouvellement créé, False s'il existait déjà
    """
    badge, created = Badge.objects.get_or_create(
        user=user,
        name=name,
        defaults={
            "description": description,
            "icon": icon,
        }
    )
    # Si le badge vient d'être créé, on notifie l'utilisateur
    if created:
        Notification.objects.create(
            user=user,
            message=f"{icon} Nouveau badge : {name} !"
        )
        # Journalisation de l'événement pour le suivi administratif
        logger.info(f"[BADGE] {user.username} a débloqué : {name}")
    return created


@receiver(post_save, sender=JournalEntry)
def check_badges_and_stats(sender, instance, created, **kwargs):
    """
    Signal déclenché à la sauvegarde d'une JournalEntry.
    Gère deux aspects principaux :
    1. Mise à jour des statistiques journalières
    2. Attribution des badges en fonction des accomplissements
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (JournalEntry)
        instance: Instance du modèle qui a été sauvegardée
        created: Booléen indiquant si l'instance vient d'être créée (True) ou mise à jour (False)
        **kwargs: Arguments supplémentaires du signal
    """
    user = instance.user

    # 🔄 Met à jour ou crée les statistiques journalières pour la date de l'entrée
    DailyStat.generate_for_user(user=user, date=instance.created_at.date())

    # ⚠️ On ne vérifie les badges que si c'est une nouvelle entrée
    # Évite de dupliquer les badges lors des mises à jour d'entrées existantes
    if not created:
        return

    # Récupère le nombre total d'entrées de l'utilisateur
    total = user.entries.count()

    # ✅ Badge : première entrée
    # Décerné lorsque l'utilisateur crée sa toute première entrée
    if total == 1:
        award_badge(
            user,
            name="Première entrée",
            description="Bravo pour ta première entrée 🎉",
            icon="🌱"
        )

    # ✅ Badge : 7 jours d'activité consécutifs
    # Vérifie si l'utilisateur a au moins une entrée pour chacun des 7 derniers jours
    streak_days = 7
    today = now().date()
    # Vérifie l'existence d'au moins une entrée pour chaque jour de la période
    has_streak = all(
        user.entries.filter(created_at__date=today - timedelta(days=i)).exists()
        for i in range(streak_days)
    )
    if has_streak:
        award_badge(
            user,
            name="7 jours d'activité",
            description="1 semaine d'activité, continue comme ça 🚀",
            icon="🔥"
        )

    # ✅ Badge : Niveau
    # Attribue un badge lorsque l'utilisateur atteint un nouveau niveau
    # La fonction get_user_level détermine le niveau en fonction du nombre total d'entrées
    level = get_user_level(total)
    if level > 0:
        badge_name = f"Niveau {level}"
        # Vérifie si l'utilisateur n'a pas déjà ce badge
        if not user.badges.filter(name=badge_name).exists():
            award_badge(
                user,
                name=badge_name,
                description=f"Tu as atteint le niveau {level} 💪",
                icon="🏆"
            )


@receiver(post_delete, sender=JournalEntry)
def update_stats_on_delete(sender, instance, **kwargs):
    """
    Signal déclenché à la suppression d'une JournalEntry.
    Assure que les statistiques journalières restent cohérentes après la suppression d'une entrée.
    
    Deux cas possibles :
    1. S'il reste des entrées pour cette date : recalcule les statistiques
    2. S'il n'y a plus d'entrées pour cette date : supprime les statistiques
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (JournalEntry)
        instance: Instance du modèle qui a été supprimée
        **kwargs: Arguments supplémentaires du signal
    """
    user = instance.user
    date = instance.created_at.date()

    # 🔄 Vérifie s'il reste des entrées pour cette date
    entries = user.entries.filter(created_at__date=date)
    if entries.exists():
        # S'il reste des entrées, recalcule les statistiques
        DailyStat.generate_for_user(user=user, date=date)
    else:
        # S'il n'y a plus d'entrées, supprime les statistiques pour cette date
        DailyStat.objects.filter(user=user, date=date).delete()
        # Journalise l'événement pour le suivi administratif
        logger.info(f"[STATS] Statistiques supprimées pour {user.username} - {date}")

@receiver(post_save, sender=Notification)
def mark_other_notifications_as_read(sender, instance, created, **kwargs):
    """
    Quand une notification est créée, marque les autres comme lues.
    """
    if created:
        # Marquer toutes les autres notifications de l'utilisateur comme lues
        Notification.objects.filter(
            user=instance.user,
            is_read=False
        ).exclude(id=instance.id).update(is_read=True)

@receiver(post_save, sender=Notification)
def limit_notifications(sender, instance, **kwargs):
    """
    Signal déclenché après la sauvegarde d'une notification.
    Limite le nombre maximum de notifications par utilisateur pour éviter une surcharge de la base de données.
    
    Fonctionnement :
    - Récupère toutes les notifications de l'utilisateur, triées par date (plus récentes d'abord)
    - Si le nombre dépasse la limite, supprime les plus anciennes
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (Notification)
        instance: Instance de notification qui vient d'être sauvegardée
        **kwargs: Arguments supplémentaires du signal
    """
    max_notifs = 100  # Nombre maximum de notifications à conserver par utilisateur
    
    # Récupère les notifications de l'utilisateur, triées des plus récentes aux plus anciennes
    qs = Notification.objects.filter(user=instance.user).order_by('-created_at')
    
    # Si le nombre dépasse la limite
    if qs.count() > max_notifs:
        # Sélectionne les notifications à supprimer (les plus anciennes au-delà de la limite)
        to_delete = qs[max_notifs:]
        # Supprime ces notifications
        to_delete.delete()
        

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Signal déclenché après la création d'un utilisateur.
    Crée automatiquement un objet de préférences par défaut pour chaque nouvel utilisateur.
    
    Cette fonction garantit que chaque utilisateur dispose immédiatement de préférences configurées
    avec les valeurs par défaut, ce qui simplifie le reste du code de l'application.
    
    Args:
        sender: Classe du modèle qui a envoyé le signal (User)
        instance: L'utilisateur qui vient d'être créé ou modifié
        created: Booléen indiquant si l'utilisateur vient d'être créé (True) ou mis à jour (False)
        **kwargs: Arguments supplémentaires du signal
    """
    # Vérifie s'il s'agit d'un nouvel utilisateur
    if created:
        # Crée un objet de préférences par défaut pour cet utilisateur
        UserPreference.objects.create(user=instance)