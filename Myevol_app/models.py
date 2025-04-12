from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilisateur personnalisé
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# Entrée de journal
class JournalEntry(models.Model):
    MOOD_CHOICES = [(i, f"{i}/10") for i in range(1, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    content = models.TextField(verbose_name="Qu'avez-vous accompli aujourd'hui ?")
    mood = models.IntegerField(choices=MOOD_CHOICES, verbose_name="Note d'humeur")
    category = models.CharField(max_length=100, verbose_name="Catégorie")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"


# Objectif
class Objective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="objectives")
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    target_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({'✅' if self.done else '🕓'})"

    def entries_done(self):
        return self.user.entries.filter(category=self.category, created_at__date=self.target_date).count()

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # nom d’icône (ou image plus tard)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    date_obtenue = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class BadgeTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10)  # emoji ou code
    condition = models.CharField(max_length=255)  # texte explicatif

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

