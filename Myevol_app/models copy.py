from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from collections import defaultdict
from django.conf import settings
from django.db.models import Avg, Count

# 👤 Utilisateur personnalisé
class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé héritant de AbstractUser de Django.
    Étend le modèle utilisateur standard avec des fonctionnalités supplémentaires
    pour l'application de suivi personnel.
    """
    email = models.EmailField(unique=True)  # Assure que chaque email est unique

    def __str__(self):
        """Représentation en chaîne de caractères de l'utilisateur"""
        return self.username

    def total_entries(self):
        """
        Retourne le nombre total d'entrées de journal pour cet utilisateur.
        Utilise la relation inverse 'entries' définie dans JournalEntry.
        """
        return self.entries.count()

    def mood_average(self, days=7):
        """
        Calcule la moyenne d'humeur sur les X derniers jours.
        
        Args:
            days (int): Nombre de jours à considérer pour le calcul
            
        Returns:
            float: Moyenne d'humeur arrondie à 1 décimale, ou None si aucune entrée
        """
        entries = self.entries.filter(created_at__gte=now() - timedelta(days=days))
        if entries.exists():
            return round(sum(entry.mood for entry in entries) / entries.count(), 1)
        return None

    def current_streak(self):
        """
        Calcule la série actuelle de jours consécutifs avec au moins une entrée.
        Vérifie jusqu'à 365 jours en arrière.
        
        Returns:
            int: Nombre de jours consécutifs avec une entrée
        """
        today = now().date()
        streak = 0
        for i in range(0, 365):
            day = today - timedelta(days=i)
            if self.entries.filter(created_at__date=day).exists():
                streak += 1
            else:
                break
        return streak

    def has_entries_every_day(self, last_n_days=7):
        """
        Vérifie si l'utilisateur a fait au moins une entrée chaque jour
        pendant les n derniers jours.
        
        Args:
            last_n_days (int): Nombre de jours à vérifier
            
        Returns:
            bool: True si l'utilisateur a une entrée pour chaque jour de la période
        """
        today = now().date()
        start_date = today - timedelta(days=last_n_days - 1)
        days_with_entry = self.entries.filter(
            created_at__date__gte=start_date
        ).values_list("created_at__date", flat=True).distinct()
        expected_days = {start_date + timedelta(days=i) for i in range(last_n_days)}
        return expected_days.issubset(set(days_with_entry))

    def level(self):
        """
        Calcule le niveau de l'utilisateur basé sur le nombre d'entrées.
        Le niveau augmente tous les 10 entrées.
        
        Returns:
            int: Niveau actuel de l'utilisateur
        """
        return (self.total_entries() // 10) + 1

    def update_badges(self):
        """
        Vérifie et attribue des badges à l'utilisateur s'il remplit les conditions.
        Parcourt tous les templates de badges et vérifie si l'utilisateur 
        remplit les conditions pour les badges qu'il n'a pas encore.
        """
        for template in BadgeTemplate.objects.all():
            if template.check_unlock(self) and not self.badges.filter(name=template.name).exists():
                Badge.objects.create(
                    user=self,
                    name=template.name,
                    icon=template.icon,
                    description=template.description,
                    level=template.level,
                )

    def all_objectives_achieved(self):
        """
        Vérifie si tous les objectifs de l'utilisateur sont achevés.
        
        Returns:
            bool: True si tous les objectifs sont achevés, False sinon
        """
        return not self.objectives.filter(done=False).exists()

    def entries_today(self):
        """
        Compte le nombre d'entrées faites aujourd'hui.
        
        Returns:
            int: Nombre d'entrées d'aujourd'hui
        """
        return self.entries.filter(created_at__date=now().date()).count()
    
    def entries_by_category(self):
        """
        Calcule la distribution des entrées par catégorie.
        
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
        """
        stats = defaultdict(int)
        for entry in self.entries.all():
            stats[entry.category] += 1
        return dict(stats)

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
        from django.db.models import Count
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
        from django.db.models import Avg
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
        
        Args:
            n (int): Nombre de jours à considérer
            
        Returns:
            dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
        """
        since = now() - timedelta(days=n)
        stats = defaultdict(int)
        for entry in self.entries.filter(created_at__gte=since):
            stats[entry.category] += 1
        return dict(stats)
    # Stocke la plus longue série de jours consécutifs avec des entrées
    longest_streak = models.PositiveIntegerField(default=0, editable=False)

    def update_streaks(self):
        """
        Met à jour le record de la plus longue série consécutive d'entrées.
        Compare la série actuelle avec le record historique et met à jour
        si nécessaire.
        
        Cette méthode devrait être appelée périodiquement pour actualiser le record,
        par exemple après l'ajout d'une nouvelle entrée de journal.
        """
        # Récupère la série actuelle de jours consécutifs
        current = self.current_streak()
        
        # Met à jour le record si la série actuelle est plus longue
        if current > self.longest_streak:
            self.longest_streak = current
            self.save()

# 📓 Entrée de journal
class JournalEntry(models.Model):
    """
    Modèle représentant une entrée de journal.
    Chaque entrée est liée à un utilisateur, a un contenu, une note d'humeur et une catégorie.
    """
    # Choix d'humeur de 1 à 10
    MOOD_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")  # Lien vers l'utilisateur
    content = models.TextField(verbose_name="Qu'avez-vous accompli aujourd'hui ?")  # Contenu de l'entrée
    mood = models.IntegerField(choices=MOOD_CHOICES, verbose_name="Note d'humeur")  # Note d'humeur (1-10)
    category = models.CharField(max_length=100, verbose_name="Catégorie")  # Catégorie de l'entrée
    created_at = models.DateTimeField(auto_now_add=True)  # Date et heure de création
    updated_at = models.DateTimeField(auto_now=True)  # Date et heure de dernière modification

    def __str__(self):
        """Représentation en chaîne de caractères de l'entrée"""
        return f"{self.user.username} - {self.created_at.date()}"

    @staticmethod
    def count_today(user):
        """
        Méthode statique pour compter les entrées d'aujourd'hui pour un utilisateur.
        
        Args:
            user (User): L'utilisateur dont on veut compter les entrées
            
        Returns:
            int: Nombre d'entrées faites aujourd'hui
        """
        return user.entries.filter(created_at__date=now().date()).count()


# 🎯 Objectif utilisateur
class Objective(models.Model):
    """
    Modèle représentant un objectif défini par l'utilisateur.
    Permet de suivre les progrès vers des objectifs spécifiques.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="objectives")  # Lien vers l'utilisateur
    title = models.CharField(max_length=255)  # Titre de l'objectif
    category = models.CharField(max_length=100)  # Catégorie de l'objectif
    done = models.BooleanField(default=False)  # État de complétion
    target_date = models.DateField()  # Date cible pour atteindre l'objectif
    target_value = models.PositiveIntegerField(default=1, verbose_name="Objectif à atteindre")  # Valeur à atteindre

    def __str__(self):
        """Représentation en chaîne de caractères de l'objectif avec indicateur d'achèvement"""
        return f"{self.title} ({'✅' if self.done else '🕓'})"

    def entries_done(self):
        """
        Compte le nombre d'entrées correspondant à la catégorie de cet objectif
        pour la date cible.
        
        Returns:
            int: Nombre d'entrées correspondant aux critères
        """
        return self.user.entries.filter(
            category=self.category,
            created_at__date=self.target_date
        ).count()

    def progress(self):
        """
        Calcule le pourcentage de progression vers l'objectif.
        
        Returns:
            int: Pourcentage de progression (0-100)
        """
        if self.target_value > 0:
            return min(100, int((self.entries_done() / self.target_value) * 100))
        return 0

    def is_achieved(self):
        """
        Vérifie si l'objectif est atteint (marqué comme fait ou progression à 100%).
        
        Returns:
            bool: True si l'objectif est atteint, False sinon
        """
        return self.done or self.progress() >= 100


# 🏅 Badge obtenu
class Badge(models.Model):
    """
    Modèle représentant un badge obtenu par un utilisateur.
    Les badges sont des récompenses pour des accomplissements spécifiques.
    """
    name = models.CharField(max_length=100)  # Nom du badge
    description = models.TextField()  # Description du badge
    icon = models.CharField(max_length=100)  # Icône (chemin ou identifiant)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")  # Lien vers l'utilisateur
    date_obtenue = models.DateField(auto_now_add=True)  # Date d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)

    def __str__(self):
        """Représentation en chaîne de caractères du badge"""
        return self.name

    def was_earned_today(self):
        """
        Vérifie si le badge a été obtenu aujourd'hui.
        
        Returns:
            bool: True si le badge a été obtenu aujourd'hui, False sinon
        """
        return self.date_obtenue == now().date()


# 🧩 BadgeTemplate : tous les badges définissables
class BadgeTemplate(models.Model):
    """
    Modèle définissant les différents badges disponibles dans l'application.
    Contient les critères d'attribution des badges aux utilisateurs.
    """
    name = models.CharField(max_length=100, unique=True)  # Nom unique du badge
    description = models.TextField()  # Description du badge
    icon = models.CharField(max_length=100)  # Icône (chemin ou identifiant)
    condition = models.CharField(max_length=255)  # Description de la condition d'obtention
    level = models.PositiveIntegerField(null=True, blank=True)  # Niveau du badge (optionnel)

    def __str__(self):
        """Représentation en chaîne de caractères du template de badge"""
        return self.name

    def check_unlock(self, user):
        """
        Vérifie si un utilisateur remplit les conditions pour débloquer ce badge.
        
        Cette méthode contient la logique détaillée pour chaque type de badge
        dans l'application. Elle vérifie différents critères selon le nom du badge.
        
        Args:
            user (User): L'utilisateur à vérifier
            
        Returns:
            bool: True si l'utilisateur remplit les conditions, False sinon
        """
        total = user.total_entries()
        mood_avg = user.mood_average(7)

        # Dictionnaire des conditions pour chaque type de badge
        conditions = {
            "Première entrée": total >= 1,  # Au moins une entrée
            "Régulier": user.has_entries_every_day(5),  # Entrées 5 jours consécutifs
            "Discipline": user.has_entries_every_day(10),  # Entrées 10 jours consécutifs
            "Résilience": user.has_entries_every_day(15),  # Entrées 15 jours consécutifs
            "Légende du Journal": user.has_entries_every_day(30),  # Entrées 30 jours consécutifs
            "Ambassadeur d'humeur": mood_avg is not None and mood_avg >= 9,  # Moyenne d'humeur élevée
            "Productivité": user.entries_today() >= 3,  # Au moins 3 entrées aujourd'hui
            "Objectif rempli !": user.all_objectives_achieved(),  # Tous les objectifs remplis
            "Persévérance": total >= 100,  # Au moins 100 entrées au total
        }

        # Vérifier si le badge est dans la liste des conditions définies
        if self.name in conditions:
            return conditions[self.name]

        # Cas spécial pour les badges de niveau
        if self.name.startswith("Niveau"):
            try:
                level_number = int(self.name.split(" ")[1])
                # Seuils pour chaque niveau (1 à 10)
                thresholds = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]
                if level_number <= len(thresholds):
                    return total >= thresholds[level_number - 1]
            except Exception:
                return False

        # Par défaut, retourne False pour les badges non reconnus
        return False


# 🔔 Notification utilisateur
class Notification(models.Model):
    """
    Modèle représentant une notification pour un utilisateur.
    Permet d'informer l'utilisateur d'événements importants dans l'application.
    """
    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif'),
        ('statistique', 'Statistique'),
        ('info', 'Information'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # Lien vers l'utilisateur
    message = models.TextField()  # Contenu de la notification
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info')  # Type de notification
    is_read = models.BooleanField(default=False)  # État de lecture
    read_at = models.DateTimeField(null=True, blank=True)  # Date de lecture (null si non lue)
    created_at = models.DateTimeField(auto_now_add=True)  # Date et heure de création
    archived = models.BooleanField(default=False)  # champ pour archiver la notification
    scheduled_at = models.DateTimeField(null=True, blank=True)  # Pour les notifications programmées
    class Meta:
        ordering = ['-created_at']  # Tri par défaut (récent en premier)

    def __str__(self):
        """Représentation en chaîne de caractères de la notification (tronquée à 50 caractères)"""
        return f"{self.user.username} - {self.message[:50]}"
    
    def archive(self):
        """
        Archive la notification (sans suppression).
        """
        self.archived = True
        self.save()

    def mark_as_read(self):
        """
        Marque une seule notification comme lue si ce n’est pas déjà fait.
        Enregistre également la date de lecture.
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save()

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues d’un utilisateur comme lues.

        Args:
            user (User): L'utilisateur concerné.

        Returns:
            int: Nombre de notifications marquées comme lues.
        """
        unread = cls.objects.filter(user=user, is_read=False)
        count = unread.update(is_read=True, read_at=now())
        return count

    @classmethod
    def get_unread(cls, user):
        """
        Récupère toutes les notifications non lues et non archivées d'un utilisateur.
        
        Cette méthode de classe permet d'accéder rapidement aux notifications
        qui nécessitent l'attention de l'utilisateur.
        
        Args:
            user: L'utilisateur dont on veut récupérer les notifications
            
        Returns:
            QuerySet: Ensemble des notifications non lues et non archivées
        """
        return cls.objects.filter(user=user, is_read=False, is_archived=False)

    @classmethod
    def get_inbox(cls, user):
        """
        Récupère toutes les notifications non archivées d'un utilisateur.
        
        Cette méthode correspond à la "boîte de réception" standard, contenant
        à la fois les notifications lues et non lues, mais pas les notifications archivées.
        
        Args:
            user: L'utilisateur dont on veut récupérer les notifications
            
        Returns:
            QuerySet: Ensemble des notifications non archivées (lues et non lues)
        """
        return cls.objects.filter(user=user, is_archived=False)

    @classmethod
    def get_archived(cls, user):
        """
        Récupère toutes les notifications archivées d'un utilisateur.
        
        Cette méthode permet d'accéder aux anciennes notifications que l'utilisateur
        a décidé de conserver mais de mettre de côté.
        
        Args:
            user: L'utilisateur dont on veut récupérer les notifications archivées
            
        Returns:
            QuerySet: Ensemble des notifications archivées
        """
        return cls.objects.filter(user=user, is_archived=True)    
        


class DailyStat(models.Model):
    """
    Modèle pour stocker les statistiques journalières d'un utilisateur.
    Agrège les données d'entrées de journal pour une analyse et un affichage efficaces.
    """
    # Relation avec l'utilisateur (utilise le modèle défini dans settings)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_stats")
    date = models.DateField()  # 📅 Date de la stat (ex : 2025-04-18)
    entries_count = models.PositiveIntegerField(default=0)  # 📝 Nombre d'entrées ce jour-là
    mood_average = models.FloatField(null=True, blank=True)  # 😄 Moyenne d'humeur ce jour-là
    categories = models.JSONField(default=dict, blank=True)  # 📊 Répartition par catégorie : {"Sport": 2, "Travail": 1}
    
    class Meta:
        """
        Métadonnées du modèle définissant les contraintes et les comportements.
        """
        unique_together = ('user', 'date')  # Garantit qu'il n'y a qu'une seule entrée par utilisateur et par jour
        ordering = ['-date']  # Tri par date décroissante (plus récent en premier)
        verbose_name = "Statistique journalière"  # Nom singulier dans l'admin
        verbose_name_plural = "Statistiques journalières"  # Nom pluriel dans l'admin
    
    def __str__(self):
        """
        Représentation en chaîne de caractères de l'objet statistique journalier.
        
        Returns:
            str: Nom d'utilisateur et date formatés (ex: "john_doe - 2025-04-18")
        """
        return f"{self.user.username} - {self.date}"
    
    @classmethod
    def generate_for_user(cls, user, date=None):
        """
        🛠️ Méthode de classe pour générer ou mettre à jour les statistiques d'un utilisateur pour une date donnée.
        
        Cette méthode calcule le nombre d'entrées, la moyenne d'humeur et les statistiques par catégorie,
        puis crée ou met à jour l'enregistrement correspondant dans la base de données.
        
        Args:
            user: L'utilisateur pour lequel générer les statistiques
            date: La date pour laquelle générer les statistiques (aujourd'hui par défaut)
            
        Returns:
            DailyStat: L'objet de statistique créé ou mis à jour
        """
        if not date:
            date = now().date()
            
        # Récupère toutes les entrées de l'utilisateur pour la date spécifiée
        entries = user.entries.filter(created_at__date=date)
        
        # Calcule le nombre total d'entrées
        entries_count = entries.count()
        
        # Calcule la moyenne d'humeur (arrondie à 1 décimale si elle existe)
        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg else None
        
        # Calcule les statistiques par catégorie
        cat_stats = {}
        for cat in entries.values_list("category", flat=True):
            cat_stats[cat] = cat_stats.get(cat, 0) + 1
        
        # Crée ou met à jour l'objet de statistique dans la base de données
        obj, created = cls.objects.update_or_create(
            user=user,
            date=date,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": cat_stats,
            }
        )
        
        return obj
    
class EventLog(models.Model):
    """
    Modèle pour enregistrer les événements et actions importantes dans l'application.
    Permet de tracer l'activité des utilisateurs et les événements système pour l'audit,
    le débogage et l'analyse des comportements utilisateurs.
    """
    # Lien vers l'utilisateur concerné (optionnel pour les événements système)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Type d'action effectuée (ex: "connexion", "création_entrée", "attribution_badge")
    action = models.CharField(max_length=255)
    
    # Détails supplémentaires sur l'événement
    description = models.TextField(blank=True)
    
    # Horodatage automatique de l'événement
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Représentation textuelle du log d'événement.
        
        Returns:
            str: Chaîne formatée avec la date/heure et l'action effectuée
        """
        return f"{self.created_at} - {self.action}"
    
class Challenge(models.Model):
    """
    Modèle représentant un défi temporaire proposé aux utilisateurs.
    Les défis encouragent l'engagement des utilisateurs en fixant des objectifs
    à atteindre dans une période définie.
    """
    # Titre du défi affiché aux utilisateurs
    title = models.CharField(max_length=255)
    
    # Description détaillée expliquant le défi
    description = models.TextField()
    
    # Période de validité du défi
    start_date = models.DateField()  # Date de début du défi
    end_date = models.DateField()    # Date de fin du défi
    
    # Nombre d'entrées à créer pour compléter le défi
    target_entries = models.PositiveIntegerField(default=5)
    
    def is_active(self):
        """
        Vérifie si le défi est actuellement actif.
        Un défi est actif si la date actuelle est comprise entre la date
        de début et la date de fin incluses.
        
        Returns:
            bool: True si le défi est actif, False sinon
        """
        today = now().date()
        return self.start_date <= today <= self.end_date
    
    def is_completed(self, user):
        """
        Vérifie si un utilisateur a complété le défi.
        Le défi est considéré comme complété si l'utilisateur a créé au moins
        le nombre requis d'entrées pendant la période du défi.
        
        Args:
            user: L'utilisateur dont on vérifie la progression
            
        Returns:
            bool: True si l'utilisateur a atteint l'objectif du défi, False sinon
        """
        return user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count() >= self.target_entries

class JournalMedia(models.Model):
    """
    Modèle pour stocker les fichiers multimédias associés aux entrées de journal.
    Permet aux utilisateurs d'enrichir leurs entrées avec des images ou des enregistrements audio.
    """
    # Relation avec l'entrée de journal à laquelle ce média est associé
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="media")
    
    # Fichier média stocké dans le dossier 'journal_media/'
    file = models.FileField(upload_to="journal_media/")
    
    # Type de média (image ou audio)
    type = models.CharField(
        max_length=10, 
        choices=[("image", "Image"), ("audio", "Audio")]
    )
    
    def __str__(self):
        """
        Représentation textuelle du média.
        
        Returns:
            str: Description du type de média et l'entrée associée
        """
        return f"{self.get_type_display()} pour {self.entry}"

class Quote(models.Model):
    """
    Modèle pour stocker des citations inspirantes ou motivantes.
    Ces citations peuvent être affichées aux utilisateurs en fonction de leur humeur
    ou à des moments stratégiques dans l'application.
    """
    # Le texte de la citation
    text = models.TextField()
    
    # L'auteur de la citation (optionnel)
    author = models.CharField(max_length=255, blank=True)
    
    # Étiquette d'humeur associée pour le ciblage contextuel
    mood_tag = models.CharField(max_length=50, blank=True)  # Ex: "positive", "low", "neutral"
    
    def __str__(self):
        """
        Représentation textuelle de la citation.
        
        Returns:
            str: Citation avec son auteur si disponible
        """
        if self.author:
            return f'"{self.text}" — {self.author}'
        return f'"{self.text}"'

class WeeklyStat(models.Model):
    """
    Modèle pour stocker les statistiques hebdomadaires d'un utilisateur.
    Agrège les données d'entrées pour fournir des insights sur une période d'une semaine.
    Permet de suivre les tendances et l'évolution sur une échelle de temps plus large que les stats quotidiennes.
    """
    # Relation avec l'utilisateur concerné
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_stats")
    
    # Premier jour de la semaine concernée (généralement un lundi)
    week_start = models.DateField()
    
    # Nombre total d'entrées créées pendant la semaine
    entries_count = models.PositiveIntegerField()
    
    # Moyenne d'humeur pour la semaine entière
    mood_average = models.FloatField(null=True, blank=True)
    
    # Répartition des entrées par catégorie au format JSON
    categories = models.JSONField(default=dict, blank=True)
    
    class Meta:
        """
        Métadonnées du modèle définissant les contraintes et comportements.
        """
        # Empêche la création de statistiques dupliquées pour la même semaine et le même utilisateur
        unique_together = ('user', 'week_start')
        
        # Trie les résultats par semaine, de la plus récente à la plus ancienne
        ordering = ['-week_start']
    
    def __str__(self):
        """
        Représentation textuelle des statistiques hebdomadaires.
        
        Returns:
            str: Chaîne identifiant l'utilisateur et la semaine concernée
        """
        return f"{self.user.username} - semaine du {self.week_start}"
    
    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Méthode de classe pour générer ou mettre à jour les statistiques hebdomadaires d'un utilisateur.
        
        Cette méthode calcule les statistiques hebdomadaires à partir d'une date de référence,
        en considérant la semaine qui contient cette date (du lundi au dimanche).
        
        Args:
            user: L'utilisateur pour lequel générer les statistiques
            reference_date: Date de référence pour déterminer la semaine (date actuelle par défaut)
            
        Returns:
            tuple: Tuple contenant (objet WeeklyStat, booléen indiquant si l'objet a été créé)
        """
        from django.db.models.functions import TruncWeek
        
        # Utilise la date actuelle si aucune date de référence n'est fournie
        if not reference_date:
            reference_date = now().date()
        
        # Calcule le premier jour de la semaine (lundi) contenant la date de référence
        week_start = reference_date - timedelta(days=reference_date.weekday())
        
        # Calcule le dernier jour de la semaine (dimanche)
        week_end = week_start + timedelta(days=6)
        
        # Récupère toutes les entrées de la semaine
        entries = user.entries.filter(created_at__date__range=(week_start, week_end))
        
        # Compte le nombre total d'entrées
        entries_count = entries.count()
        
        # Calcule la moyenne d'humeur (arrondie à 1 décimale si elle existe)
        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg else None
        
        # Compte les entrées par catégorie
        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1
        
        # Crée ou met à jour l'objet de statistique hebdomadaire
        return cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
class ChallengeProgress(models.Model):
    """
    Modèle pour suivre la progression des utilisateurs dans les défis.
    Établit une relation entre un utilisateur et un défi spécifique,
    permettant de suivre l'état d'achèvement de chaque défi pour chaque utilisateur.
    """
    # Lien vers l'utilisateur qui participe au défi
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenges")
    
    # Lien vers le défi concerné
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="progresses")
    
    # Indique si le défi a été complété par l'utilisateur
    completed = models.BooleanField(default=False)
    
    # Date et heure auxquelles le défi a été complété (si applicable)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """
        Métadonnées du modèle définissant les contraintes.
        """
        # Assure qu'un utilisateur ne peut avoir qu'une seule progression par défi
        unique_together = ('user', 'challenge')

def check_challenges(user):
    """
    Vérifie la progression et l'accomplissement des défis actifs pour un utilisateur.
    
    Cette fonction examine tous les défis actifs à la date actuelle, et pour chacun:
    1. Récupère ou crée un objet de progression pour l'utilisateur
    2. Vérifie si l'utilisateur a satisfait les conditions d'achèvement du défi
    3. Met à jour l'état de la progression si le défi est complété
    4. Crée une notification pour informer l'utilisateur de sa réussite
    
    Args:
        user: L'utilisateur dont on vérifie la progression dans les défis
    """
    # Récupère la date du jour
    today = now().date()
    
    # Récupère tous les défis actifs (dont la période inclut la date actuelle)
    for challenge in Challenge.objects.filter(start_date__lte=today, end_date__gte=today):
        # Récupère ou crée un objet de progression pour ce défi et cet utilisateur
        progress, _ = ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)
        
        # Vérifie si le défi n'est pas déjà marqué comme complété et si l'utilisateur l'a réellement complété
        if not progress.completed and challenge.is_completed(user):
            # Met à jour l'état de progression
            progress.completed = True
            progress.completed_at = now()
            progress.save()
            
            # Crée une notification pour informer l'utilisateur
            Notification.objects.create(
                user=user,
                message=f"🎯 Tu as terminé le défi : {challenge.title} !",
                notif_type="objectif"
            )





    

class UserPreference(models.Model):
    """
    Modèle pour stocker les préférences personnalisées de chaque utilisateur.
    Permet de contrôler les notifications et l'apparence de l'application.
    Chaque utilisateur a exactement une instance de ce modèle (relation one-to-one).
    """
    # Relation one-to-one avec l'utilisateur (un utilisateur a exactement une préférence)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    
    # Préférences de notifications par type
    notif_badge = models.BooleanField(default=True)      # Notifications pour les badges débloqués
    notif_objectif = models.BooleanField(default=True)   # Notifications liées aux objectifs
    notif_info = models.BooleanField(default=True)       # Notifications informatives générales
    notif_statistique = models.BooleanField(default=True)  # Notifications de statistiques
    
    # Préférences d'apparence
    dark_mode = models.BooleanField(default=False)       # Mode sombre activé ou désactivé
    accent_color = models.CharField(max_length=20, default="#6C63FF")  # Couleur principale pour personnaliser l'interface
    font_choice = models.CharField(max_length=50, default="Roboto")    # Police de caractères préférée
    enable_animations = models.BooleanField(default=True)              # Option pour activer/désactiver les animations

    def __str__(self):
        """
        Représentation textuelle de l'objet de préférences.
        
        Returns:
            str: Chaîne indiquant à quel utilisateur appartiennent ces préférences
        """
        return f"Préférences de {self.user.username}"