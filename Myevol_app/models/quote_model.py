# MyEvol_app/models/quote_model.py

import random
import logging
import hashlib
import datetime
from django.db import models
from django.db.models import Avg, Count, Case, When, IntegerField
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

# Loggs améliorés pour la gestion des citations
logger = logging.getLogger(__name__)

class Quote(models.Model):
    """
    Modèle pour stocker des citations inspirantes ou motivantes.
    Ces citations peuvent être affichées aux utilisateurs en fonction de leur humeur
    ou à des moments stratégiques dans l'application.
    """

    # Le texte de la citation
    text = models.TextField(help_text="Le texte de la citation.")

    # L'auteur de la citation (optionnel)
    author = models.CharField(max_length=255, blank=True, help_text="L'auteur de la citation.")

    # Étiquette d'humeur associée pour le ciblage contextuel
    mood_tag = models.CharField(
        max_length=50,
        blank=True,
        help_text="Étiquette d'humeur associée (ex: 'positive', 'low', 'neutral')"
    )

    class Meta:
        verbose_name = "Citation"
        verbose_name_plural = "Citations"
        ordering = ['author']
        indexes = [
            models.Index(fields=['mood_tag']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        """ Représentation textuelle de la citation. """
        return f'"{self.text}" — {self.author if self.author else "Inconnu"}'

    def __repr__(self):
        """ Représentation détaillée de la citation. """
        return f"<Quote id={self.id} text='{self.text[:50]}...' author='{self.author}'>"

    def get_absolute_url(self):
        """ Retourne l'URL vers la citation spécifique. """
        return f"/api/quotes/{self.id}/"

    def clean(self):
        """ Validation de l'objet avant l'enregistrement. """
        if not self.text:
            raise ValidationError("Le texte de la citation ne peut pas être vide.")

    def length(self):
        """ Retourne la longueur du texte de la citation. """
        return len(self.text)

    @classmethod
    def get_random(cls, mood_tag=None):
        """ Retourne une citation aléatoire, optionnellement filtrée par mood_tag. """
        queryset = cls.objects.all()
        if mood_tag:
            queryset = queryset.filter(mood_tag=mood_tag)
        
        count = queryset.count()
        if count == 0:
            return None
            
        random_index = random.randint(0, count - 1)
        return queryset[random_index]

    @classmethod
    def get_daily_quote(cls, user=None):
        """ Retourne la citation du jour, potentiellement personnalisée selon l'utilisateur. """
        today = datetime.date.today().strftime("%Y%m%d")
        mood_filter = None

        if user:
            recent_entries = user.entries.filter(
                created_at__gte=datetime.datetime.now() - datetime.timedelta(days=3)
            )
            if recent_entries.exists():
                avg_mood = recent_entries.aggregate(avg=Avg('mood'))['avg']
                if avg_mood is not None:
                    if avg_mood < 4:
                        mood_filter = 'low'
                    elif avg_mood > 7:
                        mood_filter = 'positive'
                    else:
                        mood_filter = 'neutral'
        
        quotes = cls.objects.all()
        if mood_filter:
            quotes = quotes.filter(mood_tag=mood_filter)

        count = quotes.count()
        if count == 0:
            return None

        hash_obj = hashlib.md5(today.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        index = hash_int % count
        return quotes[index]

    @classmethod
    def get_authors_list(cls):
        """ Retourne la liste des auteurs disponibles avec leur nombre de citations. """
        authors = cls.objects.exclude(author='').values('author').annotate(
            count=Count('id')
        ).order_by('author')

        return list(authors)

