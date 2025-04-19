from django.db import models


class Quote(models.Model):
    """
    Modèle pour stocker des citations inspirantes ou motivantes.
    Ces citations peuvent être affichées aux utilisateurs en fonction de leur humeur
    ou à des moments stratégiques dans l'application.
    
    API Endpoints suggérés:
    - GET /api/quotes/ - Liste de toutes les citations
    - GET /api/quotes/random/ - Retourne une citation aléatoire
    - GET /api/quotes/random/?mood_tag=positive - Citation aléatoire filtrée par étiquette
    - GET /api/quotes/daily/ - Citation du jour
    - GET /api/quotes/authors/ - Liste des auteurs disponibles
    
    Exemple de sérialisation JSON:
    {
        "id": 42,
        "text": "La vie est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.",
        "author": "Albert Einstein",
        "mood_tag": "positive",
        "length": 75  // Champ calculé optionnel
    }
    """

    # Le texte de la citation
    text = models.TextField()

    # L'auteur de la citation (optionnel)
    author = models.CharField(max_length=255, blank=True)

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
        
        """
        Filtres API recommandés:
        - author (exact, contains)
        - mood_tag (exact, in)
        - text (contains)
        - length (calculé, pour filtrer par taille)
        """
        
        indexes = [
            models.Index(fields=['mood_tag']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        """
        Représentation textuelle de la citation.
        
        Returns:
            str: Citation avec son auteur si disponible
        """
        if self.author:
            return f'"{self.text}" — {self.author}'
        return f'"{self.text}"'
    
    def length(self):
        """
        Retourne la longueur du texte de la citation.
        
        Returns:
            int: Nombre de caractères dans la citation
            
        Utilisation dans l'API:
            Peut être utilisé comme champ calculé pour filtrer les citations
            par longueur (courtes pour notifications, longues pour affichage principal).
        """
        return len(self.text)
    
    @classmethod
    def get_random(cls, mood_tag=None):
        """
        Retourne une citation aléatoire, optionnellement filtrée par mood_tag.
        
        Args:
            mood_tag (str, optional): Étiquette d'humeur pour filtrer les citations
            
        Returns:
            Quote: Une citation aléatoire ou None si aucune ne correspond
            
        Utilisation dans l'API:
            Parfait pour un endpoint qui affiche une citation aléatoire
            dans le dashboard ou les notifications.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def random(self, request):
                mood_tag = request.query_params.get('mood_tag')
                quote = Quote.get_random(mood_tag)
                if not quote:
                    return Response(
                        {"detail": "Aucune citation trouvée."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                return Response(self.get_serializer(quote).data)
        """
        import random
        
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
        """
        Retourne la citation du jour, potentiellement personnalisée selon l'utilisateur.
        
        Args:
            user (User, optional): Utilisateur pour personnalisation basée sur son humeur
            
        Returns:
            Quote: Citation du jour
            
        Utilisation dans l'API:
            Idéal pour un widget de citation du jour sur le dashboard.
            
        Note technique:
            Cette méthode assure que tous les utilisateurs voient la même citation le même jour,
            à moins qu'un filtre d'humeur spécifique ne soit appliqué selon leur profil.
        """
        import datetime
        import hashlib
        
        # Date du jour comme seed pour la sélection
        today = datetime.date.today().strftime("%Y%m%d")
        
        # Si un utilisateur est fourni, on peut personnaliser selon son humeur récente
        mood_filter = None
        if user:
            from django.db.models import Avg
            # Calcul de l'humeur moyenne sur les 3 derniers jours
            recent_entries = user.entries.filter(
                created_at__gte=datetime.datetime.now() - datetime.timedelta(days=3)
            )
            if recent_entries.exists():
                avg_mood = recent_entries.aggregate(avg=Avg('mood'))['avg']
                # Définition du filtre selon l'humeur
                if avg_mood is not None:
                    if avg_mood < 4:
                        mood_filter = 'low'
                    elif avg_mood > 7:
                        mood_filter = 'positive'
                    else:
                        mood_filter = 'neutral'
        
        # Récupération des citations correspondant au filtre d'humeur
        quotes = cls.objects.all()
        if mood_filter:
            filtered_quotes = quotes.filter(mood_tag=mood_filter)
            # Si aucune citation ne correspond, on revient à toutes les citations
            if filtered_quotes.exists():
                quotes = filtered_quotes
                
        count = quotes.count()
        if count == 0:
            return None
            
        # Utiliser le hashage pour assurer la même sélection pour tous les utilisateurs le même jour
        hash_obj = hashlib.md5(today.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # Sélection déterministe basée sur la date
        index = hash_int % count
        return quotes[index]
    
    @classmethod
    def get_authors_list(cls):
        """
        Retourne la liste des auteurs disponibles avec leur nombre de citations.
        
        Returns:
            list: Liste de dictionnaires {author, count}
            
        Utilisation dans l'API:
            Utile pour construire un filtre ou un menu déroulant des auteurs.
            
        Exemple dans une vue:
            @action(detail=False, methods=['get'])
            def authors(self, request):
                return Response(Quote.get_authors_list())
        """
        from django.db.models import Count
        
        authors = cls.objects.exclude(author='').values('author').annotate(
            count=Count('id')
        ).order_by('author')
        
        return list(authors)