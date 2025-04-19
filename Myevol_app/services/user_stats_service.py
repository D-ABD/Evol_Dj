from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from collections import defaultdict
from django.conf import settings
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from ..services.badge_service import update_user_badges
from ..services.preferences_service import create_preferences_for_user
from ..services.streak_service import update_user_streak


def mood_average(self, days=7, reference_date=None):
        """
        Calcule la moyenne d'humeur sur les X derniers jours.
        
        Args:
            days (int): Nombre de jours à considérer pour le calcul
            reference_date (date, optional): Date de référence (maintenant par défaut)
            
        Returns:
            float: Moyenne d'humeur arrondie à 1 décimale, ou None si aucune entrée
        """
        if reference_date is None:
            reference_date = now()
            
        entries = self.entries.filter(created_at__gte=reference_date - timedelta(days=days))
        avg = entries.aggregate(avg=Avg('mood'))['avg']
        return round(avg, 1) if avg is not None else None

def current_streak(self, reference_date=None):
        """
        Calcule la série actuelle de jours consécutifs avec au moins une entrée.
        Vérifie jusqu'à 365 jours en arrière.
        
        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre de jours consécutifs avec une entrée
        """
        if reference_date is None:
            reference_date = now().date()
            
        streak = 0
        for i in range(0, 365):
            day = reference_date - timedelta(days=i)
            if self.entries.filter(created_at__date=day).exists():
                streak += 1
            else:
                break
        return streak

def has_entries_every_day(self, last_n_days=7, reference_date=None):
        """
        Vérifie si l'utilisateur a fait au moins une entrée chaque jour
        pendant les n derniers jours.
        
        Args:
            last_n_days (int): Nombre de jours à vérifier
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            bool: True si l'utilisateur a une entrée pour chaque jour de la période
        """
        if reference_date is None:
            reference_date = now().date()
            
        start_date = reference_date - timedelta(days=last_n_days - 1)
        days_with_entry = self.entries.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=reference_date
        ).values_list("created_at__date", flat=True).distinct()
        
        expected_days = {start_date + timedelta(days=i) for i in range(last_n_days)}
        return len(expected_days) == len(set(days_with_entry))

@cached_property
def level(self):
        """
        Calcule le niveau de l'utilisateur basé sur le nombre d'entrées.
        Le niveau augmente tous les 10 entrées.
        
        Returns:
            int: Niveau actuel de l'utilisateur
        """
        return (self.total_entries() // 10) + 1

def total_entries(self):
        """
        Retourne le nombre total d'entrées de journal pour cet utilisateur.
        Utilise la relation inverse 'entries' définie dans JournalEntry.
        """
        return self.entries.count()




def all_objectives_achieved(self):
        """
        Vérifie si tous les objectifs de l'utilisateur sont achevés.
        
        Returns:
            bool: True si tous les objectifs sont achevés, False sinon
        """
        return not self.objectives.filter(done=False).exists()

def entries_today(self, reference_date=None):
        """
        Compte le nombre d'entrées faites aujourd'hui.
        
        Args:
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre d'entrées d'aujourd'hui
        """
        if reference_date is None:
            reference_date = now().date()
            
        return self.entries.filter(created_at__date=reference_date).count()
    
def entries_by_category(self, days=None):
        """
        Calcule la distribution des entrées par catégorie.
        
        Args:
            days (int, optional): Limite aux N derniers jours si spécifié
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
        """
        entries = self.entries.all()
        if days:
            entries = entries.filter(created_at__gte=now() - timedelta(days=days))
            
        return dict(entries.values('category').annotate(count=Count('id')).values_list('category', 'count'))

def entries_last_n_days(self, n=7):
        """
        Retourne les entrées des n derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            QuerySet: Entrées des n derniers jours
        """
        since = now() - timedelta(days=n)
        return self.entries.filter(created_at__gte=since)

def entries_per_day(self, n=7):
        """
        Calcule le nombre d'entrées par jour sur les n derniers jours.
        Utilise les fonctions d'agrégation de Django pour optimiser la requête.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec dates comme clés et nombre d'entrées comme valeurs
        """
        from django.db.models.functions import TruncDate
        
        since = now() - timedelta(days=n)
        entries = self.entries.filter(created_at__gte=since)
        data = entries.annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day')
        return {d['day']: d['count'] for d in data}

def mood_trend(self, n=7):
        """
        Calcule la moyenne d'humeur par jour sur les n derniers jours.
        Utilise les fonctions d'agrégation de Django pour optimiser la requête.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec dates comme clés et moyennes d'humeur comme valeurs
        """
        from django.db.models.functions import TruncDate
        
        since = now() - timedelta(days=n)
        entries = self.entries.filter(created_at__gte=since)
        data = entries.annotate(day=TruncDate('created_at')).values('day').annotate(moyenne=Avg('mood')).order_by('day')
        return {d['day']: round(d['moyenne'], 1) for d in data}

def days_with_entries(self, n=30):
        """
        Retourne la liste des jours avec au moins une entrée dans les n derniers jours.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            list: Liste des dates avec au moins une entrée
        """
        since = now().date() - timedelta(days=n)
        return list(
            self.entries.filter(created_at__date__gte=since)
            .values_list("created_at__date", flat=True)
            .distinct()
        )

def entries_per_category_last_n_days(self, n=7):
        """
        Calcule la distribution des entrées par catégorie pour les n derniers jours.
        Optimisé avec agrégation Django.
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
        """
        since = now() - timedelta(days=n)
        return dict(
            self.entries.filter(created_at__gte=since)
            .values('category')
            .annotate(count=Count('id'))
            .values_list('category', 'count')
        )
def update_badges(self):
        update_user_badges(self)

def update_streaks(self):
        update_user_streak(self)

def create_default_preferences(self):
        return create_preferences_for_user(self)


