from datetime import timedelta
import logging
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from collections import defaultdict
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete

from django.conf import settings
User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)

class WeeklyStat(models.Model):
    """
    Modèle pour stocker les statistiques hebdomadaires d'un utilisateur.
    Agrège les données d'entrées pour fournir des insights sur une période d'une semaine.
    Permet de suivre les tendances et l'évolution sur une échelle de temps plus large que les stats quotidiennes.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_stats")
    week_start = models.DateField(help_text="Premier jour de la semaine (lundi)")
    entries_count = models.PositiveIntegerField(help_text="Nombre total d'entrées pour la semaine")
    mood_average = models.FloatField(null=True, blank=True, help_text="Moyenne des humeurs de la semaine")
    categories = models.JSONField(default=dict, blank=True, help_text="Répartition des entrées par catégorie")

    class Meta:
        unique_together = ('user', 'week_start')
        verbose_name = "Statistique hebdomadaire"
        verbose_name_plural = "Statistiques hebdomadaires"
        ordering = ['-week_start']
        indexes = [
            models.Index(fields=['user', 'week_start']),
            models.Index(fields=['mood_average']),
        ]

    def __str__(self):
        return f"{self.user.username} - semaine du {self.week_start}"

    def __repr__(self):
        return f"<WeeklyStat user={self.user.username} week_start={self.week_start}>"

    def get_absolute_url(self):
        return f"/api/stats/weekly/{self.week_start}/"

    def clean(self):
        if self.mood_average and not (0 <= self.mood_average <= 10):
            raise ValidationError("La moyenne d'humeur doit être comprise entre 0 et 10.")

    def week_end(self):
        """
        Calcule le dernier jour de la semaine.
        """
        return self.week_start + timedelta(days=6)

    def week_number(self):
        """
        Retourne le numéro de semaine dans l'année.
        """
        return self.week_start.isocalendar()[1]

    def top_category(self):
        """
        Retourne la catégorie la plus fréquente.
        """
        if not self.categories:
            return None
        return max(self.categories.items(), key=lambda x: x[1])[0]

    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Génère ou met à jour les statistiques hebdomadaires pour un utilisateur.
        """
        if not reference_date:
            reference_date = now().date()

        week_start = reference_date - timedelta(days=reference_date.weekday())
        week_end = week_start + timedelta(days=6)

        entries = user.entries.filter(created_at__date__range=(week_start, week_end))
        entries_count = entries.count()
        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1

        stat, created = cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        return stat

    @classmethod
    def get_trends(cls, user, weeks=10):
        """
        Récupère l'évolution des statistiques sur plusieurs semaines.
        """
        current_week_start = now().date() - timedelta(days=now().date().weekday())
        start_date = current_week_start - timedelta(weeks=weeks)
        
        stats = cls.objects.filter(user=user, week_start__gte=start_date).order_by('week_start')
        
        weeks_labels, entries_data, mood_data = [], [], []
        
        for i in range(weeks + 1):
            week_date = start_date + timedelta(weeks=i)
            week_label = f"{week_date.year}-W{week_date.isocalendar()[1]}"
            weeks_labels.append(week_label)

            stat = next((s for s in stats if s.week_start == week_date), None)
            entries_data.append(stat.entries_count if stat else 0)
            mood_data.append(stat.mood_average if stat else None)
        
        return {
            'weeks': weeks_labels,
            'entries': entries_data,
            'mood': mood_data
        }

@receiver(post_save, sender=WeeklyStat)
def log_weekly_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques hebdomadaires.
    """
    if created:
        logger.info(f"Statistiques hebdomadaires créées pour {instance.user.username} - Semaine du {instance.week_start}")


@receiver(post_delete, sender=WeeklyStat)
def log_weekly_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques hebdomadaires.
    """
    logger.info(f"Statistiques hebdomadaires supprimées pour {instance.user.username} - Semaine du {instance.week_start}")



