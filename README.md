git add .
git commit -m " ajout viewset/documentation/"
git push origin main


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

Système de partage/compétition entre utilisateurs
Intégration avec d'autres applications de santé/fitness
AJout un tchat et un forum
🔔 Ajouter une notification "programmée" à afficher plus tard (scheduled_at) ?

📩 Activer une notification email ou push pour les notifications importantes ?

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


MAJ des model/tests/ok

enrichi avec :

pour tous les prochains, je souhaite que tu e propose des améliorations et les apppliquent
aprés, que tu mettes à jour avec tes conseils en plus de :  
✅ __repr__
✅ get_absolute_url()
✅ help_text sur tous les champs
loggs (import loggin...)
docstrings complet pour que le dev cree les api plus tard
au besoin, cree les services, signals...logique metier...
--------------------------------------------------
--------------------------------------------------
--------------------------------------------------
t’ajoute un logger bien structuré
 Pour que ta doc soit vraiment complète :
1. Ajoute des @extend_schema sur les vues / viewsets
Pour que Swagger affiche :

Les params d’entrée (query, body…)

Les réponses (200, 400, 403…)

Les descriptions des endpoints

python
Copier
Modifier
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Liste des objectifs de l'utilisateur",
    description="Renvoie tous les objectifs actifs de l'utilisateur connecté.",
    responses={200: ObjectiveSerializer(many=True)}
)
def list(self, request):
    ...
2. Ajoute des AutoSchema ou get_schema_fields() pour les vues basées sur APIView
Si tu utilises APIView au lieu de ViewSet, tu peux aussi ajouter :

python
Copier
Modifier
from drf_spectacular.utils import OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter(name='start_date', required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='end_date', required=False, type=str, location=OpenApiParameter.QUERY),
    ]
)
3. Ajoute des descriptions aux champs personnalisés avec @extend_schema_field si besoin
Exemple :

python
Copier
Modifier
from drf_spectacular.utils import extend_schema_field

@extend_schema_field(serializers.CharField(help_text="Nom complet de l'utilisateur."))
def get_full_name(self, obj):
    return obj.get_full_name()
🔗 Exemple final : /api/docs
Après tout ça, ta doc sera :

✨ Interactive (essai de requêtes en direct)

🧠 Descriptive (pour chaque champ et paramètre)

🧱 Structurée (chaque endpoint clair, groupé par modèle ou vue)

🔒 Sécurisée (affiche les permissions requises automatiquement si configurées)

