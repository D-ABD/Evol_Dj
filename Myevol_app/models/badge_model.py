# MyEvol_app/models/badge_model.py

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings

from ..services.levels_services import get_user_level, get_user_progress

User = settings.AUTH_USER_MODEL

class Badge(models.Model):
    """
    🏅 Badge réellement attribué à un utilisateur.
    
    Les badges sont attribués à un utilisateur lorsqu’il atteint une certaine condition
    définie dans un BadgeTemplate. Ils servent à motiver l’utilisateur et à gamifier l’expérience.

    API Endpoints recommandés :
    - GET /api/badges/ : Liste les badges de l’utilisateur courant
    - GET /api/users/{id}/badges/ : Liste les badges d’un utilisateur donné
    - GET /api/badges/recent/ : Récupère les badges récents (7 derniers jours)

    Champs calculés à exposer dans l’API :
    - was_earned_today
    - is_recent
    - days_since_earned
    """

    name = models.CharField(max_length=100, help_text="Nom du badge affiché à l’utilisateur")
    description = models.TextField(help_text="Texte explicatif du badge (accomplissement)")
    icon = models.CharField(max_length=100, help_text="Emoji ou nom d’icône visuelle pour le badge")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="badges",
        help_text="Utilisateur à qui ce badge a été attribué"
    )
    date_obtenue = models.DateField(
        auto_now_add=True,
        help_text="Date à laquelle le badge a été obtenu"
    )
    level = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Niveau associé au badge (optionnel)"
    )

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['-date_obtenue']
        unique_together = ('name', 'user')

    def __str__(self):
        """Retourne une représentation lisible du badge."""
        return f"{self.name} ({self.user.username})"

    def __repr__(self):
        """Retourne une représentation détaillée de l'objet Badge."""
        return f"<Badge id={self.id} name='{self.name}' user='{self.user.username}'>"

    def get_absolute_url(self):
        """Retourne l’URL vers la vue de détail du badge."""
        return reverse("badge-detail", kwargs={"pk": self.pk})

    def was_earned_today(self, reference_date=None):
        """Retourne True si le badge a été obtenu aujourd’hui."""
        reference_date = reference_date or now().date()
        return self.date_obtenue == reference_date
    
class BadgeTemplate(models.Model):
    """
    🧩 Modèle de badge définissant les critères pour l’attribution.
    
    Chaque template décrit un badge disponible dans le système, ainsi que les conditions
    pour l’obtenir. Lorsqu’un utilisateur remplit les conditions, un `Badge` est créé
    automatiquement en se basant sur ce modèle.

    API Endpoints recommandés :
    - GET /api/badges/templates/ : Liste tous les modèles de badges
    - GET /api/badges/templates/{id}/ : Détail d’un modèle
    - GET /api/badges/templates/{id}/progress/ : Progression vers ce badge
    - POST /api/badges/sync/ : Vérifie quels badges peuvent être débloqués

    Champs utiles pour l’API :
    - progress (dict)
    - can_unlock (booléen)
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nom unique du badge (ex: 'Régulier', 'Niveau 3')"
    )
    description = models.TextField(
        help_text="Description du badge visible dans l’interface"
    )
    icon = models.CharField(
        max_length=100,
        help_text="Emoji ou identifiant visuel de l’icône"
    )
    condition = models.CharField(
        max_length=255,
        help_text="Condition textuelle d’obtention du badge"
    )
    level = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Niveau cible (optionnel, utile pour les badges de type 'Niveau X')"
    )
    animation_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL d’une animation Lottie ou GIF"
    )
    color_theme = models.CharField(
        default="#FFD700",
        max_length=20,
        help_text="Couleur HEX du thème visuel du badge"
    )

    class Meta:
        verbose_name = "Modèle de badge"
        verbose_name_plural = "Modèles de badges"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<BadgeTemplate id={self.id} name='{self.name}'>"

    def get_absolute_url(self):
        """Retourne l’URL vers la vue de détail du modèle de badge."""
        return reverse("badge-template-detail", kwargs={"pk": self.pk})

    def extract_level_number(self):
        """Essaie d’extraire un niveau à partir du nom ('Niveau 3')."""
        try:
            if self.name.lower().startswith("niveau"):
                return int(self.name.split(" ")[1])
        except (ValueError, IndexError):
            pass
        return None

    def check_unlock(self, user):
        """Vérifie si l'utilisateur peut débloquer ce badge."""
        total = user.total_entries()
        mood_avg = user.mood_average(7)

        conditions = {
            "Première entrée": total >= 1,
            "Régulier": user.has_entries_every_day(5),
            "Discipline": user.has_entries_every_day(10),
            "Résilience": user.has_entries_every_day(15),
            "Légende du Journal": user.has_entries_every_day(30),
            "Ambassadeur d'humeur": mood_avg and mood_avg >= 9,
            "Productivité": user.entries_today() >= 3,
            "Objectif rempli !": user.all_objectives_achieved(),
            "Persévérance": total >= 100,
        }

        if self.name in conditions:
            return conditions[self.name]

        level_number = self.extract_level_number()
        if level_number:
            return get_user_level(total) >= level_number

        return False

    def get_progress(self, user):
        """Calcule la progression d’un utilisateur vers ce badge."""
        total = user.total_entries()
        unlocked = user.badges.filter(name=self.name).exists()

        if unlocked:
            level_number = self.extract_level_number()
            if level_number:
                progress_data = get_user_progress(total)
                return {
                    "percent": 100,
                    "unlocked": True,
                    "current": total,
                    "target": progress_data.get("next_threshold", total)
                }
            return {"percent": 100, "unlocked": True, "current": total, "target": total}

        # Cas spécifiques
        if self.name == "Première entrée":
            return {
                "percent": 100 if total >= 1 else 0,
                "unlocked": total >= 1,
                "current": min(total, 1),
                "target": 1
            }

        level_number = self.extract_level_number()
        if level_number:
            progress_data = get_user_progress(total)
            return {
                "percent": 100 if progress_data["level"] >= level_number else progress_data["progress"],
                "unlocked": progress_data["level"] >= level_number,
                "current": total,
                "target": progress_data["next_threshold"]
            }

        is_unlocked = self.check_unlock(user)
        return {
            "percent": 100 if is_unlocked else 0,
            "unlocked": is_unlocked,
            "current": total,
            "target": 1
        }
