from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from collections import defaultdict
from django.db.models import Avg

from django.conf import settings
User = settings.AUTH_USER_MODEL


class WeeklyStat(models.Model):
    """
    Modèle pour stocker les statistiques hebdomadaires d'un utilisateur.
    Agrège les données d'entrées pour fournir des insights sur une période d'une semaine.
    Permet de suivre les tendances et l'évolution sur une échelle de temps plus large que les stats quotidiennes.
    
    API Endpoints suggérés:
    - GET /api/stats/weekly/ - Liste des statistiques hebdomadaires de l'utilisateur
    - GET /api/stats/weekly/current/ - Statistiques de la semaine en cours
    - GET /api/stats/weekly/{date}/ - Statistiques de la semaine contenant la date spécifiée
    - GET /api/stats/weekly/trends/ - Évolution des statistiques sur plusieurs semaines
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "week_start": "2025-04-14",
        "week_end": "2025-04-20",  // Champ calculé
        "entries_count": 12,
        "mood_average": 7.5,
        "categories": {
            "Travail": 5,
            "Sport": 3,
            "Famille": 4
        },
        "top_category": "Travail",  // Champ calculé
        "week_number": 16           // Champ calculé
    }
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_stats")
    week_start = models.DateField()  # Premier jour de la semaine (lundi)
    entries_count = models.PositiveIntegerField()  # Nombre total d'entrées
    mood_average = models.FloatField(null=True, blank=True)  # Moyenne d'humeur
    categories = models.JSONField(default=dict, blank=True)  # Répartition par catégorie

    class Meta:
        unique_together = ('user', 'week_start')
        ordering = ['-week_start']
        verbose_name = "Statistique hebdomadaire"
        verbose_name_plural = "Statistiques hebdomadaires"
        
        """
        Filtres API recommandés:
        - week_start (date, gte, lte)
        - entries_count (gte, lte)
        - mood_average (gte, lte)
        """

    def __str__(self):
        return f"{self.user.username} - semaine du {self.week_start}"
        
    def week_end(self):
        """
        Calcule le dernier jour de la semaine.
        
        Returns:
            date: Date du dimanche de cette semaine
            
        Utilisation dans l'API:
            Utile comme champ calculé pour l'affichage de la période complète.
        """
        return self.week_start + timedelta(days=6)
        
    def week_number(self):
        """
        Retourne le numéro de semaine dans l'année.
        
        Returns:
            int: Numéro de la semaine (1-53)
            
        Utilisation dans l'API:
            Pratique pour l'affichage et le regroupement des données par semaine.
        """
        return self.week_start.isocalendar()[1]
        
    def top_category(self):
        """
        Détermine la catégorie la plus fréquente de la semaine.
        
        Returns:
            str: Nom de la catégorie la plus fréquente, ou None si aucune entrée
            
        Utilisation dans l'API:
            Utile pour l'affichage de résumés ou de badges dans l'interface.
        """
        if not self.categories:
            return None
            
        return max(self.categories.items(), key=lambda x: x[1])[0]

    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Génère ou met à jour les statistiques hebdomadaires pour un utilisateur.

        Args:
            user: L'utilisateur concerné
            reference_date: Date de référence (par défaut aujourd'hui)

        Returns:
            (obj, created): Statistique mise à jour ou créée
            
        Utilisation dans l'API:
            Cette méthode devrait être appelée en arrière-plan après chaque
            ajout/modification/suppression d'entrée, ou via une tâche périodique.
            
        Exemple d'utilisation dans une vue:
            @action(detail=False, methods=['post'])
            def refresh(self, request):
                date_param = request.data.get('date')
                date = parse_date(date_param) if date_param else None
                stat, created = WeeklyStat.generate_for_user(request.user, date)
                return Response(self.get_serializer(stat).data)
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

        return cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        
    @classmethod
    def get_trends(cls, user, weeks=10):
        """
        Récupère l'évolution des statistiques sur plusieurs semaines.
        
        Args:
            user: L'utilisateur concerné
            weeks: Nombre de semaines à inclure
            
        Returns:
            dict: Données de tendances structurées pour visualisation
                {
                    'weeks': ['2025-W15', '2025-W16', ...],
                    'entries': [8, 12, ...],
                    'mood': [6.5, 7.2, ...]
                }
                
        Utilisation dans l'API:
            Parfait pour générer des graphiques d'évolution.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def trends(self, request):
                weeks = int(request.query_params.get('weeks', 10))
                return Response(WeeklyStat.get_trends(request.user, weeks))
        """
        # Calculer le début de la période
        current_week_start = now().date() - timedelta(days=now().date().weekday())
        start_date = current_week_start - timedelta(weeks=weeks)
        
        # Récupérer les statistiques hebdomadaires existantes
        stats = cls.objects.filter(
            user=user,
            week_start__gte=start_date
        ).order_by('week_start')
        
        # Préparer les données de tendances
        weeks_labels = []
        entries_data = []
        mood_data = []
        
        # Remplir les semaines manquantes
        for i in range(weeks + 1):
            week_date = start_date + timedelta(weeks=i)
            week_label = f"{week_date.year}-W{week_date.isocalendar()[1]}"
            weeks_labels.append(week_label)
            
            # Chercher la stat correspondante
            stat = next((s for s in stats if s.week_start == week_date), None)
            
            entries_data.append(stat.entries_count if stat else 0)
            mood_data.append(stat.mood_average if stat and stat.mood_average else None)
        
        return {
            'weeks': weeks_labels,
            'entries': entries_data,
            'mood': mood_data
        }


class DailyStat(models.Model):
    """
    Modèle pour stocker les statistiques journalières d'un utilisateur.
    Agrège les données d'entrées de journal pour une analyse et un affichage efficaces.
    
    API Endpoints suggérés:
    - GET /api/stats/daily/ - Liste des statistiques journalières de l'utilisateur
    - GET /api/stats/daily/today/ - Statistiques du jour
    - GET /api/stats/daily/{date}/ - Statistiques d'une date spécifique
    - GET /api/stats/daily/range/?start={date}&end={date} - Statistiques sur une période
    - GET /api/stats/daily/calendar/ - Données pour la vue calendrier (heatmap)
    
    Exemple de sérialisation JSON:
    {
        "id": 123,
        "date": "2025-04-19",
        "entries_count": 3,
        "mood_average": 8.0,
        "categories": {
            "Travail": 1,
            "Sport": 1,
            "Loisirs": 1
        },
        "day_of_week": "Samedi",  // Champ calculé
        "is_weekend": true        // Champ calculé
    }
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_stats")
    date = models.DateField()
    entries_count = models.PositiveIntegerField(default=0)
    mood_average = models.FloatField(null=True, blank=True)
    categories = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
        verbose_name = "Statistique journalière"
        verbose_name_plural = "Statistiques journalières"
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
        
        """
        Filtres API recommandés:
        - date (exact, gte, lte, range)
        - entries_count (gte, lte)
        - mood_average (gte, lte)
        - is_weekend (boolean calculé)
        """

    def __str__(self):
        return f"{self.user.username} - {self.date}"
        
    def day_of_week(self):
        """
        Retourne le jour de la semaine en format lisible.
        
        Returns:
            str: Nom du jour de la semaine (Lundi, Mardi, etc.)
            
        Utilisation dans l'API:
            Utile pour l'affichage dans l'interface utilisateur.
        """
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return days[self.date.weekday()]
        
    def is_weekend(self):
        """
        Vérifie si la date tombe un weekend.
        
        Returns:
            bool: True si samedi ou dimanche
            
        Utilisation dans l'API:
            Permet de filtrer ou d'afficher différemment les weekends.
        """
        return self.date.weekday() >= 5  # 5=Samedi, 6=Dimanche

    @classmethod
    def generate_for_user(cls, user, date=None):
        """
        Génère ou met à jour les statistiques journalières pour une date donnée.

        Args:
            user: L'utilisateur concerné
            date: Date à analyser (par défaut aujourd'hui)

        Returns:
            DailyStat: Statistique mise à jour ou créée
            
        Utilisation dans l'API:
            Cette méthode devrait être appelée automatiquement via un signal
            après chaque ajout/modification/suppression d'entrée de journal.
            
        Exemple dans une vue:
            @action(detail=False, methods=['post'])
            def refresh_today(self, request):
                stat = DailyStat.generate_for_user(request.user)
                return Response(self.get_serializer(stat).data)
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

        obj, created = cls.objects.update_or_create(
            user=user,
            date=date,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(cat_stats),
            }
        )

        return obj
        
    @classmethod
    def get_calendar_data(cls, user, month=None, year=None):
        """
        Génère des données pour une visualisation de type calendrier heatmap.
        
        Args:
            user: L'utilisateur concerné
            month: Mois (1-12, None=tous les mois)
            year: Année (None=année en cours)
            
        Returns:
            list: Liste de dictionnaires pour chaque jour avec données
                [
                    {
                        "date": "2025-04-01",
                        "count": 2,
                        "mood": 7.5,
                        "intensity": 0.4  // Valeur normalisée pour la heatmap
                    },
                    ...
                ]
                
        Utilisation dans l'API:
            Idéal pour générer des visualisations de type "GitHub contributions"
            montrant l'activité quotidienne sur un calendrier.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def calendar(self, request):
                month = request.query_params.get('month')
                year = request.query_params.get('year')
                if month:
                    month = int(month)
                if year:
                    year = int(year)
                return Response(DailyStat.get_calendar_data(
                    request.user, month, year
                ))
        """
        import calendar
        from datetime import datetime
        
        # Paramètres par défaut
        if year is None:
            year = now().year
        
        # Construire le filtre de date
        date_filter = {'user': user, 'date__year': year}
        if month is not None:
            date_filter['date__month'] = month
        
        # Récupérer les statistiques
        stats = cls.objects.filter(**date_filter).order_by('date')
        
        # Déterminer les valeurs max pour normalisation
        max_count = max([stat.entries_count for stat in stats], default=1)
        
        # Générer les données pour chaque jour
        result = []
        for stat in stats:
            # Calculer une intensité normalisée pour la heatmap (0-1)
            intensity = stat.entries_count / max_count if max_count > 0 else 0
            
            result.append({
                'date': stat.date.isoformat(),
                'count': stat.entries_count,
                'mood': stat.mood_average,
                'intensity': round(intensity, 2)
            })
            
        return result