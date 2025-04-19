# Evol_Dj
# 📘 MyEvol

**MyEvol** est une application web Django de développement personnel. Elle permet de suivre son humeur au quotidien, définir des objectifs, débloquer des badges de progression et visualiser ses statistiques sous forme de graphiques.

---

## 🚀 Fonctionnalités principales

- ✍️ Écriture d’entrées de **journal** avec humeur et catégorie
- 🎯 Suivi des **objectifs personnels**
- 📊 Visualisation de **statistiques** (humeur, objectifs, catégories)
- 🏅 **Badges** de progression et niveaux à débloquer
- 🔔 **Notifications** automatiques lors du déblocage d’un badge
- 📈 Graphiques (Chart.js) intégrés au dashboard
- 👤 Authentification utilisateur (inscription, connexion, déconnexion)

---

## 🛠️ Tech Stack

- **Backend** : Django 4.2
- **Base de données** : SQLite (ou PostgreSQL)
- **Frontend** : HTML + Bootstrap 5 + Chart.js
- **Auth** : Django User Model personnalisé

---

## 📸 Aperçus

> _Exemples d’écrans à venir_  
> Tu peux ajouter ici des screenshots de ton dashboard, journal, ou badges.

---

## 📂 Structure du projet

Myevol_project/ ├── Myevol_app/ │ ├── models.py │ ├── views.py │ ├── forms.py │ ├── urls.py │ ├── templates/myevol/ │ ├── static/ │ └── utils/ ├── templates/base.html ├── manage.py └── requirements.txt


---

## ⚙️ Installation locale

Cloner le projet :
    git clone https://github.com/ton-user/my-evol.git
    cd my-evol

Activer environnement virtuel : 
    python3 -m venv env
    source env/bin/activate  # sous Linux/Mac
    env\Scripts\activate     # sous Windows


Installer les dépendances :
    pip install -r requirements.txt

Appliquer les migrations :
    python3 manage.py makemigrations
    python3 manage.py migrate

Lancer le serveur :    
    python3 manage.py runserver

Créer un super utilisateur (admin) :
    python3 manage.py createsuperuser

✅ TODO (roadmap)
    Journal quotidien
    Objectifs personnels
    Notifications et badges
    Dashboard avec stats et graphiques
    Export PDF / Excel
    Version mobile
    PWA ou version native via React Native 

🧠 Développé avec ❤️ par @Adserv    
# Evol_Dj



Ajout de fonctionnalités:

Export des données au format CSV/PDF
Système de partage/compétition entre utilisateurs
Intégration avec d'autres applications de santé/fitness
AJout un tchat et un forum


Ajoute une méthode __repr__ dans les modèles principaux (utile pour debug shell, admin ou tests).

help_text dans les champs des modèles : pratique pour l’interface d’admin ou les formulaires auto-générés.

Tests automatiques : si ce n’est pas encore fait, je peux t’aider à écrire des tests unitaires (TestCase) pour chaque modèle.

Méthode get_absolute_url : utile si tu as des vues DetailView (ou dans l’admin, par exemple).

Badge "7 jours d'activité"

Ce badge est attribué ici mais n'est pas défini dans BadgeTemplate.check_unlock(). Tu peux :

L’ajouter dans BadgeTemplate + dans la méthode check_unlock()

Ou le garder ici comme badge "hors système", à toi de choisir

Unicité des signaux :

Tu as deux signaux @receiver(post_save, sender=Notification) ➜ tu pourrais les fusionner :
award_badge() vs Badge.save()

Tu as un léger chevauchement : award_badge() crée une notification, mais Badge.save() aussi ➜ tu pourrais soit :

Supprimer la notification dans award_badge() (et laisser save() s’en charger)

Ou désactiver la création auto dans save() si l’appel vient de award_badge()

Ou ajouter un flag skip_notification=False dans Badge.save() si besoin

Assure-toi que ces données sont bien importées dans la base via un loaddata, un script ou dans une tâche initial_setup avec BadgeTemplate.objects.get_or_create(...).

Évite les doublons name dans cette liste, sinon Django lèvera une erreur d’unicité (ce qui n’est pas le cas ici).

Pour que cela fonctionne avec Celery Beat
Il te manque juste l’enregistrement de la tâche planifiée dans l’admin Django, ou via un script comme :

Exemple avec django_celery_beat :
bash
Copier
Modifier
python manage.py shell
python
Copier
Modifier
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Toutes les 10 minutes par exemple
schedule, _ = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.MINUTES)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name='Envoyer les notifications programmées',
    task='myevol_app.tasks.send_scheduled_notifications',
)
Remplace "myevol_app.tasks..." par le chemin exact vers ton fichier contenant la tâche.

✅ Tu peux aller plus loin ensuite :
Ajouter un envoi réel (mail, push, etc.)

Filtrer par notif_type

Logger plus finement les erreurs

Ajouter les loggs aux models