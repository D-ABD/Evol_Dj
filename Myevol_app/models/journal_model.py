# MyEvol_app/models/journal_model.py

import logging
from datetime import timedelta
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings


# Logger importé pour la journalisation
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL

class JournalEntry(models.Model):
    """
    Modèle représentant une entrée de journal.
    Chaque entrée est liée à un utilisateur, a un contenu, une note d'humeur et une catégorie.
    
    API Endpoints suggérés:
    - GET /api/journal-entries/ - Liste des entrées de l'utilisateur courant
    - POST /api/journal-entries/ - Créer une nouvelle entrée
    - GET /api/journal-entries/{id}/ - Détails d'une entrée spécifique
    - PUT/PATCH /api/journal-entries/{id}/ - Modifier une entrée existante
    - DELETE /api/journal-entries/{id}/ - Supprimer une entrée
    - GET /api/journal-entries/stats/ - Statistiques sur les entrées (par catégorie, humeur, etc.)
    - GET /api/journal-entries/calendar/ - Données pour vue calendrier (dates avec entrées)
    """
    
    # Choix d'humeur de 1 à 10
    MOOD_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]
    
    # Mapping des émojis pour chaque niveau d'humeur (utile pour l'API)
    MOOD_EMOJIS = {
        1: "😡", 2: "😠", 3: "😟", 4: "😐", 
        5: "🙂", 6: "😊", 7: "😃", 8: "😁", 
        9: "🤩", 10: "😍"
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries", help_text="Utilisateur concerné par l’entrée")
    content = models.TextField(verbose_name="Qu'avez-vous accompli aujourd'hui ?", help_text="Le contenu de l’entrée de journal")
    mood = models.IntegerField(
        choices=MOOD_CHOICES,
        verbose_name="Note d'humeur",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="La note d'humeur (de 1 à 10) associée à cette entrée"
    )
    category = models.CharField(max_length=100, verbose_name="Catégorie", help_text="La catégorie de l'entrée (ex : Travail, Santé)")
    created_at = models.DateTimeField(default=now, help_text="Date et heure de création de l’entrée")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date et heure de la dernière mise à jour")

    class Meta:
        verbose_name = "Entrée de journal"
        verbose_name_plural = "Entrées de journal"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"

    def __repr__(self):
        """
        Retourne une représentation plus lisible de l'entrée de journal.
        """
        return f"<JournalEntry id={self.id} user='{self.user.username}' category='{self.category}' mood='{self.mood}'>"

    @property
    def created_day(self):
        return self.created_at.date()

    def get_absolute_url(self):
        """
        Retourne l’URL vers la vue de détail de l’entrée de journal.
        """
        return reverse('journalentry-detail', kwargs={'pk': self.pk})

    def get_mood_emoji(self):
        """
        Retourne l'emoji correspondant à la note d'humeur.
        
        Returns:
            str: Emoji représentant l'humeur
        """
        return self.MOOD_EMOJIS.get(self.mood, "😐")

    def clean(self):
        """
        Validation personnalisée pour s'assurer que le contenu est suffisamment long.
        
        Raises:
            ValidationError: Si le contenu est trop court
        """
        super().clean()
        if self.content and len(self.content.strip()) < 5:
            raise ValidationError({'content': 'Le contenu doit comporter au moins 5 caractères.'})

    def save(self, *args, **kwargs):
        """
        Surcharge de save : met à jour les stats, badges, streaks, défis.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Import local pour éviter les imports circulaires
            from Myevol_app.models.stats_model import DailyStat
            
            # Importation locale de la fonction check_challenges
            from Myevol_app.services.challenge_service import check_challenges

            # Mise à jour des statistiques journalières
            DailyStat.generate_for_user(self.user, self.created_at.date())

            # Vérification des défis
            check_challenges(self.user)

            # Mise à jour des badges
            self.user.update_badges()

            # Mise à jour des séries de jours consécutifs
            self.user.update_streaks()

    @staticmethod
    def count_today(user, reference_date=None):
        """
        Compte les entrées faites aujourd'hui (ou à une date donnée).
        
        Args:
            user (User): L'utilisateur concerné
            reference_date (date, optional): Date de référence (aujourd'hui par défaut)
            
        Returns:
            int: Nombre d'entrées à la date spécifiée
        """
        if reference_date is None:
            reference_date = now().date()
        return user.entries.filter(created_at__date=reference_date).count()

    @classmethod
    def get_entries_by_date_range(cls, user, start_date, end_date):
        """
        Récupère les entrées dans une plage de dates spécifique.
        
        Args:
            user (User): L'utilisateur concerné
            start_date (date): Date de début
            end_date (date): Date de fin
            
        Returns:
            QuerySet: Entrées dans la plage de dates spécifiée
        """
        return cls.objects.filter(
            user=user,
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )
    
    @classmethod
    def get_category_suggestions(cls, user, limit=10):
        """
        Retourne les catégories les plus utilisées par l'utilisateur.
        
        Args:
            user (User): L'utilisateur concerné
            limit (int): Nombre maximum de suggestions à retourner
            
        Returns:
            list: Liste des catégories les plus utilisées
        """
        from django.db.models import Count
        
        return list(cls.objects.filter(user=user)
                   .values('category')
                   .annotate(count=Count('category'))
                   .order_by('-count')
                   .values_list('category', flat=True)[:limit])


# 📎 Médias associés à une entrée de journal
class JournalMedia(models.Model):
    """
    Modèle pour stocker les fichiers multimédias associés aux entrées de journal.
    Permet aux utilisateurs d'enrichir leurs entrées avec des images ou des enregistrements audio.
    """
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="media", help_text="Entrée de journal à laquelle ce média est associé")
    file = models.FileField(upload_to="journal_media/", help_text="Fichier multimédia (image, audio, etc.)")
    type = models.CharField(
        max_length=10,
        choices=[("image", "Image"), ("audio", "Audio")],
        help_text="Type de fichier multimédia (image ou audio)"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création du média")

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.get_type_display()} pour {self.entry}"

    def file_url(self):
        """
        Retourne l'URL complète du fichier.
        
        Returns:
            str: URL du fichier média
        """
        if self.file:
            return self.file.url
        return None

    def file_size(self):
        """
        Retourne la taille du fichier en octets.
        
        Returns:
            int: Taille du fichier en octets
        """
        if self.file:
            return self.file.size
        return 0

    def validate_file_type(self):
        """
        Vérifie si le type de fichier correspond au type déclaré.
        
        Raises:
            ValidationError: Si le type de fichier ne correspond pas
        """
        import mimetypes
        if not self.file:
            return
            
        mime_type, _ = mimetypes.guess_type(self.file.name)
        
        if self.type == 'image' and not mime_type.startswith('image/'):
            raise ValidationError({'file': 'Le fichier doit être une image.'})
            
        if self.type == 'audio' and not mime_type.startswith('audio/'):
            raise ValidationError({'file': 'Le fichier doit être un audio.'})


