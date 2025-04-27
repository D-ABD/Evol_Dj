from datetime import timedelta
import logging
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.conf import settings


User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)


class WeeklyStat(models.Model):
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
        return self.week_start + timedelta(days=6)

    def week_number(self):
        return self.week_start.isocalendar()[1]

    def top_category(self):
        if not self.categories:
            return None
        return max(self.categories.items(), key=lambda x: x[1])[0]

    @classmethod
    def generate_for_user(cls, user, date=None):
        from ..services.stats_service import compute_stats_for_period
        date = date or now().date()
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(days=6)
        stats = compute_stats_for_period(user, start, end)

        stat, created = cls.objects.update_or_create(
            user=user,
            week_start=start,
            defaults=stats
        )
        return stat


class DailyStat(models.Model):
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
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return days[self.date.weekday()]

    def is_weekend(self):
        return self.date.weekday() >= 5

    @classmethod
    def generate_for_user(cls, user, date=None):
        from ..services.stats_service import compute_stats_for_period
        date = date or now().date()
        stats = compute_stats_for_period(user, date, date)

        stat, created = cls.objects.update_or_create(
            user=user,
            date=date,
            defaults=stats
        )
        return stat


class MonthlyStat(models.Model):
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
        from ..services.stats_service import compute_stats_for_period
        reference_date = reference_date or now().date()
        start = reference_date.replace(day=1)
        end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        stats = compute_stats_for_period(user, start, end)

        stat, created = cls.objects.update_or_create(
            user=user,
            month_start=start,
            defaults=stats
        )
        return stat


class AnnualStat(models.Model):
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
        from ..services.stats_service import compute_stats_for_period
        reference_date = reference_date or now().date()
        start = reference_date.replace(month=1, day=1)
        end = start.replace(month=12, day=31)
        stats = compute_stats_for_period(user, start, end)

        stat, created = cls.objects.update_or_create(
            user=user,
            year_start=start,
            defaults=stats
        )
        return stat