class DailyStat(models.Model):
    """
    Modèle pour stocker les statistiques journalières d'un utilisateur.
    Agrège les données d'entrées de journal pour une analyse et un affichage efficaces.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_stats")
    date = models.DateField(help_text="La date des statistiques")
    entries_count = models.PositiveIntegerField(default=0, help_text="Nombre total d'entrées pour la journée")
    mood_average = models.FloatField(null=True, blank=True, help_text="Moyenne des humeurs de la journée")
    categories = models.JSONField(default=dict, blank=True, help_text="Répartition des entrées par catégorie")

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = "Statistique journalière"
        verbose_name_plural = "Statistiques journalières"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def __repr__(self):
        return f"<DailyStat user={self.user.username} date={self.date}>"

    def get_absolute_url(self):
        return f"/api/stats/daily/{self.date}/"

    def clean(self):
        if self.mood_average and not (0 <= self.mood_average <= 10):
            raise ValidationError("La moyenne d'humeur doit être comprise entre 0 et 10.")

    def day_of_week(self):
        """
        Retourne le jour de la semaine en format lisible.
        """
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return days[self.date.weekday()]

    def is_weekend(self):
        """
        Vérifie si la date tombe un weekend.
        """
        return self.date.weekday() >= 5

    @classmethod
    def generate_for_user(cls, user, date=None):
        """
        Génère ou met à jour les statistiques journalières pour une date donnée.
        """
        if not date:
            date = now().date()

        entries = user.entries.filter(created_at__date=date)
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        cat_stats = defaultdict(int)
        for entry in entries:
            cat_stats[entry.category] += 1

        stat, created = cls.objects.update_or_create(
            user=user,
            date=date,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(cat_stats),
            }
        )
        return stat

    @classmethod
    def get_calendar_data(cls, user, month=None, year=None):
        """
        Génère des données pour une visualisation de type calendrier heatmap.
        """
        from datetime import datetime
        if year is None:
            year = now().year
        
        date_filter = {'user': user, 'date__year': year}
        if month is not None:
            date_filter['date__month'] = month

        stats = cls.objects.filter(**date_filter).order_by('date')

        max_count = max([stat.entries_count for stat in stats], default=1)

        result = []
        for stat in stats:
            intensity = stat.entries_count / max_count if max_count > 0 else 0
            result.append({
                'date': stat.date.isoformat(),
                'count': stat.entries_count,
                'mood': stat.mood_average,
                'intensity': round(intensity, 2)
            })
        return result

@receiver(post_save, sender=DailyStat)
def log_daily_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques journalières.
    """
    if created:
        logger.info(f"Statistiques journalières créées pour {instance.user.username} - {instance.date}")


@receiver(post_delete, sender=DailyStat)
def log_daily_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques journalières.
    """
    logger.info(f"Statistiques journalières supprimées pour {instance.user.username} - {instance.date}")

class MonthlyStat(models.Model):
    """
    Modèle pour stocker les statistiques mensuelles d'un utilisateur.
    Permet de suivre les tendances et l'évolution sur une période d'un mois.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="monthly_stats")
    month_start = models.DateField(help_text="Premier jour du mois")
    entries_count = models.PositiveIntegerField(help_text="Nombre total d'entrées pour le mois")
    mood_average = models.FloatField(null=True, blank=True, help_text="Moyenne des humeurs du mois")
    categories = models.JSONField(default=dict, blank=True, help_text="Répartition des entrées par catégorie")

    class Meta:
        unique_together = ('user', 'month_start')
        ordering = ['-month_start']
        verbose_name = "Statistique mensuelle"
        verbose_name_plural = "Statistiques mensuelles"

    def __str__(self):
        return f"{self.user.username} - mois de {self.month_start.strftime('%B %Y')}"

    def __repr__(self):
        return f"<MonthlyStat user={self.user.username} month_start={self.month_start}>"

    def get_absolute_url(self):
        return f"/api/stats/monthly/{self.month_start}/"

    def clean(self):
        if self.mood_average and not (0 <= self.mood_average <= 10):
            raise ValidationError("La moyenne d'humeur doit être comprise entre 0 et 10.")

    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Génère ou met à jour les statistiques mensuelles pour un utilisateur.
        """
        if not reference_date:
            reference_date = now().date()

        month_start = reference_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        entries = user.entries.filter(created_at__date__range=(month_start, month_end))
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1

        stat, created = cls.objects.update_or_create(
            user=user,
            month_start=month_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        return stat


class AnnualStat(models.Model):
    """
    Modèle pour stocker les statistiques annuelles d'un utilisateur.
    Permet de suivre les tendances et l'évolution sur une période d'une année.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="annual_stats")
    year_start = models.DateField(help_text="Premier jour de l'année")
    entries_count = models.PositiveIntegerField(help_text="Nombre total d'entrées pour l'année")
    mood_average = models.FloatField(null=True, blank=True, help_text="Moyenne des humeurs de l'année")
    categories = models.JSONField(default=dict, blank=True, help_text="Répartition des entrées par catégorie")

    class Meta:
        unique_together = ('user', 'year_start')
        ordering = ['-year_start']
        verbose_name = "Statistique annuelle"
        verbose_name_plural = "Statistiques annuelles"

    def __str__(self):
        return f"{self.user.username} - année {self.year_start.year}"

    def __repr__(self):
        return f"<AnnualStat user={self.user.username} year_start={self.year_start}>"

    def get_absolute_url(self):
        return f"/api/stats/annual/{self.year_start.year}/"

    def clean(self):
        if self.mood_average and not (0 <= self.mood_average <= 10):
            raise ValidationError("La moyenne d'humeur doit être comprise entre 0 et 10.")

    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Génère ou met à jour les statistiques annuelles pour un utilisateur.
        """
        if not reference_date:
            reference_date = now().date()

        year_start = reference_date.replace(month=1, day=1)
        year_end = year_start.replace(month=12, day=31)

        entries = user.entries.filter(created_at__date__range=(year_start, year_end))
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1

        stat, created = cls.objects.update_or_create(
            user=user,
            year_start=year_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        return stat
