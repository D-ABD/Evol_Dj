Directory structure:
└── d-abd-evol_dj.git/
    ├── README.md
    ├── asgi.py
    ├── data_backup.json
    ├── ingest.md
    ├── manage.py
    ├── projet.md
    ├── pytest.ini
    ├── requirements.txt
    ├── supervisord.conf
    ├── chat/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── views.py
    │   └── migrations/
    │       └── __init__.py
    ├── config/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── celery.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── forum/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── views.py
    │   └── migrations/
    │       └── __init__.py
    ├── journal_media/
    ├── Myevol_app/
    │   ├── __init__.py
    │   ├── api_urls.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── tasks.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── admin/
    │   │   ├── __init__.py
    │   │   ├── badge_admin.py
    │   │   ├── challenge_admin.py
    │   │   ├── event_log_admin.py
    │   │   ├── journal_admin.py
    │   │   ├── notifications_admin.py
    │   │   ├── objectives_admin.py
    │   │   ├── quote_admin.py
    │   │   ├── stats_admin.py
    │   │   ├── tasks_admin.py
    │   │   ├── user_admin.py
    │   │   └── utils_admin.py
    │   ├── api_viewsets/
    │   │   ├── __init__.py
    │   │   ├── badge_viewset.py
    │   │   ├── challenge_viewset.py
    │   │   ├── event_log_viewset.py
    │   │   ├── journal_viewset.py
    │   │   ├── notification_viewset.py
    │   │   ├── objective_viewset.py
    │   │   ├── quote_viewset.py
    │   │   ├── stats_viewset.py
    │   │   ├── user_preference_viewset.py
    │   │   └── user_viewset.py
    │   ├── fixtures/
    │   │   └── badge_templates.json
    │   ├── migrations/
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_alter_challenge_options_alter_journalmedia_options_and_more.py
    │   │   ├── 0003_alter_badgetemplate_options_badgetemplate_is_active_and_more.py
    │   │   ├── 0004_alter_challengeprogress_options_and_more.py
    │   │   ├── 0005_alter_badgetemplate_options_and_more.py
    │   │   ├── 0006_alter_journalentry_category_and_more.py
    │   │   ├── 0007_annualstat_monthlystat_and_more.py
    │   │   ├── 0008_alter_notification_options_alter_badge_date_obtenue_and_more.py
    │   │   └── __init__.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── badge_model.py
    │   │   ├── challenge_model.py
    │   │   ├── event_log_model.py
    │   │   ├── journal_model.py
    │   │   ├── notification_model.py
    │   │   ├── objective_model.py
    │   │   ├── quote_model.py
    │   │   ├── stats_model.py
    │   │   ├── user_model.py
    │   │   └── userPreference_model.py
    │   ├── serializers/
    │   │   ├── __init__.py
    │   │   ├── badge_serializers.py
    │   │   ├── challenge_serializers.py
    │   │   ├── event_log_serializers.py
    │   │   ├── journal_serializers.py
    │   │   ├── notification_serializers.py
    │   │   ├── objective_serializers.py
    │   │   ├── quote_serializers.py
    │   │   ├── stats_serializers.py
    │   │   ├── user_serializers.py
    │   │   └── userPreference_serializers.py
    │   ├── services/
    │   │   ├── badge_service.py
    │   │   ├── challenge_service.py
    │   │   ├── event_log_service.py
    │   │   ├── journal_service.py
    │   │   ├── levels_services.py
    │   │   ├── notification_service.py
    │   │   ├── objective_service.py
    │   │   ├── quote_service.py
    │   │   ├── stats_service.py
    │   │   ├── streak_service.py
    │   │   ├── user_service.py
    │   │   ├── user_stats_service.py
    │   │   └── userpreference_service.py
    │   ├── signals/
    │   │   ├── badge_signals.py
    │   │   ├── challenge_signals.py
    │   │   ├── event_log_signals.py
    │   │   ├── journal_signals.py
    │   │   ├── objective_signals.py
    │   │   ├── quote_signals.py
    │   │   ├── stats_signals.py
    │   │   ├── user_signals.py
    │   │   └── userpreference_signals.py
    │   ├── templates/
    │   │   ├── base.html
    │   │   └── myevol/
    │   │       ├── add_entry.html
    │   │       ├── add_objective.html
    │   │       ├── badge_explore.html
    │   │       ├── badge_list.html
    │   │       ├── dashboard.html
    │   │       ├── home.html
    │   │       ├── notifications.html
    │   │       ├── badges/
    │   │       │   ├── badge_explore.html
    │   │       │   └── badge_list.html
    │   │       └── users/
    │   │           ├── login.html
    │   │           └── register.html
    │   └── templatetags/
    │       ├── __init__.py
    │       └── form_tags.py
    └── tests/
        ├── __init__.py
        ├── tests_models/
        │   ├── __init__.py
        │   ├── test_badge_model.py
        │   ├── test_challenge_model.py
        │   ├── test_event_log_model.py
        │   ├── test_journal_model.py
        │   ├── test_notification_model.py
        │   ├── test_objective_model.py
        │   ├── test_preference_model.py
        │   ├── test_quote_model.py
        │   ├── test_services.py
        │   ├── test_stats_model.py
        │   └── test_user_model.py
        ├── tests_serializers/
        │   ├── __init__.py
        │   ├── test_serializers.py
        │   ├── tests_badge_serializers.py
        │   ├── tests_challenge_serializers.py
        │   ├── tests_event_log_serializers.py
        │   ├── tests_journal_serializers.py
        │   ├── tests_notification_serializers.py
        │   ├── tests_objective_serializers.py
        │   ├── tests_quote_serializers.py
        │   ├── tests_stats_serializers.py
        │   ├── tests_user_serializers.py
        │   └── tests_userPreference_serializers.py
        ├── tests_services/
        │   ├── __init__.py
        │   └── test_services.py
        ├── tests_signals/
        │   ├── __init__.py
        │   ├── test_additional_cases.py
        │   └── tests_signals.py
        └── tests_views/
            └── __init__.py


Files Content:

(Files content cropped to 300k characters, download full ingest to see more)
================================================
FILE: README.md
================================================
git add .
git commit -m " refonte des models, signaux et services + all tests ok (148 tests)"
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




================================================
FILE: asgi.py
================================================
# Evol_dj/asgi.py
import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Evol_dj.settings")
django.setup()
application = get_default_application()



================================================
FILE: data_backup.json
================================================
[{"model": "auth.permission", "pk": 1, "fields": {"name": "Can add log entry", "content_type": 1, "codename": "add_logentry"}}, {"model": "auth.permission", "pk": 2, "fields": {"name": "Can change log entry", "content_type": 1, "codename": "change_logentry"}}, {"model": "auth.permission", "pk": 3, "fields": {"name": "Can delete log entry", "content_type": 1, "codename": "delete_logentry"}}, {"model": "auth.permission", "pk": 4, "fields": {"name": "Can view log entry", "content_type": 1, "codename": "view_logentry"}}, {"model": "auth.permission", "pk": 5, "fields": {"name": "Can add permission", "content_type": 2, "codename": "add_permission"}}, {"model": "auth.permission", "pk": 6, "fields": {"name": "Can change permission", "content_type": 2, "codename": "change_permission"}}, {"model": "auth.permission", "pk": 7, "fields": {"name": "Can delete permission", "content_type": 2, "codename": "delete_permission"}}, {"model": "auth.permission", "pk": 8, "fields": {"name": "Can view permission", "content_type": 2, "codename": "view_permission"}}, {"model": "auth.permission", "pk": 9, "fields": {"name": "Can add group", "content_type": 3, "codename": "add_group"}}, {"model": "auth.permission", "pk": 10, "fields": {"name": "Can change group", "content_type": 3, "codename": "change_group"}}, {"model": "auth.permission", "pk": 11, "fields": {"name": "Can delete group", "content_type": 3, "codename": "delete_group"}}, {"model": "auth.permission", "pk": 12, "fields": {"name": "Can view group", "content_type": 3, "codename": "view_group"}}, {"model": "auth.permission", "pk": 13, "fields": {"name": "Can add content type", "content_type": 4, "codename": "add_contenttype"}}, {"model": "auth.permission", "pk": 14, "fields": {"name": "Can change content type", "content_type": 4, "codename": "change_contenttype"}}, {"model": "auth.permission", "pk": 15, "fields": {"name": "Can delete content type", "content_type": 4, "codename": "delete_contenttype"}}, {"model": "auth.permission", "pk": 16, "fields": {"name": "Can view content type", "content_type": 4, "codename": "view_contenttype"}}, {"model": "auth.permission", "pk": 17, "fields": {"name": "Can add session", "content_type": 5, "codename": "add_session"}}, {"model": "auth.permission", "pk": 18, "fields": {"name": "Can change session", "content_type": 5, "codename": "change_session"}}, {"model": "auth.permission", "pk": 19, "fields": {"name": "Can delete session", "content_type": 5, "codename": "delete_session"}}, {"model": "auth.permission", "pk": 20, "fields": {"name": "Can view session", "content_type": 5, "codename": "view_session"}}, {"model": "auth.permission", "pk": 21, "fields": {"name": "Can add user", "content_type": 6, "codename": "add_user"}}, {"model": "auth.permission", "pk": 22, "fields": {"name": "Can change user", "content_type": 6, "codename": "change_user"}}, {"model": "auth.permission", "pk": 23, "fields": {"name": "Can delete user", "content_type": 6, "codename": "delete_user"}}, {"model": "auth.permission", "pk": 24, "fields": {"name": "Can view user", "content_type": 6, "codename": "view_user"}}, {"model": "auth.permission", "pk": 25, "fields": {"name": "Can add objective", "content_type": 7, "codename": "add_objective"}}, {"model": "auth.permission", "pk": 26, "fields": {"name": "Can change objective", "content_type": 7, "codename": "change_objective"}}, {"model": "auth.permission", "pk": 27, "fields": {"name": "Can delete objective", "content_type": 7, "codename": "delete_objective"}}, {"model": "auth.permission", "pk": 28, "fields": {"name": "Can view objective", "content_type": 7, "codename": "view_objective"}}, {"model": "auth.permission", "pk": 29, "fields": {"name": "Can add journal entry", "content_type": 8, "codename": "add_journalentry"}}, {"model": "auth.permission", "pk": 30, "fields": {"name": "Can change journal entry", "content_type": 8, "codename": "change_journalentry"}}, {"model": "auth.permission", "pk": 31, "fields": {"name": "Can delete journal entry", "content_type": 8, "codename": "delete_journalentry"}}, {"model": "auth.permission", "pk": 32, "fields": {"name": "Can view journal entry", "content_type": 8, "codename": "view_journalentry"}}, {"model": "auth.permission", "pk": 33, "fields": {"name": "Can add badge template", "content_type": 9, "codename": "add_badgetemplate"}}, {"model": "auth.permission", "pk": 34, "fields": {"name": "Can change badge template", "content_type": 9, "codename": "change_badgetemplate"}}, {"model": "auth.permission", "pk": 35, "fields": {"name": "Can delete badge template", "content_type": 9, "codename": "delete_badgetemplate"}}, {"model": "auth.permission", "pk": 36, "fields": {"name": "Can view badge template", "content_type": 9, "codename": "view_badgetemplate"}}, {"model": "auth.permission", "pk": 37, "fields": {"name": "Can add badge", "content_type": 10, "codename": "add_badge"}}, {"model": "auth.permission", "pk": 38, "fields": {"name": "Can change badge", "content_type": 10, "codename": "change_badge"}}, {"model": "auth.permission", "pk": 39, "fields": {"name": "Can delete badge", "content_type": 10, "codename": "delete_badge"}}, {"model": "auth.permission", "pk": 40, "fields": {"name": "Can view badge", "content_type": 10, "codename": "view_badge"}}, {"model": "auth.permission", "pk": 41, "fields": {"name": "Can add notification", "content_type": 11, "codename": "add_notification"}}, {"model": "auth.permission", "pk": 42, "fields": {"name": "Can change notification", "content_type": 11, "codename": "change_notification"}}, {"model": "auth.permission", "pk": 43, "fields": {"name": "Can delete notification", "content_type": 11, "codename": "delete_notification"}}, {"model": "auth.permission", "pk": 44, "fields": {"name": "Can view notification", "content_type": 11, "codename": "view_notification"}}, {"model": "contenttypes.contenttype", "pk": 1, "fields": {"app_label": "admin", "model": "logentry"}}, {"model": "contenttypes.contenttype", "pk": 2, "fields": {"app_label": "auth", "model": "permission"}}, {"model": "contenttypes.contenttype", "pk": 3, "fields": {"app_label": "auth", "model": "group"}}, {"model": "contenttypes.contenttype", "pk": 4, "fields": {"app_label": "contenttypes", "model": "contenttype"}}, {"model": "contenttypes.contenttype", "pk": 5, "fields": {"app_label": "sessions", "model": "session"}}, {"model": "contenttypes.contenttype", "pk": 6, "fields": {"app_label": "Myevol_app", "model": "user"}}, {"model": "contenttypes.contenttype", "pk": 7, "fields": {"app_label": "Myevol_app", "model": "objective"}}, {"model": "contenttypes.contenttype", "pk": 8, "fields": {"app_label": "Myevol_app", "model": "journalentry"}}, {"model": "contenttypes.contenttype", "pk": 9, "fields": {"app_label": "Myevol_app", "model": "badgetemplate"}}, {"model": "contenttypes.contenttype", "pk": 10, "fields": {"app_label": "Myevol_app", "model": "badge"}}, {"model": "contenttypes.contenttype", "pk": 11, "fields": {"app_label": "Myevol_app", "model": "notification"}}, {"model": "sessions.session", "pk": "7go2ji89957ey1wg8qa9obnaqzuf8sd9", "fields": {"session_data": ".eJxVjEEOwiAQRe_C2pAMDIW6dO8ZyDADUjU0Ke3KeHdt0oVu_3vvv1Skba1x63mJk6izAnX63RLxI7cdyJ3abdY8t3WZkt4VfdCur7Pk5-Vw_w4q9fqtLSRmg4mSBPQDgAuOHAUPZMV5YvAEJRkraPLIWEK2kv0wWiRbENX7A-gqN_g:1u2yQh:wJxroG6fi3TKHbWu0w3xGHeUXg9ZbAq4k47ql3HnpNg", "expire_date": "2025-04-24T20:23:19.742Z"}}, {"model": "Myevol_app.user", "pk": 1, "fields": {"password": "pbkdf2_sha256$600000$bdbVEKYnxOKDGQb9Syt10a$xi4fAp1H1ePVTJSzMcnOUP3GA71vMMRe7ADGkFHWZnM=", "last_login": "2025-04-10T20:23:19.739Z", "is_superuser": true, "username": "ABD", "first_name": "", "last_name": "", "is_staff": true, "is_active": true, "date_joined": "2025-04-10T19:19:21.971Z", "email": "abdouldiatta@gmail.com", "groups": [], "user_permissions": []}}, {"model": "Myevol_app.journalentry", "pk": 1, "fields": {"user": 1, "content": "azerty", "mood": 6, "category": "rest", "created_at": "2025-04-11T21:03:08.679Z"}}, {"model": "Myevol_app.badge", "pk": 1, "fields": {"name": "Première entrée", "description": "Bravo pour ta première entrée 🎉", "icon": "🌱", "user": 1, "date_obtenue": "2025-04-11"}}, {"model": "Myevol_app.badge", "pk": 2, "fields": {"name": "Niveau 1", "description": "Tu as atteint le niveau 1 💪", "icon": "🏆", "user": 1, "date_obtenue": "2025-04-11"}}, {"model": "Myevol_app.badgetemplate", "pk": 1, "fields": {"name": "Première entrée", "description": "Bravo pour ta première entrée 🎉", "icon": "🌱", "condition": "Créer une première entrée de journal"}}, {"model": "Myevol_app.badgetemplate", "pk": 2, "fields": {"name": "7 jours d'activité", "description": "1 semaine d'activité, continue comme ça 🚀", "icon": "🔥", "condition": "Ajouter au moins 1 entrée par jour pendant 7 jours"}}, {"model": "Myevol_app.badgetemplate", "pk": 3, "fields": {"name": "Niveau 1", "description": "Tu as atteint le niveau 1 💪", "icon": "🏆", "condition": "Atteindre le niveau 1 (1 entrée)"}}, {"model": "Myevol_app.badgetemplate", "pk": 4, "fields": {"name": "Niveau 2", "description": "Tu as atteint le niveau 2 💪", "icon": "🏆", "condition": "Atteindre le niveau 2 (5 entrées)"}}, {"model": "Myevol_app.badgetemplate", "pk": 5, "fields": {"name": "Niveau 3", "description": "Tu as atteint le niveau 3 💪", "icon": "🏆", "condition": "Atteindre le niveau 3 (10 entrées)"}}, {"model": "Myevol_app.notification", "pk": 1, "fields": {"user": 1, "message": "🎉 Nouveau badge : Première entrée !", "is_read": true, "created_at": "2025-04-11T21:03:08.739Z"}}, {"model": "Myevol_app.notification", "pk": 2, "fields": {"user": 1, "message": "🏆 Félicitations, tu as atteint le Niveau 1 !", "is_read": true, "created_at": "2025-04-11T21:03:08.767Z"}}]


================================================
FILE: ingest.md
================================================



================================================
FILE: manage.py
================================================
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



================================================
FILE: projet.md
================================================



================================================
FILE: pytest.ini
================================================
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = test_*.py  # Fichiers de test (commençant par "test_")
testpaths = tests         # Dossier racine des tests
norecursedirs = .venv __pycache__  # Dossiers ignorés


================================================
FILE: requirements.txt
================================================
amqp==5.3.1
asgiref==3.8.1
async-timeout==5.0.1
attrs==25.3.0
billiard==4.2.1
celery==5.5.1
channels==4.2.2
channels_redis==4.2.1
click==8.1.8
click-didyoumean==0.3.1
click-plugins==1.1.1
click-repl==0.3.0
cron-descriptor==1.4.5
Django==4.2.20
django-celery-beat==2.8.0
django-cors-headers==4.7.0
django-timezone-field==7.1
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
drf-spectacular==0.28.0
exceptiongroup==1.2.2
flower==2.0.1
freezegun==1.5.1
humanize==4.12.2
inflection==0.5.1
iniconfig==2.1.0
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
kombu==5.5.3
msgpack==1.1.0
packaging==25.0
pluggy==1.5.0
prometheus_client==0.21.1
prompt_toolkit==3.0.51
psycopg2-binary==2.9.10
PyJWT==2.9.0
pytest==8.3.5
pytest-django==4.11.1
python-crontab==3.2.0
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
pytz==2025.2
PyYAML==6.0.2
redis==5.2.1
referencing==0.36.2
rpds-py==0.24.0
six==1.17.0
sqlparse==0.5.3
tomli==2.2.1
tornado==6.4.2
typing_extensions==4.13.2
tzdata==2025.2
uritemplate==4.1.1
vine==5.1.0
wcwidth==0.2.13



================================================
FILE: supervisord.conf
================================================
[program:celery_worker]
directory=/path/to/your/project
command=/path/to/your/venv/bin/celery -A config worker --loglevel=info
autostart=true
autorestart=true
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker_error.log
user=your_linux_user
numprocs=1
priority=998
environment=DJANGO_SETTINGS_MODULE="config.settings"

[program:celery_beat]
directory=/path/to/your/project
command=/path/to/your/venv/bin/celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
autostart=true
autorestart=true
stdout_logfile=/var/log/celery/beat.log
stderr_logfile=/var/log/celery/beat_error.log
user=your_linux_user
numprocs=1
priority=999
environment=DJANGO_SETTINGS_MODULE="config.settings"



================================================
FILE: chat/__init__.py
================================================



================================================
FILE: chat/admin.py
================================================
from django.contrib import admin

# Register your models here.



================================================
FILE: chat/apps.py
================================================
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'



================================================
FILE: chat/models.py
================================================
# chat/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.sender} à {self.recipient} : {self.content[:20]}"



================================================
FILE: chat/tests.py
================================================
from django.test import TestCase

# Create your tests here.



================================================
FILE: chat/views.py
================================================
from django.shortcuts import render

# Create your views here.



================================================
FILE: chat/migrations/__init__.py
================================================



================================================
FILE: config/__init__.py
================================================
from __future__ import absolute_import, unicode_literals

# Initialise celery à l’import du projet
from .celery import app as celery_app

__all__ = ("celery_app",)



================================================
FILE: config/asgi.py
================================================
"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()



================================================
FILE: config/celery.py
================================================
import os
from celery import Celery

# Indique à Django d'utiliser le bon fichier settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Nom du projet ici = "config"
app = Celery("config")

# Charger les paramètres de settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Cherche automatiquement les tâches dans les apps
app.autodiscover_tasks()
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'



================================================
FILE: config/settings.py
================================================
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k%s35+y)-2%f2sft$2et#0$=6yt)q_)uxyb14x$+@jfzqf5fi)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Myevol_app',
    'django_celery_beat',
    'rest_framework',
    'corsheaders',  # pour autoriser l'accès depuis Expo
    'rest_framework_simplejwt',
    'rest_framework.authtoken',  # seulement si tu veux aussi gérer des tokens classiques




]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True  # à restreindre en prod
CORS_ALLOW_CREDENTIALS = True  # pour les cookies d'authentification

ROOT_URLCONF = 'config.urls'


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



import os
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()

# Configuration de la base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_TZ = True
USE_I18N = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'Myevol_app.User'

LOGIN_URL = 'myevol:login'
LOGIN_REDIRECT_URL = 'myevol:dashboard'
LOGOUT_REDIRECT_URL = 'myevol:login'

# CELERY CONFIG
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Assure-toi que Redis tourne
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    # 🔔 Envoyer la question "Qu'as-tu fait aujourd'hui ?" tous les jours à 19h
    'ask_user_daily_activity': {
        'task': 'Myevol_app.tasks.ask_user_daily_activity',
        'schedule': crontab(hour=19, minute=0),
    },

    # 📊 Générer statistiques journalières tous les jours à minuit
    'generate_daily_stats': {
        'task': 'Myevol_app.tasks.generate_all_daily_stats',
        'schedule': crontab(hour=0, minute=0),
    },

    # 📈 Générer statistiques hebdomadaires chaque lundi à 9h
    'generate_weekly_stats': {
        'task': 'Myevol_app.tasks.generate_all_weekly_stats',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # 1 = lundi
    },

    # 📅 Générer statistiques mensuelles le 1er du mois à 9h
    'generate_monthly_stats': {
        'task': 'Myevol_app.tasks.generate_all_monthly_stats',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),
    },

    # 🗓️ Générer statistiques annuelles le 1er janvier à 9h
    'generate_annual_stats': {
        'task': 'Myevol_app.tasks.generate_all_annual_stats',
        'schedule': crontab(hour=9, minute=0, day_of_month=1, month_of_year=1),
    },

    # 🧹 Nettoyer les anciennes notifications (> 90 jours) tous les jours à 3h du matin
    'clean_old_notifications': {
        'task': 'Myevol_app.tasks.clean_old_notifications',
        'schedule': crontab(hour=3, minute=0),
    },

    # 🧠 Vérifier/Recalculer les streaks tous les jours à 0h30
    'update_user_streaks': {
        'task': 'Myevol_app.tasks.recalculate_all_streaks',
        'schedule': crontab(hour=0, minute=30),
    },

    # 🚨 Envoyer un rappel s’il n’y a pas eu d'entrée depuis X jours (ex: tous les jours à 18h)
    'remind_inactive_users': {
        'task': 'Myevol_app.tasks.remind_inactive_users',
        'schedule': crontab(hour=18, minute=0),
    },
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Par exemple 10 badges par page
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'MyEvol API',
    'DESCRIPTION': 'Documentation complète de l’API MyEvol pour l’application mobile.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # ou INFO
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
DEFAULT_ADMIN_EMAIL = "admin@monapp.com"



================================================
FILE: config/urls.py
================================================
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Myevol_app.urls')),  # <== ici
]






================================================
FILE: config/wsgi.py
================================================
"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()



================================================
FILE: forum/__init__.py
================================================



================================================
FILE: forum/admin.py
================================================
from django.contrib import admin

# Register your models here.



================================================
FILE: forum/apps.py
================================================
from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum'



================================================
FILE: forum/models.py
================================================
# forum/models.py

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.author} dans {self.thread}"



================================================
FILE: forum/tests.py
================================================
from django.test import TestCase

# Create your tests here.



================================================
FILE: forum/views.py
================================================
from django.shortcuts import render

# Create your views here.



================================================
FILE: forum/migrations/__init__.py
================================================




================================================
FILE: Myevol_app/__init__.py
================================================



================================================
FILE: Myevol_app/api_urls.py
================================================



================================================
FILE: Myevol_app/apps.py
================================================
from django.apps import AppConfig

class MyevolAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Myevol_app'

    def ready(self):
        import Myevol_app.signals.badge_signals
        import Myevol_app.signals.challenge_signals
        import Myevol_app.signals.event_log_signals
        import Myevol_app.signals.journal_signals
        import Myevol_app.signals.objective_signals
        import Myevol_app.signals.quote_signals
        import Myevol_app.signals.stats_signals
        import Myevol_app.signals.user_signals
        import Myevol_app.signals.userpreference_signals



================================================
FILE: Myevol_app/forms.py
================================================



================================================
FILE: Myevol_app/tasks.py
================================================
# tasks.py
from celery import shared_task
from django.utils.timezone import now
from .models import Notification, User
from .services import stats_service, streak_service, notification_service
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task
def send_scheduled_notifications():
    """
    Tâche pour envoyer toutes les notifications programmées.
    """
    logger.info("Scheduled notifications task executed.")
    return "Scheduled notifications sent."

@shared_task
def generate_all_daily_stats():
    """
    Génère les statistiques journalières pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_daily_stats(user)
    return "Statistiques journalières générées."

@shared_task
def generate_all_weekly_stats():
    """
    Génère les statistiques hebdomadaires pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_weekly_stats(user)
    return "Statistiques hebdomadaires générées."

@shared_task
def generate_all_monthly_stats():
    """
    Génère les statistiques mensuelles pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_monthly_stats(user)
    return "Statistiques mensuelles générées."

@shared_task
def generate_all_annual_stats():
    """
    Génère les statistiques annuelles pour tous les utilisateurs.
    """
    for user in User.objects.all():
        stats_service.generate_annual_stats(user)
    return "Statistiques annuelles générées."

@shared_task
def recalculate_all_streaks():
    """
    Recalcule les streaks (séries d'entrées consécutives) de tous les utilisateurs.
    """
    for user in User.objects.all():
        streak_service.update_user_streak(user)
    return "Séries (streaks) mises à jour."

@shared_task
def remind_inactive_users():
    """
    Envoie un rappel aux utilisateurs sans activité récente.
    """
    threshold = now() - timedelta(days=2)  # Ex : pas d'entrée depuis 2 jours
    for user in User.objects.all():
        if not user.entries.filter(created_at__gte=threshold).exists():
            notification_service.create_user_notification(
                user=user,
                message="N'oubliez pas d'écrire dans votre journal aujourd'hui 📖",
                notif_type="journal_reminder"
            )
    return "Rappels envoyés aux utilisateurs inactifs."

@shared_task
def clean_old_notifications():
    """
    Supprime les anciennes notifications de plus de 90 jours.
    """
    cutoff = now() - timedelta(days=90)
    count, _ = Notification.objects.filter(created_at__lt=cutoff).delete()
    return f"{count} anciennes notifications supprimées."

@shared_task
def ask_user_daily_activity():
    """
    Demande quotidienne aux utilisateurs de réfléchir à leur journée à 19h.
    """
    for user in User.objects.all():
        notification_service.create_user_notification(
            user=user,
            message="Qu'avez-vous accompli aujourd'hui ? Prenez un moment pour écrire dans votre journal. ✍️",
            notif_type="journal_prompt"
        )
    return "Notifications de réflexion journalière envoyées."



================================================
FILE: Myevol_app/urls.py
================================================
from django.urls import path
from . import views

app_name = "myevol"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-entry/', views.add_entry_view, name='add_entry'),
    path('add-objective/', views.add_objective_view, name='add_objective'),
    path('badges/', views.badge_list_view, name='badge_list'),
    path('badges/explorer/', views.badge_explore_view, name='badge_explore'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('logout/', views.logout_view, name='logout'),  # à ajuster selon auth
]



================================================
FILE: Myevol_app/views.py
================================================
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def home_view(request):
    return render(request, "myevol/home.html")

def dashboard_view(request):
    return render(request, "myevol/dashboard.html")

def add_entry_view(request):
    return render(request, "myevol/add_entry.html")

def add_objective_view(request):
    return render(request, "myevol/add_objective.html")

def badge_list_view(request):
    return render(request, "myevol/badge_list.html")

def badge_explore_view(request):
    return render(request, "myevol/badge_explore.html")

def notifications_view(request):
    return render(request, "myevol/notifications.html")

def logout_view(request):
    logout(request)
    return redirect("myevol:home")



================================================
FILE: Myevol_app/admin/__init__.py
================================================



================================================
FILE: Myevol_app/admin/badge_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 🏅 Gestion des badges =====
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_link', 'icon_display', 'date_obtenue', 'level', 'is_new')
    list_filter = ('name', 'date_obtenue', 'level')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    date_hierarchy = 'date_obtenue'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur personnalisé"""
        if obj.user:
            url = reverse("admin:Myevol_app_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"

    
    def icon_display(self, obj):
        """Affiche l'icône du badge"""
        return format_html('<span style="font-size: 1.5em;">{}</span>', obj.icon)
    icon_display.short_description = "Icône"
    
    def is_new(self, obj):
        """Indique si le badge a été obtenu aujourd'hui"""
        return obj.was_earned_today()
    is_new.boolean = True
    is_new.short_description = "Nouveau"


@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_display', 'level', 'condition', 'badges_count')
    list_filter = ('level',)
    search_fields = ('name', 'description', 'condition')
    
    def icon_display(self, obj):
        """Affiche l'icône du template de badge"""
        return format_html('<span style="font-size: 1.5em; color: {};">{}</span>', 
                           obj.color_theme, obj.icon)
    icon_display.short_description = "Icône"
    
    def badges_count(self, obj):
        """Nombre de badges attribués de ce type"""
        return Badge.objects.filter(name=obj.name).count()
    badges_count.short_description = "Badges attribués"




================================================
FILE: Myevol_app/admin/challenge_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 🎯 Gestion des défis =====
class ChallengeProgressInline(admin.TabularInline):
    model = ChallengeProgress
    extra = 0
    readonly_fields = ('user', 'completed', 'completed_at')
    fields = ('user', 'completed', 'completed_at')
    can_delete = False
    max_num = 20
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'target_entries', 'is_active_now', 'days_left', 'participants_count')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    inlines = [ChallengeProgressInline]
    
    def is_active_now(self, obj):
        """Vérifie si le défi est actuellement actif"""
        return obj.is_active()
    is_active_now.boolean = True
    is_active_now.short_description = "Actif"
    
    def days_left(self, obj):
        """Jours restants avant la fin du défi"""
        days = obj.days_remaining()
        if days <= 0:
            return "Terminé"
        return f"{days} jour{'s' if days > 1 else ''}"
    days_left.short_description = "Jours restants"
    
    def participants_count(self, obj):
        """Nombre d'utilisateurs participant au défi"""
        return obj.progresses.count()
    participants_count.short_description = "Participants"


@admin.register(ChallengeProgress)
class ChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge_link', 'completed', 'completed_at', 'progress_percent')
    list_filter = ('completed', 'completed_at', 'challenge')
    search_fields = ('user__username', 'user__email', 'challenge__title')
    date_hierarchy = 'completed_at'
    raw_id_fields = ('user', 'challenge')
    
    def challenge_link(self, obj):
        """Affiche un lien vers l'admin du défi"""
        url = reverse("admin:core_challenge_change", args=[obj.challenge.id])
        return format_html('<a href="{}">{}</a>', url, obj.challenge.title)
    challenge_link.short_description = "Défi"
    
    def progress_percent(self, obj):
        """Affiche le pourcentage de progression"""
        progress = obj.get_progress()
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px;">'
            '<div style="width: {}%; background-color: #4CAF50; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            progress['percent'], progress['percent'])
    progress_percent.short_description = "Progression"





================================================
FILE: Myevol_app/admin/event_log_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 📝 Gestion des logs d'événements =====
@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_link', 'action', 'description_preview', 'has_metadata')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'user__email', 'action', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'user', 'action', 'description', 'metadata_formatted')
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        if obj.user:
            url = reverse("admin:auth_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = "Utilisateur"
    
    def description_preview(self, obj):
        """Affiche un aperçu de la description"""
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description
    description_preview.short_description = "Description"
    
    def has_metadata(self, obj):
        """Indique si le log contient des métadonnées"""
        return obj.metadata is not None and bool(obj.metadata)
    has_metadata.boolean = True
    has_metadata.short_description = "Métadonnées"
    
    def metadata_formatted(self, obj):
        """Affiche les métadonnées formatées en JSON"""
        if not obj.metadata:
            return "-"
        import json
        return format_html('<pre>{}</pre>', json.dumps(obj.metadata, indent=2))
    metadata_formatted.short_description = "Métadonnées"






================================================
FILE: Myevol_app/admin/journal_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 📝 Gestion du journal =====
class JournalMediaInline(admin.TabularInline):
    model = JournalMedia
    extra = 0
    fields = ('file', 'type', 'created_at', 'preview')
    readonly_fields = ('created_at', 'preview')
    
    def preview(self, obj):
        """Affiche un aperçu du média"""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 300px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'display_date', 'mood_with_emoji', 'category', 'content_preview')
    list_filter = ('mood', 'category', 'created_at')
    search_fields = ('content', 'user__username', 'user__email', 'category')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    inlines = [JournalMediaInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def display_date(self, obj):
        """Affiche la date de création formatée"""
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    display_date.short_description = "Date"
    
    def mood_with_emoji(self, obj):
        """Affiche l'humeur avec son emoji correspondant"""
        return format_html('{} <span style="font-size: 1.2em;">{}</span>', 
                           obj.mood, obj.get_mood_emoji())
    mood_with_emoji.short_description = "Humeur"
    
    def content_preview(self, obj):
        """Affiche un aperçu du contenu"""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = "Contenu"


@admin.register(JournalMedia)
class JournalMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry_link', 'type', 'file_size_display', 'created_at', 'preview')
    list_filter = ('type', 'created_at')
    search_fields = ('entry__content', 'entry__user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'preview')
    
    def entry_link(self, obj):
        """Affiche un lien vers l'admin de l'entrée"""
        url = reverse("admin:core_journalentry_change", args=[obj.entry.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.entry))
    entry_link.short_description = "Entrée"
    
    def file_size_display(self, obj):
        """Affiche la taille du fichier en format lisible"""
        size = obj.file_size()
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.1f} MB"
    file_size_display.short_description = "Taille"
    
    def preview(self, obj):
        """Affiche un aperçu du média"""
        if obj.type == 'image' and obj.file:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 400px;" />', obj.file.url)
        elif obj.type == 'audio' and obj.file:
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        return "-"
    preview.short_description = "Aperçu"




================================================
FILE: Myevol_app/admin/notifications_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 🔔 Gestion des notifications =====
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'notif_type_display', 'message_preview', 'is_read', 'archived', 'created_at')
    list_filter = ('notif_type', 'is_read', 'archived', 'created_at')
    search_fields = ('message', 'user__username', 'user__email')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    actions = ['mark_as_read', 'mark_as_unread', 'archive_notifications']
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def notif_type_display(self, obj):
        """Affiche le type de notification avec une couleur distinctive"""
        colors = {
            'badge': '#9C27B0',
            'objectif': '#4CAF50',
            'statistique': '#2196F3',
            'info': '#607D8B'
        }
        return format_html('<span style="color: {};">{}</span>', 
                          colors.get(obj.notif_type, 'black'), obj.type_display)
    notif_type_display.short_description = "Type"
    
    def message_preview(self, obj):
        """Affiche un aperçu du message"""
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = "Message"
    
    def mark_as_read(self, request, queryset):
        """Action pour marquer les notifications comme lues"""
        updated = queryset.update(is_read=True, read_at=now())
        self.message_user(request, f"{updated} notification(s) marquée(s) comme lue(s).")
    mark_as_read.short_description = "Marquer comme lues"
    
    def mark_as_unread(self, request, queryset):
        """Action pour marquer les notifications comme non lues"""
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f"{updated} notification(s) marquée(s) comme non lue(s).")
    mark_as_unread.short_description = "Marquer comme non lues"
    
    def archive_notifications(self, request, queryset):
        """Action pour archiver les notifications"""
        updated = queryset.update(archived=True)
        self.message_user(request, f"{updated} notification(s) archivée(s).")
    archive_notifications.short_description = "Archiver les notifications"




================================================
FILE: Myevol_app/admin/objectives_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 🎯 Gestion des objectifs =====
@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_link', 'category', 'target_date', 'done_status', 'progress_display')
    list_filter = ('done', 'category', 'target_date')
    search_fields = ('title', 'user__username', 'user__email', 'category')
    date_hierarchy = 'target_date'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def done_status(self, obj):
        """Affiche l'état de complétion de l'objectif"""
        if obj.done:
            return format_html('<span style="color: green;">✓ Terminé</span>')
        elif obj.is_overdue():
            return format_html('<span style="color: red;">⚠ En retard</span>')
        else:
            return format_html('<span style="color: orange;">⏳ En cours</span>')
    done_status.short_description = "État"
    
    def progress_display(self, obj):
        """Affiche la progression de l'objectif sous forme de barre"""
        progress = obj.progress()
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px;">'
            '<div style="width: {}%; background-color: {}; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            progress, '#4CAF50' if progress == 100 else '#2196F3', progress)
    progress_display.short_description = "Progression"





================================================
FILE: Myevol_app/admin/quote_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 📜 Gestion des citations =====
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_preview', 'author', 'mood_tag', 'length_display')
    list_filter = ('mood_tag', 'author')
    search_fields = ('text', 'author')
    
    def quote_preview(self, obj):
        """Affiche un aperçu de la citation"""
        if len(obj.text) > 70:
            return f'"{obj.text[:70]}..."'
        return f'"{obj.text}"'
    quote_preview.short_description = "Citation"
    
    def length_display(self, obj):
        """Affiche la longueur de la citation avec une indication visuelle"""
        length = obj.length()
        if length < 50:
            category = "Courte"
            color = "#8BC34A"
        elif length < 120:
            category = "Moyenne"
            color = "#FFC107"
        else:
            category = "Longue"
            color = "#FF9800"
        
        return format_html('<span style="color: {};">{} ({} caractères)</span>', 
                          color, category, length)
    length_display.short_description = "Longueur"





================================================
FILE: Myevol_app/admin/stats_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)


# ===== 📊 Gestion des statistiques =====
@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = ('date', 'user_link', 'entries_count', 'mood_average_display', 'day_of_week_display', 'categories_preview')
    list_filter = ('date',)
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'date'
    raw_id_fields = ('user',)
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def mood_average_display(self, obj):
        """Affiche la moyenne d'humeur avec une couleur indicative"""
        if obj.mood_average is None:
            return "-"
        
        color = "#CCCCCC"  # Gris par défaut
        if obj.mood_average >= 8:
            color = "#4CAF50"  # Vert
        elif obj.mood_average >= 6:
            color = "#8BC34A"  # Vert clair
        elif obj.mood_average >= 4:
            color = "#FFC107"  # Ambre
        elif obj.mood_average >= 2:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Rouge
            
        return format_html('<span style="color: {}; font-weight: bold;">{:.1f}</span>', 
                           color, obj.mood_average)
    mood_average_display.short_description = "Humeur moyenne"
    
    def day_of_week_display(self, obj):
        """Affiche le jour de la semaine avec mise en évidence du weekend"""
        day = obj.day_of_week()
        is_weekend = obj.is_weekend()
        return format_html('<span style="{}font-weight: {};">{}</span>', 
                          'color: #E91E63; ' if is_weekend else '', 
                          'bold' if is_weekend else 'normal', 
                          day)
    day_of_week_display.short_description = "Jour"
    
    def categories_preview(self, obj):
        """Affiche un aperçu des catégories utilisées"""
        if not obj.categories:
            return "-"
        
        # Limiter à 3 catégories maximum pour l'affichage
        cats = list(obj.categories.items())
        if len(cats) <= 3:
            return ", ".join([f"{cat}: {count}" for cat, count in cats])
        else:
            preview = ", ".join([f"{cat}: {count}" for cat, count in cats[:3]])
            return f"{preview}, ... (+{len(cats)-3})"
    categories_preview.short_description = "Catégories"


@admin.register(WeeklyStat)
class WeeklyStatAdmin(admin.ModelAdmin):
    list_display = ('week_display', 'user_link', 'entries_count', 'mood_average_display', 'top_category_display')
    list_filter = ('week_start',)
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'week_start'
    raw_id_fields = ('user',)
    
    def week_display(self, obj):
        """Affiche la semaine de façon lisible"""
        return f"Semaine {obj.week_number()} ({obj.week_start.strftime('%d/%m')} - {obj.week_end().strftime('%d/%m/%Y')})"
    week_display.short_description = "Semaine"
    
    def user_link(self, obj):
        """Affiche un lien vers l'admin de l'utilisateur"""
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = "Utilisateur"
    
    def mood_average_display(self, obj):
        """Affiche la moyenne d'humeur avec une couleur indicative"""
        if obj.mood_average is None:
            return "-"
        
        color = "#CCCCCC"  # Gris par défaut
        if obj.mood_average >= 8:
            color = "#4CAF50"  # Vert
        elif obj.mood_average >= 6:
            color = "#8BC34A"  # Vert clair
        elif obj.mood_average >= 4:
            color = "#FFC107"  # Ambre
        elif obj.mood_average >= 2:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Rouge
            
        return format_html('<span style="color: {}; font-weight: bold;">{:.1f}</span>', 
                           color, obj.mood_average)
    mood_average_display.short_description = "Humeur moyenne"
    
    def top_category_display(self, obj):
        """Affiche la catégorie la plus fréquente avec le compte"""
        top = obj.top_category()
        if not top:
            return "-"
        count = obj.categories.get(top, 0)
        return f"{top} ({count})"
    top_category_display.short_description = "Catégorie principale"





================================================
FILE: Myevol_app/admin/tasks_admin.py
================================================
from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
    ClockedSchedule
)
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from celery import current_app


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'interval', 'crontab', 'solar', 'clocked', 'enabled', 'last_run_at', 'one_off', 'start_time', 'expire_seconds', 'run_now_link')
    list_filter = ('enabled', 'task', 'crontab', 'interval', 'solar', 'clocked')
    search_fields = ('name', 'task')
    ordering = ('-last_run_at',)
    readonly_fields = ('last_run_at', 'total_run_count')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('run-now/<int:pk>/', self.admin_site.admin_view(self.run_now_view), name='periodictask_run_now'),
        ]
        return custom_urls + urls

    def run_now_link(self, obj):
        return format_html(
            '<a class="button" href="{}">▶️ Exécuter maintenant</a>',
            f'run-now/{obj.pk}/'
        )
    run_now_link.short_description = "Action immédiate"
    run_now_link.allow_tags = True

    def run_now_view(self, request, pk, *args, **kwargs):
        task = PeriodicTask.objects.get(pk=pk)
        try:
            current_app.send_task(task.task)
            self.message_user(request, f"Tâche {task.name} déclenchée avec succès ✅", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Erreur lors du lancement : {e}", messages.ERROR)
        return redirect('admin:django_celery_beat_periodictask_changelist')


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')
    search_fields = ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(admin.ModelAdmin):
    list_display = ('every', 'period')
    search_fields = ('every', 'period')


@admin.register(SolarSchedule)
class SolarScheduleAdmin(admin.ModelAdmin):
    list_display = ('event', 'latitude', 'longitude')
    search_fields = ('event',)


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(admin.ModelAdmin):
    list_display = ('clocked_time',)
    search_fields = ('clocked_time',)



================================================
FILE: Myevol_app/admin/user_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)




# ===== 👤 Gestion des utilisateurs et préférences =====
class UserPreferenceInline(admin.StackedInline):
    model = UserPreference
    can_delete = False
    fieldsets = (
        ('Notifications', {
            'fields': (('notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique'),)
        }),
        ('Apparence', {
            'fields': (('dark_mode', 'accent_color'), ('font_choice', 'enable_animations'))
        }),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'date_joined', 'level_display', 'entries_count', 'streak_display')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login', 'entries_count', 'current_streak', 'mood_avg', 'badges_count')
    inlines = [UserPreferenceInline]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'avatar_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Statistiques', {'fields': ('entries_count', 'current_streak', 'longest_streak', 'xp', 'mood_avg', 'badges_count')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    def full_name(self, obj):
        """Retourne le nom complet de l'utilisateur"""
        return obj.get_full_name() or "-"
    full_name.short_description = "Nom complet"
    
    def entries_count(self, obj):
        """Nombre total d'entrées de journal"""
        return obj.total_entries()
    entries_count.short_description = "Entrées"
    
    def current_streak(self, obj):
        """Série actuelle de jours consécutifs"""
        return obj.current_streak()
    current_streak.short_description = "Série actuelle"
    
    def mood_avg(self, obj):
        """Moyenne d'humeur sur les 7 derniers jours"""
        avg = obj.mood_average(7)
        if avg is None:
            return "-"
        return f"{avg:.1f}/10"
    mood_avg.short_description = "Humeur (7j)"
    
    def badges_count(self, obj):
        """Nombre de badges obtenus"""
        return obj.badges.count()
    badges_count.short_description = "Badges"
    
    def level_display(self, obj):
        """Affiche le niveau avec une barre visuelle"""
        level = obj.level
        from ..utils.levels import get_user_progress
        progress = get_user_progress(obj.total_entries())
        
        return format_html(
            '<div><strong>Niveau {}</strong></div>'
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 4px; margin-top: 2px;">'
            '<div style="width: {}%; background-color: #673AB7; color: white; text-align: center; border-radius: 4px;">'
            '{:.0f}%</div></div>',
            level, progress["progress"], progress["progress"])
    level_display.short_description = "Niveau"
    
    def streak_display(self, obj):
        """Affiche les séries de jours consécutifs"""
        current = obj.current_streak()
        longest = obj.longest_streak
        
        if current == 0:
            return "Aucune série active"
        
        if current == longest:
            return format_html('<span style="color: #4CAF50; font-weight: bold;">{} jour(s) 🔥</span>', current)
        
        return format_html('Actuelle: <span style="color: #2196F3;">{}</span> | '
                          'Record: <span style="color: #4CAF50;">{}</span>', 
                          current, longest)
    streak_display.short_description = "Séries"


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'notifications_enabled', 'accent_color_display', 'font_choice')
    list_filter = ('dark_mode', 'notif_badge', 'notif_objectif', 'notif_info', 'notif_statistique', 'font_choice')
    search_fields = ('user__username', 'user__email')
    actions = ['reset_to_defaults']
    
    def notifications_enabled(self, obj):
        """Affiche quelles notifications sont activées"""
        enabled = []
        if obj.notif_badge:
            enabled.append("Badge")
        if obj.notif_objectif:
            enabled.append("Objectif")
        if obj.notif_info:
            enabled.append("Info")
        if obj.notif_statistique:
            enabled.append("Statistique")
            
        if not enabled:
            return format_html('<span style="color: #F44336;">Aucune</span>')
        elif len(enabled) == 4:
            return format_html('<span style="color: #4CAF50;">Toutes</span>')
        else:
            return ", ".join(enabled)
    notifications_enabled.short_description = "Notifications"
    
    def accent_color_display(self, obj):
        """Affiche la couleur d'accent avec un échantillon visuel"""
        return format_html(
            '<div style="display: inline-block; width: 20px; height: 20px; background-color: {}; '
            'border-radius: 50%; vertical-align: middle; margin-right: 5px;"></div> {}',
            obj.accent_color, obj.accent_color)
    accent_color_display.short_description = "Couleur d'accent"
    
    def reset_to_defaults(self, request, queryset):
        """Action pour réinitialiser les préférences aux valeurs par défaut"""
        for pref in queryset:
            pref.reset_to_defaults()
        self.message_user(request, f"{queryset.count()} préférence(s) réinitialisée(s) avec succès.")
    reset_to_defaults.short_description = "Réinitialiser aux valeurs par défaut"





================================================
FILE: Myevol_app/admin/utils_admin.py
================================================
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)

# Configuration des groupes d'administration
admin.site.site_header = "Administration MyEvol"
admin.site.site_title = "MyEvol Admin"
admin.site.index_title = "Tableau de bord d'administration"

# Organisation des modèles par sections dans l'admin
class MyEvolAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Organise les modèles par groupes fonctionnels pour une navigation plus intuitive
        """
        app_list = super().get_app_list(request)
        
        # Créer des sections personnalisées
        custom_app_list = []
        
        # Section Utilisateurs
        users_app = {
            'name': 'Utilisateurs',
            'app_label': 'users',
            'app_url': '/admin/users/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Journal
        journal_app = {
            'name': 'Journal',
            'app_label': 'journal',
            'app_url': '/admin/journal/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Engagement
        engagement_app = {
            'name': 'Engagement',
            'app_label': 'engagement',
            'app_url': '/admin/engagement/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Statistiques
        stats_app = {
            'name': 'Statistiques',
            'app_label': 'stats',
            'app_url': '/admin/stats/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Système
        system_app = {
            'name': 'Système',
            'app_label': 'system',
            'app_url': '/admin/system/',
            'has_module_perms': True,
            'models': []
        }
        
        # Dictionnaire pour mapper les modèles aux sections
        model_mapping = {
            'users': ['User', 'UserPreference', 'Badge', 'BadgeTemplate'],
            'journal': ['JournalEntry', 'JournalMedia', 'Objective'],
            'engagement': ['Challenge', 'ChallengeProgress', 'Notification', 'Quote'],
            'stats': ['DailyStat', 'WeeklyStat'],
            'system': ['EventLog']
        }
        
        # Obtenir tous les modèles
        all_models = []
        for app in app_list:
            all_models.extend(app['models'])
        
        # Répartir les modèles dans les sections personnalisées
        for model in all_models:
            model_name = model['object_name']
            
            if model_name in model_mapping['users']:
                users_app['models'].append(model)
            elif model_name in model_mapping['journal']:
                journal_app['models'].append(model)
            elif model_name in model_mapping['engagement']:
                engagement_app['models'].append(model)
            elif model_name in model_mapping['stats']:
                stats_app['models'].append(model)
            elif model_name in model_mapping['system']:
                system_app['models'].append(model)
        
        # Ajouter les sections à la liste personnalisée
        custom_app_list.append(users_app)
        custom_app_list.append(journal_app)
        custom_app_list.append(engagement_app)
        custom_app_list.append(stats_app)
        custom_app_list.append(system_app)
        
        # Garder les autres applications non classées
        for app in app_list:
            if app['app_label'] not in ['users', 'journal', 'engagement', 'stats', 'system']:
                custom_app_list.append(app)
        
        return custom_app_list




================================================
FILE: Myevol_app/api_viewsets/__init__.py
================================================



================================================
FILE: Myevol_app/api_viewsets/badge_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/challenge_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/event_log_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/journal_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/notification_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/objective_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/quote_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/stats_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/user_preference_viewset.py
================================================



================================================
FILE: Myevol_app/api_viewsets/user_viewset.py
================================================



================================================
FILE: Myevol_app/fixtures/badge_templates.json
================================================
[
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 1",
      "description": "Tu as atteint le niveau 1 💪",
      "icon": "🥉",
      "condition": "Atteindre 1 entrée"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 2",
      "description": "Tu as atteint le niveau 2 💪",
      "icon": "🥉",
      "condition": "Atteindre 5 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 3",
      "description": "Tu as atteint le niveau 3 💪",
      "icon": "🥈",
      "condition": "Atteindre 10 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 4",
      "description": "Tu as atteint le niveau 4 💪",
      "icon": "🥈",
      "condition": "Atteindre 20 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 5",
      "description": "Tu as atteint le niveau 5 💪",
      "icon": "🥇",
      "condition": "Atteindre 35 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 6",
      "description": "Tu as atteint le niveau 6 💪",
      "icon": "🥇",
      "condition": "Atteindre 50 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 7",
      "description": "Tu as atteint le niveau 7 💪",
      "icon": "🏆",
      "condition": "Atteindre 75 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 8",
      "description": "Tu as atteint le niveau 8 💪",
      "icon": "🏆",
      "condition": "Atteindre 100 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 9",
      "description": "Tu as atteint le niveau 9 💪",
      "icon": "🏅",
      "condition": "Atteindre 150 entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Niveau 10",
      "description": "Tu as atteint le niveau 10 💪",
      "icon": "🎖️",
      "condition": "Atteindre 200 entrées"
    }
  },

  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Première entrée",
      "description": "Bravo pour ta première entrée 🎉",
      "icon": "🌱",
      "condition": "Créer une première entrée de journal"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Régulier",
      "description": "Bravo pour ta régularité sur 5 jours consécutifs !",
      "icon": "📅",
      "condition": "5 jours consécutifs avec au moins une entrée"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Discipline",
      "description": "La discipline est ta force, continue comme ça !",
      "icon": "🧘‍♂️",
      "condition": "10 jours consécutifs d’entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Résilience",
      "description": "Ta constance forge ta progression",
      "icon": "💎",
      "condition": "15 jours consécutifs d’entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Légende du Journal",
      "description": "Une légende est née : 30 jours d’affilée !",
      "icon": "🔥",
      "condition": "30 jours consécutifs d’entrées"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Ambassadeur d’humeur",
      "description": "Tu rayonnes de positivité !",
      "icon": "😄",
      "condition": "Moyenne d’humeur ≥ 9 sur les 7 derniers jours"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Productivité",
      "description": "Journée ultra-productive !",
      "icon": "⚡",
      "condition": "Ajouter 3 entrées en une seule journée"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Objectif rempli !",
      "description": "Tu avances avec clarté et détermination.",
      "icon": "✅",
      "condition": "Tous les objectifs actuels sont atteints"
    }
  },
  {
    "model": "Myevol_app.badgetemplate",
    "fields": {
      "name": "Persévérance",
      "description": "Tu montes pas à pas vers les sommets.",
      "icon": "🏔️",
      "condition": "Atteindre 100 entrées"
    }
  }
]



================================================
FILE: Myevol_app/migrations/0001_initial.py
================================================
# Generated by Django 4.2.20 on 2025-04-19 12:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=255)),
                ('level', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Modèle de badge',
                'verbose_name_plural': 'Modèles de badges',
            },
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('target_entries', models.PositiveIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name="Qu'avez-vous accompli aujourd'hui ?")),
                ('mood', models.IntegerField(choices=[(1, '1/10'), (2, '2/10'), (3, '3/10'), (4, '4/10'), (5, '5/10'), (6, '6/10'), (7, '7/10'), (8, '8/10'), (9, '9/10'), (10, '10/10')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name="Note d'humeur")),
                ('category', models.CharField(max_length=100, verbose_name='Catégorie')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Entrée de journal',
                'verbose_name_plural': 'Entrées de journal',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.CharField(blank=True, max_length=255)),
                ('mood_tag', models.CharField(blank=True, help_text="Étiquette d’humeur associée (ex: 'positive', 'low', 'neutral')", max_length=50)),
            ],
            options={
                'verbose_name': 'Citation',
                'verbose_name_plural': 'Citations',
                'ordering': ['author'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('longest_streak', models.PositiveIntegerField(default=0, editable=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif_badge', models.BooleanField(default=True)),
                ('notif_objectif', models.BooleanField(default=True)),
                ('notif_info', models.BooleanField(default=True)),
                ('notif_statistique', models.BooleanField(default=True)),
                ('dark_mode', models.BooleanField(default=False)),
                ('accent_color', models.CharField(default='#6C63FF', max_length=20)),
                ('font_choice', models.CharField(default='Roboto', max_length=50)),
                ('enable_animations', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Préférence utilisateur',
                'verbose_name_plural': 'Préférences utilisateur',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100)),
                ('done', models.BooleanField(default=False)),
                ('target_date', models.DateField()),
                ('target_value', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Objectif à atteindre')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objectives', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Objectif',
                'verbose_name_plural': 'Objectifs',
                'ordering': ['target_date', 'done'],
            },
        ),
        migrations.CreateModel(
            name='JournalMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='journal_media/')),
                ('type', models.CharField(choices=[('image', 'Image'), ('audio', 'Audio')], max_length=10)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='Myevol_app.journalentry')),
            ],
        ),
        migrations.AddField(
            model_name='journalentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Événement',
                'verbose_name_plural': 'Événements',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DailyStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('entries_count', models.PositiveIntegerField(default=0)),
                ('mood_average', models.FloatField(blank=True, null=True)),
                ('categories', models.JSONField(blank=True, default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_stats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Statistique journalière',
                'verbose_name_plural': 'Statistiques journalières',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ChallengeProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='Myevol_app.challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=100)),
                ('date_obtenue', models.DateField(auto_now_add=True)),
                ('level', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Badge',
                'verbose_name_plural': 'Badges',
                'ordering': ['-date_obtenue'],
            },
        ),
        migrations.CreateModel(
            name='WeeklyStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start', models.DateField()),
                ('entries_count', models.PositiveIntegerField()),
                ('mood_average', models.FloatField(blank=True, null=True)),
                ('categories', models.JSONField(blank=True, default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_stats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Statistique hebdomadaire',
                'verbose_name_plural': 'Statistiques hebdomadaires',
                'ordering': ['-week_start'],
                'unique_together': {('user', 'week_start')},
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('notif_type', models.CharField(choices=[('badge', 'Badge débloqué'), ('objectif', 'Objectif'), ('statistique', 'Statistique'), ('info', 'Information')], default='info', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['user', 'is_read', 'archived'], name='Myevol_app__user_id_d27d4b_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='journalentry',
            index=models.Index(fields=['user', 'created_at'], name='Myevol_app__user_id_621c24_idx'),
        ),
        migrations.AddIndex(
            model_name='journalentry',
            index=models.Index(fields=['category'], name='Myevol_app__categor_09ed04_idx'),
        ),
        migrations.AddIndex(
            model_name='dailystat',
            index=models.Index(fields=['user', 'date'], name='Myevol_app__user_id_0b0832_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='dailystat',
            unique_together={('user', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='challengeprogress',
            unique_together={('user', 'challenge')},
        ),
        migrations.AlterUniqueTogether(
            name='badge',
            unique_together={('name', 'user')},
        ),
    ]



================================================
FILE: Myevol_app/migrations/0002_alter_challenge_options_alter_journalmedia_options_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-19 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['-end_date'], 'verbose_name': 'Défi', 'verbose_name_plural': 'Défis'},
        ),
        migrations.AlterModelOptions(
            name='journalmedia',
            options={'ordering': ['created_at'], 'verbose_name': 'Média', 'verbose_name_plural': 'Médias'},
        ),
        migrations.AddField(
            model_name='badgetemplate',
            name='animation_url',
            field=models.URLField(blank=True, help_text="Lien vers une animation Lottie ou GIF pour enrichir l'affichage du badge", null=True),
        ),
        migrations.AddField(
            model_name='badgetemplate',
            name='color_theme',
            field=models.CharField(default='#FFD700', max_length=20),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='metadata',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='journalmedia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True, help_text="Lien vers l'image de l'avatar", null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='xp',
            field=models.PositiveIntegerField(default=0, help_text="Points d'expérience cumulés"),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_logs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quote',
            name='mood_tag',
            field=models.CharField(blank=True, help_text="Étiquette d'humeur associée (ex: 'positive', 'low', 'neutral')", max_length=50),
        ),
        migrations.AddIndex(
            model_name='eventlog',
            index=models.Index(fields=['user', 'action'], name='Myevol_app__user_id_e0f943_idx'),
        ),
        migrations.AddIndex(
            model_name='eventlog',
            index=models.Index(fields=['created_at'], name='Myevol_app__created_20eb22_idx'),
        ),
        migrations.AddIndex(
            model_name='quote',
            index=models.Index(fields=['mood_tag'], name='Myevol_app__mood_ta_ef3048_idx'),
        ),
        migrations.AddIndex(
            model_name='quote',
            index=models.Index(fields=['author'], name='Myevol_app__author_3a2bb3_idx'),
        ),
    ]



================================================
FILE: Myevol_app/migrations/0003_alter_badgetemplate_options_badgetemplate_is_active_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-21 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0002_alter_challenge_options_alter_journalmedia_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badgetemplate',
            options={'ordering': ['level', 'name'], 'verbose_name': 'Modèle de badge', 'verbose_name_plural': 'Modèles de badges'},
        ),
        migrations.AddField(
            model_name='badgetemplate',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Détermine si le badge peut être attribué'),
        ),
        migrations.AlterField(
            model_name='badge',
            name='date_obtenue',
            field=models.DateField(auto_now_add=True, help_text="Date d'obtention automatique du badge"),
        ),
        migrations.AlterField(
            model_name='badge',
            name='description',
            field=models.TextField(help_text='Texte descriptif affiché dans l’application'),
        ),
        migrations.AlterField(
            model_name='badge',
            name='icon',
            field=models.CharField(help_text="Icône du badge (emoji ou chemin d'image)", max_length=100),
        ),
        migrations.AlterField(
            model_name='badge',
            name='level',
            field=models.PositiveIntegerField(blank=True, help_text='Niveau associé (pour les badges de progression)', null=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='name',
            field=models.CharField(help_text='Nom du badge (ex. Niveau 3, Régulier)', max_length=100),
        ),
        migrations.AlterField(
            model_name='badge',
            name='user',
            field=models.ForeignKey(help_text='Utilisateur ayant obtenu ce badge', on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='animation_url',
            field=models.URLField(blank=True, help_text='Animation Lottie ou GIF du badge', null=True),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='color_theme',
            field=models.CharField(default='#FFD700', help_text="Couleur d'affichage du badge", max_length=20),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='condition',
            field=models.CharField(help_text='Description simple de la condition d’obtention', max_length=255),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='description',
            field=models.TextField(help_text="Description visible dans l'app"),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='icon',
            field=models.CharField(help_text='Icône (emoji, URL ou nom de fichier)', max_length=100),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='level',
            field=models.PositiveIntegerField(blank=True, help_text="Niveau cible pour les badges de type 'Niveau'", null=True),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='name',
            field=models.CharField(help_text='Nom unique du badge (ex. Régulier, Niveau 3)', max_length=100, unique=True),
        ),
        migrations.AddIndex(
            model_name='badge',
            index=models.Index(fields=['user', 'name'], name='Myevol_app__user_id_1656ff_idx'),
        ),
        migrations.AddIndex(
            model_name='badge',
            index=models.Index(fields=['user', 'date_obtenue'], name='Myevol_app__user_id_5eee4a_idx'),
        ),
    ]



================================================
FILE: Myevol_app/migrations/0004_alter_challengeprogress_options_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-21 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0003_alter_badgetemplate_options_badgetemplate_is_active_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challengeprogress',
            options={'verbose_name': 'Progression de défi', 'verbose_name_plural': 'Progressions de défis'},
        ),
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.TextField(help_text='Description détaillée du défi'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='end_date',
            field=models.DateField(help_text='Date de fin du défi (inclus)'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='start_date',
            field=models.DateField(help_text='Date de début du défi (inclus)'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='target_entries',
            field=models.PositiveIntegerField(default=5, help_text="Nombre d'entrées attendues pour réussir le défi"),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='title',
            field=models.CharField(help_text='Titre du défi visible par les utilisateurs', max_length=255),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='challenge',
            field=models.ForeignKey(help_text='Défi concerné', on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='Myevol_app.challenge'),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='completed',
            field=models.BooleanField(default=False, help_text='Indique si le défi a été complété par l’utilisateur'),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='completed_at',
            field=models.DateTimeField(blank=True, help_text='Date de complétion du défi (si terminé)', null=True),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='user',
            field=models.ForeignKey(help_text='Utilisateur participant au défi', on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL),
        ),
    ]



================================================
FILE: Myevol_app/migrations/0005_alter_badgetemplate_options_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-21 10:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0004_alter_challengeprogress_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badgetemplate',
            options={'verbose_name': 'Modèle de badge', 'verbose_name_plural': 'Modèles de badges'},
        ),
        migrations.AlterModelOptions(
            name='challengeprogress',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='badge',
            name='Myevol_app__user_id_1656ff_idx',
        ),
        migrations.RemoveIndex(
            model_name='badge',
            name='Myevol_app__user_id_5eee4a_idx',
        ),
        migrations.RemoveField(
            model_name='badgetemplate',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='badge',
            name='date_obtenue',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='badge',
            name='icon',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='badge',
            name='level',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='badge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='animation_url',
            field=models.URLField(blank=True, help_text="Lien vers une animation Lottie ou GIF pour enrichir l'affichage du badge", null=True),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='color_theme',
            field=models.CharField(default='#FFD700', max_length=20),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='condition',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='icon',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='level',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.TextField(help_text='Objectif et règles du défi'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='end_date',
            field=models.DateField(help_text='Date de fin du défi'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='start_date',
            field=models.DateField(help_text='Date de début du défi'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='target_entries',
            field=models.PositiveIntegerField(default=5, help_text='Nombre d’entrées à atteindre pour réussir ce défi'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='title',
            field=models.CharField(help_text='Titre du défi (affiché dans l’interface)', max_length=255),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='Myevol_app.challenge'),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='category',
            field=models.CharField(help_text="Thématique de l'entrée (ex: Travail, Perso, Sport).", max_length=100, verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='content',
            field=models.TextField(help_text='Texte libre décrivant votre journée ou vos accomplissements.', verbose_name="Qu'avez-vous accompli aujourd'hui ?"),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text="Date de création de l'entrée."),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='mood',
            field=models.IntegerField(choices=[(1, '1/10'), (2, '2/10'), (3, '3/10'), (4, '4/10'), (5, '5/10'), (6, '6/10'), (7, '7/10'), (8, '8/10'), (9, '9/10'), (10, '10/10')], help_text='Note d’humeur de 1 à 10.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name="Note d'humeur"),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text="Date de dernière modification de l'entrée."),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='user',
            field=models.ForeignKey(help_text="Utilisateur ayant rédigé l'entrée.", on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text="Date d'ajout du fichier."),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='entry',
            field=models.ForeignKey(help_text='Entrée de journal associée à ce média.', on_delete=django.db.models.deletion.CASCADE, related_name='media', to='Myevol_app.journalentry'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='file',
            field=models.FileField(help_text='Fichier média (image ou audio).', upload_to='journal_media/'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='type',
            field=models.CharField(choices=[('image', 'Image'), ('audio', 'Audio')], help_text='Type de média.', max_length=10),
        ),
    ]



================================================
FILE: Myevol_app/migrations/0006_alter_journalentry_category_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-21 10:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0005_alter_badgetemplate_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='category',
            field=models.CharField(max_length=100, verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='content',
            field=models.TextField(verbose_name="Qu'avez-vous accompli aujourd'hui ?"),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='mood',
            field=models.IntegerField(choices=[(1, '1/10'), (2, '2/10'), (3, '3/10'), (4, '4/10'), (5, '5/10'), (6, '6/10'), (7, '7/10'), (8, '8/10'), (9, '9/10'), (10, '10/10')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name="Note d'humeur"),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='Myevol_app.journalentry'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='file',
            field=models.FileField(upload_to='journal_media/'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='type',
            field=models.CharField(choices=[('image', 'Image'), ('audio', 'Audio')], max_length=10),
        ),
    ]



================================================
FILE: Myevol_app/migrations/0007_annualstat_monthlystat_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-21 18:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0006_alter_journalentry_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_start', models.DateField(help_text="Premier jour de l'année")),
                ('entries_count', models.PositiveIntegerField(help_text="Nombre total d'entrées pour l'année")),
                ('mood_average', models.FloatField(blank=True, help_text="Moyenne des humeurs de l'année", null=True)),
                ('categories', models.JSONField(blank=True, default=dict, help_text='Répartition des entrées par catégorie')),
            ],
            options={
                'verbose_name': 'Statistique annuelle',
                'verbose_name_plural': 'Statistiques annuelles',
                'ordering': ['-year_start'],
            },
        ),
        migrations.CreateModel(
            name='MonthlyStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_start', models.DateField(help_text='Premier jour du mois')),
                ('entries_count', models.PositiveIntegerField(help_text="Nombre total d'entrées pour le mois")),
                ('mood_average', models.FloatField(blank=True, help_text='Moyenne des humeurs du mois', null=True)),
                ('categories', models.JSONField(blank=True, default=dict, help_text='Répartition des entrées par catégorie')),
            ],
            options={
                'verbose_name': 'Statistique mensuelle',
                'verbose_name_plural': 'Statistiques mensuelles',
                'ordering': ['-month_start'],
            },
        ),
        migrations.AlterModelOptions(
            name='challengeprogress',
            options={'verbose_name': 'Progression de défi', 'verbose_name_plural': 'Progressions de défi'},
        ),
        migrations.AddField(
            model_name='eventlog',
            name='severity',
            field=models.CharField(choices=[('INFO', 'Information'), ('WARN', 'Warning'), ('ERROR', 'Error'), ('CRITICAL', 'Critical')], default='INFO', help_text="Niveau de gravité de l'événement", max_length=10),
        ),
        migrations.AlterField(
            model_name='badge',
            name='date_obtenue',
            field=models.DateField(auto_now_add=True, help_text='Date à laquelle le badge a été obtenu'),
        ),
        migrations.AlterField(
            model_name='badge',
            name='description',
            field=models.TextField(help_text='Texte explicatif du badge (accomplissement)'),
        ),
        migrations.AlterField(
            model_name='badge',
            name='icon',
            field=models.CharField(help_text='Emoji ou nom d’icône visuelle pour le badge', max_length=100),
        ),
        migrations.AlterField(
            model_name='badge',
            name='level',
            field=models.PositiveIntegerField(blank=True, help_text='Niveau associé au badge (optionnel)', null=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='name',
            field=models.CharField(help_text='Nom du badge affiché à l’utilisateur', max_length=100),
        ),
        migrations.AlterField(
            model_name='badge',
            name='user',
            field=models.ForeignKey(help_text='Utilisateur à qui ce badge a été attribué', on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='animation_url',
            field=models.URLField(blank=True, help_text='URL d’une animation Lottie ou GIF', null=True),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='color_theme',
            field=models.CharField(default='#FFD700', help_text='Couleur HEX du thème visuel du badge', max_length=20),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='condition',
            field=models.CharField(help_text='Condition textuelle d’obtention du badge', max_length=255),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='description',
            field=models.TextField(help_text='Description du badge visible dans l’interface'),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='icon',
            field=models.CharField(help_text='Emoji ou identifiant visuel de l’icône', max_length=100),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='level',
            field=models.PositiveIntegerField(blank=True, help_text="Niveau cible (optionnel, utile pour les badges de type 'Niveau X')", null=True),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='name',
            field=models.CharField(help_text="Nom unique du badge (ex: 'Régulier', 'Niveau 3')", max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.TextField(help_text='Description du défi et règles à suivre'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='target_entries',
            field=models.PositiveIntegerField(default=5, help_text="Nombre d'entrées à réaliser pour réussir le défi"),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='title',
            field=models.CharField(help_text="Titre du défi affiché à l'utilisateur", max_length=255),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='challenge',
            field=models.ForeignKey(help_text='Défi concerné', on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='Myevol_app.challenge'),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='completed',
            field=models.BooleanField(default=False, help_text='Statut de complétion du défi'),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='completed_at',
            field=models.DateTimeField(blank=True, help_text='Date de complétion', null=True),
        ),
        migrations.AlterField(
            model_name='challengeprogress',
            name='user',
            field=models.ForeignKey(help_text='Utilisateur lié à ce défi', on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dailystat',
            name='categories',
            field=models.JSONField(blank=True, default=dict, help_text='Répartition des entrées par catégorie'),
        ),
        migrations.AlterField(
            model_name='dailystat',
            name='date',
            field=models.DateField(help_text='La date des statistiques'),
        ),
        migrations.AlterField(
            model_name='dailystat',
            name='entries_count',
            field=models.PositiveIntegerField(default=0, help_text="Nombre total d'entrées pour la journée"),
        ),
        migrations.AlterField(
            model_name='dailystat',
            name='mood_average',
            field=models.FloatField(blank=True, help_text='Moyenne des humeurs de la journée', null=True),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='action',
            field=models.CharField(help_text="Type d'action enregistrée (ex : 'connexion', 'attribution_badge')", max_length=255),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Horodatage de l’événement (généré automatiquement)'),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='description',
            field=models.TextField(blank=True, help_text="Détail ou message libre sur l'événement"),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='metadata',
            field=models.JSONField(blank=True, help_text='Données additionnelles liées à l’événement (ex : id d’un badge, durée, etc.)', null=True),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Utilisateur concerné par l’événement (optionnel pour les logs système)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_logs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='category',
            field=models.CharField(help_text="La catégorie de l'entrée (ex : Travail, Santé)", max_length=100, verbose_name='Catégorie'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='content',
            field=models.TextField(help_text='Le contenu de l’entrée de journal', verbose_name="Qu'avez-vous accompli aujourd'hui ?"),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date et heure de création de l’entrée'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='mood',
            field=models.IntegerField(choices=[(1, '1/10'), (2, '2/10'), (3, '3/10'), (4, '4/10'), (5, '5/10'), (6, '6/10'), (7, '7/10'), (8, '8/10'), (9, '9/10'), (10, '10/10')], help_text="La note d'humeur (de 1 à 10) associée à cette entrée", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name="Note d'humeur"),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date et heure de la dernière mise à jour'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='user',
            field=models.ForeignKey(help_text='Utilisateur concerné par l’entrée', on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='archived',
            field=models.BooleanField(default=False, help_text='Indique si la notification est archivée'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date de création de la notification'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False, help_text='Indique si la notification a été lue'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(help_text='Contenu de la notification'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('badge', 'Badge débloqué'), ('objectif', 'Objectif atteint'), ('statistique', 'Mise à jour statistique'), ('info', 'Information générale')], default='info', help_text='Type de notification', max_length=20),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read_at',
            field=models.DateTimeField(blank=True, help_text='Date de lecture de la notification', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='scheduled_at',
            field=models.DateTimeField(blank=True, help_text="Date programmée pour l'envoi de la notification", null=True),
        ),
        migrations.AlterField(
            model_name='objective',
            name='category',
            field=models.CharField(help_text="Catégorie de l'objectif.", max_length=100),
        ),
        migrations.AlterField(
            model_name='objective',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text="Date de création de l'objectif."),
        ),
        migrations.AlterField(
            model_name='objective',
            name='done',
            field=models.BooleanField(default=False, help_text="Indique si l'objectif est atteint."),
        ),
        migrations.AlterField(
            model_name='objective',
            name='target_date',
            field=models.DateField(help_text="Date cible pour atteindre l'objectif."),
        ),
        migrations.AlterField(
            model_name='objective',
            name='target_value',
            field=models.PositiveIntegerField(default=1, help_text="Nombre d'actions nécessaires pour accomplir l'objectif.", validators=[django.core.validators.MinValueValidator(1)], verbose_name='Objectif à atteindre'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='title',
            field=models.CharField(help_text="Titre de l'objectif.", max_length=255),
        ),
        migrations.AlterField(
            model_name='quote',
            name='author',
            field=models.CharField(blank=True, help_text="L'auteur de la citation.", max_length=255),
        ),
        migrations.AlterField(
            model_name='quote',
            name='text',
            field=models.TextField(help_text='Le texte de la citation.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True, help_text="URL de l'image de l'avatar de l'utilisateur.", null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text="L'email de l'utilisateur, utilisé pour l'authentification.", max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='longest_streak',
            field=models.PositiveIntegerField(default=0, editable=False, help_text="La plus longue série d'entrées consécutives."),
        ),
        migrations.AlterField(
            model_name='user',
            name='xp',
            field=models.PositiveIntegerField(default=0, help_text="Le nombre total de points d'expérience cumulés par l'utilisateur."),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='accent_color',
            field=models.CharField(default='#6C63FF', help_text="Couleur principale utilisée dans l'interface. Format hexadécimal (#RRGGBB)", max_length=20),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='dark_mode',
            field=models.BooleanField(default=False, help_text="Active ou désactive le mode sombre pour l'interface"),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='enable_animations',
            field=models.BooleanField(default=True, help_text="Active ou désactive les animations dans l'application"),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='font_choice',
            field=models.CharField(default='Roboto', help_text="Police de caractères préférée pour l'interface", max_length=50),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='notif_badge',
            field=models.BooleanField(default=True, help_text='Active ou désactive les notifications pour les badges débloqués'),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='notif_info',
            field=models.BooleanField(default=True, help_text='Active ou désactive les notifications informatives générales'),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='notif_objectif',
            field=models.BooleanField(default=True, help_text='Active ou désactive les notifications liées aux objectifs'),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='notif_statistique',
            field=models.BooleanField(default=True, help_text='Active ou désactive les notifications de statistiques'),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='user',
            field=models.OneToOneField(help_text='Utilisateur auquel ces préférences appartiennent', on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='weeklystat',
            name='categories',
            field=models.JSONField(blank=True, default=dict, help_text='Répartition des entrées par catégorie'),
        ),
        migrations.AlterField(
            model_name='weeklystat',
            name='entries_count',
            field=models.PositiveIntegerField(help_text="Nombre total d'entrées pour la semaine"),
        ),
        migrations.AlterField(
            model_name='weeklystat',
            name='mood_average',
            field=models.FloatField(blank=True, help_text='Moyenne des humeurs de la semaine', null=True),
        ),
        migrations.AlterField(
            model_name='weeklystat',
            name='week_start',
            field=models.DateField(help_text='Premier jour de la semaine (lundi)'),
        ),
        migrations.AddIndex(
            model_name='weeklystat',
            index=models.Index(fields=['user', 'week_start'], name='Myevol_app__user_id_62c5c9_idx'),
        ),
        migrations.AddIndex(
            model_name='weeklystat',
            index=models.Index(fields=['mood_average'], name='Myevol_app__mood_av_031597_idx'),
        ),
        migrations.AddField(
            model_name='monthlystat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_stats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='annualstat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annual_stats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='monthlystat',
            unique_together={('user', 'month_start')},
        ),
        migrations.AlterUniqueTogether(
            name='annualstat',
            unique_together={('user', 'year_start')},
        ),
    ]



================================================
FILE: Myevol_app/migrations/0008_alter_notification_options_alter_badge_date_obtenue_and_more.py
================================================
# Generated by Django 4.2.20 on 2025-04-25 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0007_annualstat_monthlystat_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at'], 'verbose_name': 'Notification', 'verbose_name_plural': 'Notifications'},
        ),
        migrations.AlterField(
            model_name='badge',
            name='date_obtenue',
            field=models.DateField(auto_now_add=True, db_index=True, help_text='Date à laquelle le badge a été obtenu'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date de création du média'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='entry',
            field=models.ForeignKey(help_text='Entrée de journal à laquelle ce média est associé', on_delete=django.db.models.deletion.CASCADE, related_name='media', to='Myevol_app.journalentry'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='file',
            field=models.FileField(help_text='Fichier multimédia (image, audio, etc.)', upload_to='journal_media/'),
        ),
        migrations.AlterField(
            model_name='journalmedia',
            name='type',
            field=models.CharField(choices=[('image', 'Image'), ('audio', 'Audio')], help_text='Type de fichier multimédia (image ou audio)', max_length=10),
        ),
        migrations.AlterField(
            model_name='notification',
            name='archived',
            field=models.BooleanField(default=False, help_text='Indique si la notification a été archivée'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(help_text="Contenu textuel de la notification à afficher à l'utilisateur"),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('badge', 'Badge débloqué'), ('objectif', 'Objectif atteint'), ('statistique', 'Mise à jour statistique'), ('info', 'Information générale')], default='info', help_text='Type de la notification (ex : badge, statistique, info)', max_length=20),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read_at',
            field=models.DateTimeField(blank=True, help_text='Date à laquelle la notification a été lue', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='scheduled_at',
            field=models.DateTimeField(blank=True, help_text='Date programmée pour afficher la notification', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(help_text='Utilisateur concerné par la notification', on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True, help_text="URL de l'avatar de l'utilisateur.", null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text="Adresse e-mail de l'utilisateur.", max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='longest_streak',
            field=models.PositiveIntegerField(default=0, editable=False, help_text='Plus longue série de jours consécutifs.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='xp',
            field=models.PositiveIntegerField(default=0, help_text="Points d'expérience accumulés."),
        ),
    ]



================================================
FILE: Myevol_app/migrations/__init__.py
================================================



================================================
FILE: Myevol_app/models/__init__.py
================================================
# Myevol_app/models/__init__.py

from .user_model import *
from .journal_model import *
from .notification_model import *
from .objective_model import *
from .badge_model import *
from .challenge_model import *
from .stats_model import *
from .event_log_model import *
from .userPreference_model import *
from .quote_model import *



================================================
FILE: Myevol_app/models/badge_model.py
================================================
# MyEvol_app/models/badge_model.py

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings

from ..services.levels_services import get_user_level, get_user_progress

User = settings.AUTH_USER_MODEL

class Badge(models.Model):
    """
    🏅 Badge réellement attribué à un utilisateur.
    
    Les badges sont attribués à un utilisateur lorsqu’il atteint une certaine condition
    définie dans un BadgeTemplate. Ils servent à motiver l’utilisateur et à gamifier l’expérience.

    API Endpoints recommandés :
    - GET /api/badges/ : Liste les badges de l’utilisateur courant
    - GET /api/users/{id}/badges/ : Liste les badges d’un utilisateur donné
    - GET /api/badges/recent/ : Récupère les badges récents (7 derniers jours)

    Champs calculés à exposer dans l’API :
    - was_earned_today
    - is_recent
    - days_since_earned
    """

    name = models.CharField(max_length=100, help_text="Nom du badge affiché à l’utilisateur")
    description = models.TextField(help_text="Texte explicatif du badge (accomplissement)")
    icon = models.CharField(max_length=100, help_text="Emoji ou nom d’icône visuelle pour le badge")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="badges",
        help_text="Utilisateur à qui ce badge a été attribué"
    )
    date_obtenue = models.DateField(
        auto_now_add=True, 
        db_index=True, 
        help_text="Date à laquelle le badge a été obtenu"
        )

    level = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Niveau associé au badge (optionnel)"
    )

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['-date_obtenue']
        unique_together = ('name', 'user')

    def __str__(self):
        """Retourne une représentation lisible du badge."""
        return f"{self.name} ({self.user.username})"

    def __repr__(self):
        """Retourne une représentation détaillée de l'objet Badge."""
        return f"<Badge id={self.id} name='{self.name}' user='{self.user.username}'>"

    def get_absolute_url(self):
        """Retourne l’URL vers la vue de détail du badge."""
        return reverse("badge-detail", kwargs={"pk": self.pk})

    def was_earned_today(self, reference_date=None):
        """Retourne True si le badge a été obtenu aujourd’hui."""
        reference_date = reference_date or now().date()
        return self.date_obtenue == reference_date
    
class BadgeTemplate(models.Model):
    """
    🧩 Modèle de badge définissant les critères pour l’attribution.
    
    Chaque template décrit un badge disponible dans le système, ainsi que les conditions
    pour l’obtenir. Lorsqu’un utilisateur remplit les conditions, un `Badge` est créé
    automatiquement en se basant sur ce modèle.

    API Endpoints recommandés :
    - GET /api/badges/templates/ : Liste tous les modèles de badges
    - GET /api/badges/templates/{id}/ : Détail d’un modèle
    - GET /api/badges/templates/{id}/progress/ : Progression vers ce badge
    - POST /api/badges/sync/ : Vérifie quels badges peuvent être débloqués

    Champs utiles pour l’API :
    - progress (dict)
    - can_unlock (booléen)
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nom unique du badge (ex: 'Régulier', 'Niveau 3')"
    )
    description = models.TextField(
        help_text="Description du badge visible dans l’interface"
    )
    icon = models.CharField(
        max_length=100,
        help_text="Emoji ou identifiant visuel de l’icône"
    )
    condition = models.CharField(
        max_length=255,
        help_text="Condition textuelle d’obtention du badge"
    )
    level = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Niveau cible (optionnel, utile pour les badges de type 'Niveau X')"
    )
    animation_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL d’une animation Lottie ou GIF"
    )
    color_theme = models.CharField(
        default="#FFD700",
        max_length=20,
        help_text="Couleur HEX du thème visuel du badge"
    )

    class Meta:
        verbose_name = "Modèle de badge"
        verbose_name_plural = "Modèles de badges"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<BadgeTemplate id={self.id} name='{self.name}'>"

    def get_absolute_url(self):
        """Retourne l’URL vers la vue de détail du modèle de badge."""
        return reverse("badge-template-detail", kwargs={"pk": self.pk})

    def extract_level_number(self):
        """Essaie d’extraire un niveau à partir du nom ('Niveau 3')."""
        try:
            if self.name.lower().startswith("niveau"):
                return int(self.name.split(" ")[1])
        except (ValueError, IndexError):
            pass
        return None

    def check_unlock(self, user):
        """Vérifie si l'utilisateur peut débloquer ce badge."""
        total = user.total_entries()
        mood_avg = user.mood_average(7)

        conditions = {
            "Première entrée": total >= 1,
            "Régulier": user.has_entries_every_day(5),
            "Discipline": user.has_entries_every_day(10),
            "Résilience": user.has_entries_every_day(15),
            "Légende du Journal": user.has_entries_every_day(30),
            "Ambassadeur d'humeur": mood_avg and mood_avg >= 9,
            "Productivité": user.entries_today() >= 3,
            "Objectif rempli !": user.all_objectives_achieved(),
            "Persévérance": total >= 100,
        }

        if self.name in conditions:
            return conditions[self.name]

        level_number = self.extract_level_number()
        if level_number:
            return get_user_level(total) >= level_number

        return False

    def get_progress(self, user):
        """Calcule la progression d’un utilisateur vers ce badge."""
        total = user.total_entries()
        unlocked = user.badges.filter(name=self.name).exists()

        if unlocked:
            level_number = self.extract_level_number()
            if level_number:
                progress_data = get_user_progress(total)
                return {
                    "percent": 100,
                    "unlocked": True,
                    "current": total,
                    "target": progress_data.get("next_threshold", total)
                }
            return {"percent": 100, "unlocked": True, "current": total, "target": total}

        # Cas spécifiques
        if self.name == "Première entrée":
            return {
                "percent": 100 if total >= 1 else 0,
                "unlocked": total >= 1,
                "current": min(total, 1),
                "target": 1
            }

        level_number = self.extract_level_number()
        if level_number:
            progress_data = get_user_progress(total)
            return {
                "percent": 100 if progress_data["level"] >= level_number else progress_data["progress"],
                "unlocked": progress_data["level"] >= level_number,
                "current": total,
                "target": progress_data["next_threshold"]
            }

        is_unlocked = self.check_unlock(user)
        return {
            "percent": 100 if is_unlocked else 0,
            "unlocked": is_unlocked,
            "current": total,
            "target": 1
        }



================================================
FILE: Myevol_app/models/challenge_model.py
================================================
# MyEvol_app/models/challenge_model.py

from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
import logging



User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)

class Challenge(models.Model):
    """
    🎯 Modèle représentant un défi temporaire proposé aux utilisateurs.

    Les défis visent à stimuler l'engagement en fixant des objectifs à atteindre 
    dans une période donnée (ex : nombre d’entrées à réaliser en X jours).

    API Endpoints recommandés :
    - GET /api/challenges/ : Liste paginée des défis
    - GET /api/challenges/{id}/ : Détails d’un défi
    - GET /api/challenges/active/ : Liste des défis actifs uniquement
    - GET /api/challenges/{id}/participants/ : Liste des participants

    Champs calculés à exposer dans l’API :
    - is_active (bool) : Indique si le défi est actuellement actif
    - days_remaining (int) : Nombre de jours restants avant la fin du défi
    - participants_count (int) : Nombre de participants inscrits à ce défi
    """
    title = models.CharField(max_length=255, help_text="Titre du défi affiché à l'utilisateur")
    description = models.TextField(help_text="Description du défi et règles à suivre")
    start_date = models.DateField(help_text="Date de début du défi")
    end_date = models.DateField(help_text="Date de fin du défi")
    target_entries = models.PositiveIntegerField(
        default=5,
        help_text="Nombre d'entrées à réaliser pour réussir le défi"
    )

    class Meta:
        ordering = ['-end_date']
        verbose_name = "Défi"
        verbose_name_plural = "Défis"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Challenge title='{self.title}' target={self.target_entries} from={self.start_date} to={self.end_date}>"

    def get_absolute_url(self):
        """Retourne l'URL vers la vue de détail du défi."""
        return reverse('challenge_detail', kwargs={'pk': self.pk})

    @property
    def is_active(self):
        """Retourne True si le défi est actif aujourd’hui (entre start et end)."""
        today = now().date()
        return self.start_date <= today <= self.end_date

    @property
    def days_remaining(self):
        """Retourne le nombre de jours restants avant la fin du défi."""
        today = now().date()
        return max(0, (self.end_date - today).days)

    @property
    def participants_count(self):
        """Retourne le nombre de participants inscrits à ce défi."""
        return self.progresses.count()

    def is_completed(self, user):
        """
        Vérifie si l’utilisateur a complété le défi (atteint l’objectif d’entrées).
        """
        return user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count() >= self.target_entries

    def get_progress(self, user):
        """
        Calcule la progression de l’utilisateur sur ce défi.
        
        Args:
            user (User): Utilisateur pour lequel calculer la progression
        
        Returns:
            dict: Un dictionnaire contenant la progression sous forme de pourcentage
                  et d'informations sur le nombre actuel et le nombre cible d'entrées
        """
        current = user.entries.filter(
            created_at__date__range=(self.start_date, self.end_date)
        ).count()

        completed = current >= self.target_entries
        percent = min(100, int((current / self.target_entries) * 100)) if self.target_entries > 0 else 0

        return {
            'percent': percent,
            'current': current,
            'target': self.target_entries,
            'completed': completed
        }

    def save(self, *args, **kwargs):
        """
        Redéfinition de la méthode save pour logguer la création de chaque défi.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            logger.info(f"Création d'un nouveau défi : {self.title} (ID: {self.id})")


class ChallengeProgress(models.Model):
    """
    Suivi individuel d’un utilisateur sur un défi.
    Ce modèle est utilisé pour savoir si l'utilisateur a complété un défi et pour stocker
    l'état actuel de la progression sur ce défi.
    
    API recommandée :
    - GET /api/users/me/challenges/ : Liste des défis avec progression
    - GET /api/challenges/{id}/progress/ : Détails de la progression d'un utilisateur
    - POST /api/challenges/{id}/join/ : Rejoindre un défi
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="challenges",
        help_text="Utilisateur lié à ce défi"
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name="progresses",
        help_text="Défi concerné"
    )
    completed = models.BooleanField(default=False, help_text="Statut de complétion du défi")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Date de complétion")

    class Meta:
        unique_together = ('user', 'challenge')
        verbose_name = "Progression de défi"
        verbose_name_plural = "Progressions de défi"

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

    def __repr__(self):
        return f"<ChallengeProgress user='{self.user.username}' challenge='{self.challenge.title}' completed={self.completed}>"

    def get_absolute_url(self):
        """Retourne l’URL vers la vue de détail de la progression du défi."""
        return reverse('challenge_progress_detail', kwargs={'pk': self.pk})

    def get_progress(self):
        """
        Retourne la progression actuelle de l’utilisateur sur ce défi.
        
        Retourne la progression en termes de pourcentage, ainsi que l'état de complétion.
        """
        return self.challenge.get_progress(self.user)

    def save(self, *args, **kwargs):
        """
        Redéfinition de la méthode save pour logguer la mise à jour de la progression du défi.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        from ..models.event_log_model import EventLog

        if not is_new and self.completed and self.completed_at is None:
            self.completed_at = now()
            EventLog.log_action(
                action="defi_termine",
                description=f"{self.user.username} a complété le défi '{self.challenge.title}'",
                user=self.user,
                metadata={"challenge_id": self.challenge.id}
            )



================================================
FILE: Myevol_app/models/event_log_model.py
================================================
# MyEvol_app/models/event_log_model.py

from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)
User = settings.AUTH_USER_MODEL


class EventLog(models.Model):
    """
    📋 Journalisation des événements système ou utilisateur.
    
    Ce modèle trace toutes les actions notables de l'application, que ce soit côté utilisateur
    (ex : "connexion", "attribution_badge") ou côté système (ex : "nettoyage_quotidien").

    ✅ Objectifs :
    - Faciliter l’audit et le debug
    - Offrir des statistiques d’usage
    - Suivre les événements critiques

    🔗 Endpoints API recommandés :
    - GET /api/logs/
    - GET /api/users/{id}/logs/
    - GET /api/logs/statistics/

    🔧 Champs calculés à exposer :
    - temps_écoulé (depuis l’événement)
    - résumé (action + date)
    
    📦 Services liés :
    - Peut être appelé depuis n’importe quel service via `EventLog.log_action(...)`
    """
    
    SEVERITY_CHOICES = [
        ('INFO', 'Information'),
        ('WARN', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="event_logs",
        help_text="Utilisateur concerné par l’événement (optionnel pour les logs système)"
    )
    action = models.CharField(
        max_length=255,
        help_text="Type d'action enregistrée (ex : 'connexion', 'attribution_badge')"
    )
    description = models.TextField(
        blank=True,
        help_text="Détail ou message libre sur l'événement"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Horodatage de l’événement (généré automatiquement)"
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Données additionnelles liées à l’événement (ex : id d’un badge, durée, etc.)"
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='INFO',
        help_text="Niveau de gravité de l'événement"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        indexes = [
            models.Index(fields=["user", "action"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} - {self.action}"

    def __repr__(self):
        return f"<EventLog id={self.id} action='{self.action}' user='{self.user}' at='{self.created_at}'>"

    def get_absolute_url(self):
        return reverse("eventlog-detail", kwargs={"pk": self.pk})

    @classmethod
    def log_action(cls, action, description="", user=None, severity="INFO", **metadata):
        """
        ✅ Crée un log d’événement, appelé depuis services/signaux/vues.

        Args:
            action (str): Type d’action enregistrée
            description (str): Détail complémentaire de l’événement
            user (User, optional): Utilisateur concerné
            severity (str): Gravité de l'événement (INFO, WARN, ERROR, CRITICAL)
            **metadata (dict): Données personnalisées stockées en JSON

        Returns:
            EventLog: Instance sauvegardée
        """
        log = cls.objects.create(
            action=action,
            description=description,
            user=user,
            severity=severity,
            metadata=metadata or None
        )
        username = getattr(user, 'username', 'System')
        logger.info(f"[LOG] {username} > {action} > {description} > Severity: {severity}")
        return log

    @classmethod
    def get_action_counts(cls, days=30, user=None):
        """
        📊 Statistiques agrégées des événements.

        Args:
            days (int): Nombre de jours à considérer depuis aujourd’hui
            user (User, optional): Filtrer les événements par utilisateur

        Returns:
            dict: Clés = action, Valeurs = nombre d’occurrences

        Exemple :
            {'connexion': 31, 'attribution_badge': 12}
        """
        since = now() - timedelta(days=days)
        qs = cls.objects.filter(created_at__gte=since)
        if user:
            qs = qs.filter(user=user)
        return dict(qs.values("action").annotate(count=Count("id")).values_list("action", "count"))

    def has_metadata(self):
        return bool(self.metadata)



================================================
FILE: Myevol_app/models/journal_model.py
================================================
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





================================================
FILE: Myevol_app/models/notification_model.py
================================================
from django.db import models
from django.conf import settings
from django.utils.timezone import now
import logging

User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)

class Notification(models.Model):
    """
    Modèle représentant une notification envoyée à un utilisateur.
    Permet d'informer l'utilisateur d'événements importants, comme des badges obtenus ou des objectifs atteints.
    
    Types de notifications :
    - badge : Notification liée à un badge débloqué
    - objectif : Notification liée à un objectif atteint
    - statistique : Notification sur l'évolution des statistiques
    - info : Notification informative générale
    """

    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif atteint'),
        ('statistique', 'Mise à jour statistique'),
        ('info', 'Information générale'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="Utilisateur concerné par la notification"
    )
    message = models.TextField(help_text="Contenu textuel de la notification à afficher à l'utilisateur")
    notif_type = models.CharField(
        max_length=20,
        choices=NOTIF_TYPES,
        default='info',
        help_text="Type de la notification (ex : badge, statistique, info)"
    )
    is_read = models.BooleanField(default=False, help_text="Indique si la notification a été lue")
    read_at = models.DateTimeField(null=True, blank=True, help_text="Date à laquelle la notification a été lue")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de la notification")
    archived = models.BooleanField(default=False, help_text="Indique si la notification a été archivée")
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text="Date programmée pour afficher la notification")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'archived']),
        ]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        """
        Représentation textuelle d'une notification.
        """
        return f"{self.user.username} - {self.message[:50]}"

    @property
    def type_display(self):
        """
        Retourne l’étiquette lisible du type de notification.

        Returns:
            str: Libellé utilisateur du type de notification
        """
        return dict(self.NOTIF_TYPES).get(self.notif_type, "Information générale")

    def archive(self):
        """
        Archive la notification sans la supprimer.

        Effet :
            Met à jour le champ `archived` à True si ce n'est pas déjà fait.
        """
        if not self.archived:
            self.archived = True
            self.save(update_fields=['archived'])
            logger.info(f"[NOTIF] Notification archivée pour {self.user.username}")

    def mark_as_read(self):
        """
        Marque la notification comme lue, enregistre l'heure de lecture.

        Effet :
            - is_read = True
            - read_at = maintenant
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])
            logger.info(f"[NOTIF] Notification lue pour {self.user.username}")

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues d’un utilisateur comme lues.

        Args:
            user (User): Utilisateur cible

        Returns:
            int: Nombre de notifications mises à jour
        """
        unread = cls.objects.filter(user=user, is_read=False, archived=False)
        count = unread.update(is_read=True, read_at=now())
        logger.info(f"[NOTIF] {count} notifications marquées comme lues pour {user.username}")
        return count

    @classmethod
    def create_notification(cls, user, message, notif_type='info', scheduled_at=None):
        """
        Crée une notification pour un utilisateur.

        Args:
            user (User): Utilisateur concerné
            message (str): Contenu de la notification
            notif_type (str): Type de notification parmi : 'badge', 'objectif', 'statistique', 'info'
            scheduled_at (datetime, optional): Date à laquelle afficher la notification

        Returns:
            Notification: Instance créée
        """
        notif = cls.objects.create(
            user=user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )
        logger.info(f"[NOTIF] Nouvelle notification '{notif_type}' créée pour {user.username}")
        return notif



================================================
FILE: Myevol_app/models/objective_model.py
================================================
# MyEvol_app/models/objective_model.py

import logging
from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Création d'un logger
logger = logging.getLogger(__name__)

# 🎯 Objectif utilisateur
class Objective(models.Model):
    """
    Modèle représentant un objectif défini par l'utilisateur.
    Permet de suivre les progrès vers des objectifs spécifiques.
    
    API Endpoints suggérés:
    - GET /api/objectives/ - Liste des objectifs de l'utilisateur
    - POST /api/objectives/ - Créer un nouvel objectif
    - GET /api/objectives/{id}/ - Détails d'un objectif spécifique
    - PUT/PATCH /api/objectives/{id}/ - Modifier un objectif existant
    - DELETE /api/objectives/{id}/ - Supprimer un objectif
    - POST /api/objectives/{id}/complete/ - Marquer un objectif comme complété
    - GET /api/objectives/stats/ - Statistiques sur les objectifs (par catégorie, par état)
    - GET /api/objectives/upcoming/ - Objectifs dont l'échéance approche
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="objectives")
    title = models.CharField(max_length=255, help_text="Titre de l'objectif.")
    category = models.CharField(max_length=100, help_text="Catégorie de l'objectif.")
    done = models.BooleanField(default=False, help_text="Indique si l'objectif est atteint.")
    target_date = models.DateField(help_text="Date cible pour atteindre l'objectif.")
    target_value = models.PositiveIntegerField(default=1, verbose_name="Objectif à atteindre", validators=[MinValueValidator(1)], help_text="Nombre d'actions nécessaires pour accomplir l'objectif.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'objectif.")

    class Meta:
        verbose_name = "Objectif"
        verbose_name_plural = "Objectifs"
        ordering = ['target_date', 'done']

    def __str__(self):
        """Représentation en chaîne de caractères de l'objectif avec indicateur d'achèvement"""
        return f"{self.title} ({'✅' if self.done else '🕓'})"

    def __repr__(self):
        """Représentation plus détaillée de l'objectif"""
        return f"<Objective id={self.id} title='{self.title}' done={self.done} target_date={self.target_date}>"

    def get_absolute_url(self):
        """Retourne l'URL vers l'objectif spécifique"""
        return f"/api/objectives/{self.id}/"

    def clean(self):
        """Vérifie que la date cible n'est pas dans le passé"""
        if self.target_date < now().date():
            raise ValidationError("La date cible ne peut pas être dans le passé.")

    def entries_done(self):
        """Compte le nombre d'entrées correspondant à la catégorie de cet objectif pour la date cible"""
        return self.user.entries.filter(
            category=self.category,
            created_at__date=self.target_date
        ).count()

    def progress(self):
        """Calcule le pourcentage de progression vers l'objectif"""
        if self.target_value > 0:
            return min(100, int((self.entries_done() / self.target_value) * 100))
        return 0

    def is_achieved(self):
        """Vérifie si l'objectif est atteint"""
        return self.done or self.progress() >= 100
        
    def days_remaining(self):
        """Calcule le nombre de jours restants avant la date cible"""
        return (self.target_date - now().date()).days
        
    def is_overdue(self):
        """Vérifie si l'objectif est en retard"""
        return not self.done and self.target_date < now().date()

    def save(self, *args, **kwargs):
        """
        Surcharge pour mettre à jour l'état 'done' automatiquement si l'objectif est atteint.
        La notification est désormais gérée par un signal externe.
        """
        self.full_clean()  # Appelle clean()

        logger.info(f"Sauvegarde de l'objectif: {self.title} (État: {'Complété' if self.done else 'En cours'})")

        if not self.done and self.progress() >= 100:
            self.done = True  # On le marque comme complété (notification déléguée au signal)

        super().save(*args, **kwargs)


    def is_due_today(self):
        """Vérifie si la date cible de l’objectif est aujourd’hui"""
        return self.target_date == now().date()

    @property
    def progress_percent(self):
        """Renvoie la progression de l’objectif en pourcentage (0 à 100)"""
        return self.progress()

    @classmethod
    def get_upcoming(cls, user, days=7):
        """Récupère les objectifs dont l'échéance approche dans les prochains jours"""
        today = now().date()
        deadline = today + timedelta(days=days)
        
        logger.info(f"Récupération des objectifs à venir pour {user.username}, dans les {days} prochains jours.")
        
        return cls.objects.filter(
            user=user,
            done=False,
            target_date__gte=today,
            target_date__lte=deadline
        ).order_by('target_date')
        
    @classmethod
    def get_statistics(cls, user):
        """
        Calcule des statistiques sur les objectifs de l'utilisateur.
        """
        from django.db.models import Count, Case, When, IntegerField
        
        # Statistiques globales
        objectives = cls.objects.filter(user=user)
        total = objectives.count()
        completed = objectives.filter(done=True).count()
        
        # Statistiques par catégorie
        by_category = objectives.values('category').annotate(
            total=Count('id'),
            completed=Count(Case(When(done=True, then=1), output_field=IntegerField()))
        ).order_by('-total')
        
        # Objectifs en retard
        overdue = objectives.filter(
            done=False,
            target_date__lt=now().date()
        ).count()
        
        # Calcul du taux de complétion
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        logger.info(f"Statistiques des objectifs pour {user.username} : Total {total}, Complétés {completed}, Taux de complétion {completion_rate}%")
        
        return {
            'total': total,
            'completed': completed,
            'completion_rate': round(completion_rate, 1),
            'overdue': overdue,
            'by_category': {
                item['category']: {'total': item['total'], 'completed': item['completed']} 
                for item in by_category
            }
        }



================================================
FILE: Myevol_app/models/quote_model.py
================================================
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




================================================
FILE: Myevol_app/models/stats_model.py
================================================
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



================================================
FILE: Myevol_app/models/user_model.py
================================================
from datetime import timedelta
import logging
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils.timezone import now
from collections import defaultdict
from functools import wraps
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..services.levels_services import get_user_progress

from ..services.badge_service import update_user_badges
from ..services.streak_service import update_user_streak
from ..services.userpreference_service import create_or_update_preferences
from ..services.user_stats_service import compute_mood_average, compute_current_streak

logger = logging.getLogger(__name__)

def cache_result(timeout=60):
    """
    Décorateur pour mettre en cache le résultat d'une méthode d'instance 
    pendant une durée donnée (en secondes).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"user_{self.pk}_entries_by_category_{args}_{kwargs}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(self, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur.
    Étend AbstractUser avec des champs et méthodes spécifiques à l'app MyEvol.
    """

    email = models.EmailField(unique=True, help_text="Adresse e-mail de l'utilisateur.")
    longest_streak = models.PositiveIntegerField(default=0, editable=False, help_text="Plus longue série de jours consécutifs.")
    avatar_url = models.URLField(blank=True, null=True, help_text="URL de l'avatar de l'utilisateur.")
    xp = models.PositiveIntegerField(default=0, help_text="Points d'expérience accumulés.")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        """Retourne le nom d'utilisateur (username)."""
        return self.username

    def get_full_name(self):
        """Retourne le nom complet (prénom + nom)."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Retourne le prénom ou le username si le prénom est vide."""
        return self.first_name or self.username

    def to_dict(self):
        """
        Représentation de l'utilisateur sous forme de dictionnaire 
        (utile pour les API ou le frontend).
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.get_full_name(),
            "entries": self.total_entries,
            "current_streak": self.current_streak(),
            "mood_average": self.mood_average(),
            "level": self.level(),
            "level_progress": self.level_progress(),
        }

    @property
    def total_entries(self):
        """Retourne le nombre total d'entrées de journal de l'utilisateur."""
        return self.entries.count()

    def mood_average(self, days=7, category=None):
        from Myevol_app.models.user_model import compute_mood_average
        return compute_mood_average(self, days, category)


    def current_streak(self, reference_date=None):
        return compute_current_streak(self, reference_date)


    @cache_result(timeout=300)
    def entries_by_category(self, days=None):
        """
        Calcule la répartition des entrées de journal par catégorie 
        (sur les X derniers jours si précisé).
        """
        entries = self.entries.all()
        if days:
            entries = entries.filter(created_at__gte=now() - timedelta(days=days))
        return dict(
            entries.select_related('category')
            .values('category')
            .annotate(count=Count('id'))
            .values_list('category', 'count')
        )

    def level(self):
        """
        Retourne le niveau actuel de l'utilisateur basé sur le nombre d'entrées.
        """
        progress = get_user_progress(self.total_entries)
        return progress['level']

    def level_progress(self):
        """
        Retourne la progression du niveau actuel en pourcentage.
        """
        progress = get_user_progress(self.total_entries)
        return progress['progress']

    def update_badges(self):
        """
        Met à jour les badges de l'utilisateur via le badge_service.
        """
        try:
            update_user_badges(self)
            logger.info(f"Badges mis à jour pour {self.username} (ID: {self.id})")
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des badges pour {self.username} : {e}")

    def update_streaks(self):
        """
        Met à jour la plus longue série d'entrées consécutives.
        """
        update_user_streak(self)
        logger.info(f"Série d'entrées mise à jour pour {self.username} (ID: {self.id})")

    def create_default_preferences(self):
        """
        Crée des préférences par défaut pour l'utilisateur.
        """
        preferences_data = {
            "dark_mode": False,
            "accent_color": "#6C63FF",
            "font_choice": "Roboto",
            "enable_animations": True,
            "notif_badge": True,
            "notif_objectif": True,
            "notif_info": True,
            "notif_statistique": True
        }
        preferences = create_or_update_preferences(self, preferences_data)
        logger.info(f"Préférences par défaut créées pour {self.username}")
        return preferences

    def add_xp(self, amount):
        """
        Ajoute des points d'expérience à l'utilisateur.
        """
        if amount < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")
        self.xp += amount
        self.save(update_fields=['xp'])
        logger.info(f"{amount} XP ajoutés à {self.username} — Total XP : {self.xp}")

    def clean(self):
        """Validation du modèle : XP ne peut pas être négatif."""
        if self.xp < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")

    def save(self, *args, **kwargs):
        """
        Sauvegarde personnalisée : crée les préférences par défaut à la création.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.create_default_preferences()
            logger.info(f"Nouvel utilisateur {self.username} créé avec préférences.")

    @property
    def is_new(self):
        """Retourne True si l'utilisateur n'a pas encore été sauvegardé (nouveau)."""
        return self.pk is None

    def get_absolute_url(self):
        """Retourne l'URL publique de l'utilisateur."""
        return f"/users/{self.id}/"

    def __repr__(self):
        """Représentation lisible de l'utilisateur."""
        return f"<User username={self.username}>"

    def has_entries_every_day(self, days):
        """
        Vérifie si l'utilisateur a fait au moins une entrée par jour 
        durant les X derniers jours.
        """
        from ..models.journal_model import JournalEntry
        start_date = now().date() - timedelta(days=days - 1)
        entries = self.entries.filter(created_at__date__gte=start_date)
        active_days = entries.values_list("created_at__date", flat=True).distinct()
        return len(active_days) >= days

    def entries_today(self):
        """Retourne le nombre d'entrées créées aujourd'hui."""
        return self.entries.filter(created_at__date=now().date()).count()

    def all_objectives_achieved(self):
        """
        Vérifie si tous les objectifs de l'utilisateur sont complétés.
        """
        from ..models.objective_model import Objective
        return not Objective.objects.filter(user=self, done=False).exists()

    @receiver(post_save, sender='Myevol_app.User')
    @receiver(post_delete, sender='Myevol_app.User')
    def invalidate_cache(sender, instance, **kwargs):
        """
        Invalide le cache des statistiques par catégorie lors d'une sauvegarde
        ou suppression de l'utilisateur.
        """
        cache_key = f"user_{instance.pk}_entries_by_category_()_{{}}"
        cache.delete(cache_key)
        logger.info(f"Cache invalidé pour {instance.username} (ID: {instance.id})")



================================================
FILE: Myevol_app/models/userPreference_model.py
================================================
#  models/userPreference_model.py
import logging
import re
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Initialisation du logger
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL

# Constants for notification types
NOTIFICATION_TYPES = ['badge', 'objectif', 'info', 'statistique']

class UserPreference(models.Model):
    """
    Modèle pour stocker les préférences personnalisées de chaque utilisateur.
    Permet de contrôler les notifications et l'apparence de l'application.
    Chaque utilisateur a exactement une instance de ce modèle (relation one-to-one).
    """
    
    # Relation one-to-one avec l'utilisateur
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="preferences", 
        help_text="Utilisateur auquel ces préférences appartiennent"
    )

    # Préférences de notifications par type
    notif_badge = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications pour les badges débloqués"
    )
    notif_objectif = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications liées aux objectifs"
    )
    notif_info = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications informatives générales"
    )
    notif_statistique = models.BooleanField(
        default=True,
        help_text="Active ou désactive les notifications de statistiques"
    )

    # Préférences d'apparence
    dark_mode = models.BooleanField(
        default=False,
        help_text="Active ou désactive le mode sombre pour l'interface"
    )
    accent_color = models.CharField(
        max_length=20, 
        default="#6C63FF", 
        help_text="Couleur principale utilisée dans l'interface. Format hexadécimal (#RRGGBB)"
    )
    font_choice = models.CharField(
        max_length=50, 
        default="Roboto", 
        help_text="Police de caractères préférée pour l'interface"
    )
    enable_animations = models.BooleanField(
        default=True, 
        help_text="Active ou désactive les animations dans l'application"
    )

    class Meta:
        verbose_name = "Préférence utilisateur"
        verbose_name_plural = "Préférences utilisateur"
        ordering = ["user"]

    def __str__(self):
        """
        Représentation textuelle de l'objet de préférences.
        
        Returns:
            str: Chaîne indiquant à quel utilisateur appartiennent ces préférences
        """
        return f"Préférences de {self.user.username}"

    def __repr__(self):
        """
        Retourne une représentation de l'objet utilisateur sous forme de chaîne de caractères.
        
        Utilisé principalement dans les logs et les interfaces interactives.
        
        Returns:
            str: Représentation de l'objet UserPreference
        """
        return f"<UserPreference user={self.user.username}>"

    def get_absolute_url(self):
        """
        Retourne l'URL absolue des préférences de l'utilisateur.
        
        Utilisé pour accéder aux préférences de l'utilisateur via son URL dédiée.
        
        Returns:
            str: URL pour accéder aux préférences de l'utilisateur
        """
        return f"/users/{self.user.id}/preferences/"

    def to_dict(self):
        """
        Renvoie les préférences sous forme de dictionnaire.
        Pratique pour l'affichage ou l'utilisation dans une API.
        
        Returns:
            dict: Préférences utilisateur structurées
            
        Utilisation dans l'API:
            Cette méthode peut servir de base pour la sérialisation,
            mais privilégiez les sérialiseurs DRF pour plus de contrôle.
            
        Exemple dans un sérialiseur:
            class UserPreferenceSerializer(serializers.ModelSerializer):
                class Meta:
                    model = UserPreference
                    exclude = ['user']  # L'utilisateur est implicite
        """
        return {
            "dark_mode": self.dark_mode,
            "accent_color": self.accent_color,
            "font_choice": self.font_choice,
            "enable_animations": self.enable_animations,
            "notifications": {
                "badge": self.notif_badge,
                "objectif": self.notif_objectif,
                "info": self.notif_info,
                "statistique": self.notif_statistique,
            }
        }

    def get_appearance_settings(self):
        """
        Récupère uniquement les paramètres d'apparence.
        
        Returns:
            dict: Paramètres d'apparence de l'interface
            
        Utilisation dans l'API:
            Utile pour un endpoint dédié à l'apparence ou pour
            la récupération rapide des préférences visuelles au chargement.
        """
        logger.info(f"Récupération des paramètres d'apparence pour l'utilisateur {self.user.username}")
        return {
            "dark_mode": self.dark_mode,
            "accent_color": self.accent_color,
            "font_choice": self.font_choice,
            "enable_animations": self.enable_animations
        }

    def get_notification_settings(self):
        """
        Récupère uniquement les paramètres de notification.
        
        Returns:
            dict: Préférences de notifications par type
            
        Utilisation dans l'API:
            Idéal pour vérifier rapidement si un type de notification
            est activé avant d'en envoyer une.
        """
        logger.info(f"Récupération des paramètres de notification pour l'utilisateur {self.user.username}")
        return {
            "badge": self.notif_badge,
            "objectif": self.notif_objectif,
            "info": self.notif_info,
            "statistique": self.notif_statistique
        }

    def reset_to_defaults(self):
        """
        Réinitialise toutes les préférences aux valeurs par défaut.
        
        Utilisation dans l'API:
            Parfait pour un endpoint permettant à l'utilisateur de
            réinitialiser toutes ses préférences d'un coup.
        """
        logger.info(f"Réinitialisation des préférences aux valeurs par défaut pour l'utilisateur {self.user.username}")
        self.dark_mode = False
        self.accent_color = "#6C63FF"
        self.font_choice = "Roboto"
        self.enable_animations = True
        self.notif_badge = True
        self.notif_objectif = True
        self.notif_info = True
        self.notif_statistique = True
        self.save()

    @classmethod
    def get_or_create_for_user(cls, user):
        """
        Récupère les préférences d'un utilisateur ou les crée si elles n'existent pas.
        
        Args:
            user: L'utilisateur pour lequel récupérer/créer les préférences
            
        Returns:
            UserPreference: Instance de préférences
            
        Utilisation dans l'API:
            Très utile dans les vues pour s'assurer que l'utilisateur
            a toujours des préférences définies.
        """
        prefs, created = cls.objects.get_or_create(
            user=user,
            defaults={
                "dark_mode": False,
                "accent_color": "#6C63FF",
                "font_choice": "Roboto",
                "enable_animations": True,
                "notif_badge": True,
                "notif_objectif": True,
                "notif_info": True,
                "notif_statistique": True
            }
        )
        if created:
            logger.info(f"Préférences par défaut créées pour l'utilisateur {user.username}")
        else:
            logger.info(f"Préférences récupérées pour l'utilisateur {user.username}")
        return prefs

    def should_send_notification(self, notif_type):
        """
        Vérifie si un type spécifique de notification est activé.
        
        Args:
            notif_type (str): Type de notification ('badge', 'objectif', etc.)
            
        Returns:
            bool: True si ce type de notification est activé
            
        Utilisation dans l'API:
            Idéal pour les services de notification pour vérifier
            les préférences de l'utilisateur avant d'envoyer une notification.
            
        Exemple:
            if user.preferences.should_send_notification('badge'):
                send_badge_notification(user, badge)
        """
        mapping = {
            'badge': self.notif_badge,
            'objectif': self.notif_objectif,
            'info': self.notif_info,
            'statistique': self.notif_statistique
        }
        result = mapping.get(notif_type, False)
        logger.debug(f"Vérification de la notification '{notif_type}' pour l'utilisateur {self.user.username}: {result}")
        return result
    
    
# ------------------------------------
# Signaux dans signals/userPreference_signals.py
# ------------------------------------
"""
    - `handle_user_preferences`: Crée les préférences par défaut pour l'utilisateur si elles n'existent pas. 
      Ce service est appelé pour s'assurer que chaque utilisateur a bien des préférences créées à la première connexion. 
      Si les préférences existent déjà, elles sont mises à jour avec les nouvelles informations.

    - `get_or_create_for_user`: Récupère ou crée les préférences d'un utilisateur dans le service `userpreference_service`. 
      Ce service vérifie si l'utilisateur a déjà des préférences associées à son compte, sinon, il les crée avec des valeurs par défaut.

    Les signaux dans ce fichier gèrent les actions automatiques lors de la création ou mise à jour des préférences utilisateur, notamment :
    - La mise à jour des badges et des streaks de l'utilisateur chaque fois que ses préférences sont modifiées (`handle_user_preference_update`).
    - La création de préférences par défaut si elles n'existent pas lors de la création du modèle `UserPreference` (`create_default_preferences`).
    - L'envoi de notifications de mise à jour des préférences à l'utilisateur (`send_notification_on_preference_change`).
    - La validation des préférences avant leur enregistrement pour garantir la conformité des données (`validate_preferences`).

    Ces signaux permettent d'automatiser la gestion des préférences et d'intégrer facilement la logique de gestion des notifications et des actions utilisateur via des services.
"""



================================================
FILE: Myevol_app/serializers/__init__.py
================================================



================================================
FILE: Myevol_app/serializers/badge_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count
from collections import defaultdict

from ..models.badge_model import Badge, BadgeTemplate

User = get_user_model()


class BadgeSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Badge.
    
    Expose les badges attribués à un utilisateur avec leurs métadonnées
    et les champs calculés comme was_earned_today, is_recent, etc.
    """
    was_earned_today = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    days_since_earned = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'icon', 'date_obtenue', 'level',
            'was_earned_today', 'is_recent', 'days_since_earned',
            'user_id', 'user_username'
        ]
        read_only_fields = ['date_obtenue']
    
    def get_was_earned_today(self, obj):
        """Retourne True si le badge a été obtenu aujourd'hui."""
        return obj.was_earned_today()
    
    def get_is_recent(self, obj):
        """Retourne True si le badge a été obtenu dans les 7 derniers jours."""
        today = timezone.now().date()
        delta = today - obj.date_obtenue
        return delta.days <= 7
    
    def get_days_since_earned(self, obj):
        """Retourne le nombre de jours écoulés depuis l'obtention du badge."""
        today = timezone.now().date()
        delta = today - obj.date_obtenue
        return delta.days


class BadgeTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle BadgeTemplate.
    
    Expose les modèles de badges disponibles dans le système.
    """
    level_number = serializers.SerializerMethodField()
    
    class Meta:
        model = BadgeTemplate
        fields = [
            'id', 'name', 'description', 'icon', 'condition', 
            'level', 'animation_url', 'color_theme', 'level_number'
        ]
    
    def get_level_number(self, obj):
        """
        Extrait le numéro de niveau à partir du nom du badge
        si c'est un badge de type 'Niveau X'.
        """
        return obj.extract_level_number()


class BadgeTemplateWithProgressSerializer(BadgeTemplateSerializer):
    """
    Extension du serializer BadgeTemplate incluant la progression
    de l'utilisateur vers l'obtention du badge.
    """
    progress = serializers.SerializerMethodField()
    can_unlock = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    
    class Meta(BadgeTemplateSerializer.Meta):
        fields = BadgeTemplateSerializer.Meta.fields + ['progress', 'can_unlock', 'is_unlocked']
    
    def get_progress(self, obj):
        """
        Retourne les informations de progression vers ce badge.
        La progression est calculée pour l'utilisateur spécifié ou l'utilisateur courant.
        """
        user = self._get_user()
        if user and user.is_authenticated:
            return obj.get_progress(user)
        return {"percent": 0, "unlocked": False, "current": 0, "target": 0}
    
    def get_can_unlock(self, obj):
        """
        Retourne True si l'utilisateur peut débloquer ce badge.
        """
        user = self._get_user()
        if user and user.is_authenticated:
            return obj.check_unlock(user)
        return False
    
    def get_is_unlocked(self, obj):
        """
        Retourne True si l'utilisateur a déjà débloqué ce badge.
        """
        user = self._get_user()
        if user and user.is_authenticated:
            return user.badges.filter(name=obj.name).exists()
        return False
    
    def _get_user(self):
        """
        Récupère l'utilisateur à partir du contexte.
        Supporte soit l'utilisateur de la requête, soit un utilisateur spécifié.
        """
        # Vérifier d'abord si un utilisateur spécifique a été fourni dans le contexte
        user_id = self.context.get('user_id')
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
                
        # Sinon, utiliser l'utilisateur de la requête
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user
            
        return None


class UserBadgeStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques de badges d'un utilisateur.
    
    Fournit des informations sur les badges obtenus et disponibles pour un utilisateur,
    y compris les statistiques récentes et la progression globale.
    """
    total_badges = serializers.SerializerMethodField()
    recent_badges = serializers.SerializerMethodField()
    unlocked_percentage = serializers.SerializerMethodField()
    badges_by_category = serializers.SerializerMethodField()
    next_available_badges = serializers.SerializerMethodField()
    
    def get_total_badges(self, user):
        """Nombre total de badges obtenus par l'utilisateur."""
        return user.badges.count()
    
    def get_recent_badges(self, user):
        """Badges obtenus au cours des 7 derniers jours."""
        today = timezone.now().date()
        week_ago = today - timezone.timedelta(days=7)
        recent = user.badges.filter(date_obtenue__gte=week_ago)
        return BadgeSerializer(recent, many=True).data
    
    def get_unlocked_percentage(self, user):
        """Pourcentage de badges débloqués sur le total disponible."""
        total_templates = BadgeTemplate.objects.count()
        if total_templates == 0:
            return 0
        return round((user.badges.count() / total_templates) * 100, 1)
    
    def get_badges_by_category(self, user):
        """Badges groupés par catégorie/type."""
        # On utilise le préfixe du nom comme catégorie pour cet exemple
        # Dans une implémentation réelle, vous pourriez ajouter un champ 'category' au modèle
        badges = user.badges.all()
        categories = defaultdict(list)
        
        for badge in badges:
            if badge.name.startswith("Niveau"):
                categories["Niveaux"].append(BadgeSerializer(badge).data)
            elif "entrée" in badge.name.lower():
                categories["Progression"].append(BadgeSerializer(badge).data)
            else:
                categories["Accomplissements"].append(BadgeSerializer(badge).data)
                
        return dict(categories)
    
    def get_next_available_badges(self, user):
        """Liste des prochains badges que l'utilisateur peut débloquer."""
        # On récupère les templates que l'utilisateur n'a pas encore débloqués
        unlocked_names = user.badges.values_list('name', flat=True)
        available_templates = BadgeTemplate.objects.exclude(name__in=unlocked_names)
        
        # On vérifie lesquels peuvent être débloqués
        next_badges = []
        for template in available_templates:
            if template.check_unlock(user):
                next_badges.append(template)
        
        return BadgeTemplateWithProgressSerializer(
            next_badges, 
            many=True, 
            context={'request': self.context.get('request')}
        ).data


================================================
FILE: Myevol_app/serializers/challenge_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models.challenge_model import Challenge, ChallengeProgress

User = get_user_model()


class ChallengeSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Challenge.
    
    Expose les défis avec leurs métadonnées et les champs calculés
    comme is_active, days_remaining et participants_count.
    """
    is_active = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 
            'target_entries', 'is_active', 'days_remaining', 'participants_count'
        ]
        read_only_fields = ['is_active', 'days_remaining', 'participants_count']


class ChallengeProgressSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ChallengeProgress.
    
    Expose la progression d'un utilisateur sur un défi spécifique.
    """
    progress = serializers.SerializerMethodField()
    challenge_title = serializers.ReadOnlyField(source='challenge.title')
    challenge_description = serializers.ReadOnlyField(source='challenge.description')
    days_remaining = serializers.ReadOnlyField(source='challenge.days_remaining')
    start_date = serializers.ReadOnlyField(source='challenge.start_date')
    end_date = serializers.ReadOnlyField(source='challenge.end_date')
    
    class Meta:
        model = ChallengeProgress
        fields = [
            'id', 'user', 'challenge', 'completed', 'completed_at',
            'progress', 'challenge_title', 'challenge_description',
            'days_remaining', 'start_date', 'end_date'
        ]
        read_only_fields = ['completed', 'completed_at', 'progress']
    
    def get_progress(self, obj):
        """
        Récupère la progression actuelle de l'utilisateur sur ce défi.
        """
        return obj.get_progress()


class ChallengeDetailSerializer(ChallengeSerializer):
    """
    Serializer étendu pour les détails d'un défi.
    
    Inclut la progression de l'utilisateur courant si disponible.
    """
    user_progress = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()
    
    class Meta(ChallengeSerializer.Meta):
        fields = ChallengeSerializer.Meta.fields + ['user_progress', 'joined']
    
    def get_user_progress(self, obj):
        """
        Retourne la progression de l'utilisateur courant sur ce défi.
        """
        user = self._get_user()
        if not user or not user.is_authenticated:
            return None
            
        return obj.get_progress(user)
    
    def get_joined(self, obj):
        """
        Retourne True si l'utilisateur courant participe à ce défi.
        """
        user = self._get_user()
        if not user or not user.is_authenticated:
            return False
            
        return ChallengeProgress.objects.filter(user=user, challenge=obj).exists()
    
    def _get_user(self):
        """
        Récupère l'utilisateur à partir du contexte.
        """
        # D'abord vérifier un utilisateur spécifique fourni
        user_id = self.context.get('user_id')
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
        
        # Sinon utiliser l'utilisateur de la requête
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user
            
        return None


class UserChallengeStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques des défis d'un utilisateur.
    
    Fournit des informations sur les défis actifs, complétés et disponibles
    pour un utilisateur donné.
    """
    total_challenges_joined = serializers.SerializerMethodField()
    active_challenges = serializers.SerializerMethodField()
    completed_challenges = serializers.SerializerMethodField()
    available_challenges = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    
    def get_total_challenges_joined(self, user):
        """Nombre total de défis rejoints par l'utilisateur."""
        return user.challenges.count()
    
    def get_active_challenges(self, user):
        """Liste des défis actifs de l'utilisateur (rejoints mais non complétés)."""
        today = timezone.now().date()
        progresses = user.challenges.filter(
            challenge__end_date__gte=today,
            completed=False
        ).select_related('challenge')
        
        return ChallengeProgressSerializer(progresses, many=True).data
    
    def get_completed_challenges(self, user):
        """Liste des défis complétés par l'utilisateur."""
        progresses = user.challenges.filter(completed=True).select_related('challenge')
        return ChallengeProgressSerializer(progresses, many=True).data
    
    def get_available_challenges(self, user):
        """Liste des défis disponibles non rejoints par l'utilisateur."""
        today = timezone.now().date()
        joined_ids = user.challenges.values_list('challenge_id', flat=True)
        
        available = Challenge.objects.filter(
            end_date__gte=today
        ).exclude(
            id__in=joined_ids
        )
        
        return ChallengeSerializer(available, many=True).data
    
    def get_completion_rate(self, user):
        """Taux de complétion des défis (défis complétés / défis rejoints)."""
        total = user.challenges.count()
        if total == 0:
            return 0
        
        completed = user.challenges.filter(completed=True).count()
        return round((completed / total) * 100, 1)


class ParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer pour les participants d'un défi.
    
    Expose les informations de base sur l'utilisateur et sa progression sur le défi.
    """
    username = serializers.ReadOnlyField(source='user.username')
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = ChallengeProgress
        fields = ['id', 'user', 'username', 'completed', 'completed_at', 'progress']
    
    def get_progress(self, obj):
        """Récupère la progression actuelle du participant sur le défi."""
        return obj.get_progress()


================================================
FILE: Myevol_app/serializers/event_log_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from django.contrib.auth import get_user_model

from ..models.event_log_model import EventLog

User = get_user_model()

class EventLogSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle EventLog.
    
    Expose les événements du journal avec leurs métadonnées
    ainsi que des champs calculés pour l'UX comme temps écoulé et résumé.
    """
    temps_écoulé = serializers.SerializerMethodField()
    résumé = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username', default=None)
    user_id = serializers.ReadOnlyField(source='user.id', default=None)
    
    class Meta:
        model = EventLog
        fields = [
            'id', 'user', 'user_username', 'user_id', 'action', 'description',
            'created_at', 'metadata', 'severity', 'temps_écoulé', 'résumé'
        ]
        read_only_fields = ['created_at', 'temps_écoulé', 'résumé']
    
    def get_temps_écoulé(self, obj):
        """
        Calcule le temps écoulé depuis la création de l'événement.

        Returns:
            dict: Détail du temps écoulé en secondes, minutes, heures et jours.
        """
        now = timezone.now()
        delta = now - obj.created_at
        return {
            'total_seconds': int(delta.total_seconds()),
            'days': delta.days,
            'hours': int(delta.seconds / 3600),
            'minutes': int((delta.seconds % 3600) / 60),
            'seconds': delta.seconds % 60,
            'human_format': self._format_timedelta_human(delta)
        }
    
    def get_résumé(self, obj):
        """
        Génère un résumé concis de l'événement.

        Returns:
            str: Action + date formatée.
        """
        return f"{obj.action} ({obj.created_at.strftime('%d/%m/%Y %H:%M')})"
    
    def _format_timedelta_human(self, delta):
        """
        Convertit un timedelta en format lisible par l'humain.

        Args:
            delta (timedelta): Différence de temps.

        Returns:
            str: Description humanisée.
        """
        if delta.days > 0:
            return f"il y a {delta.days} jour{'s' if delta.days > 1 else ''}"
        hours = delta.seconds // 3600
        if hours > 0:
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        minutes = (delta.seconds % 3600) // 60
        if minutes > 0:
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        return "à l'instant"


class EventLogDetailSerializer(EventLogSerializer):
    """
    Serializer détaillé pour un événement unique.
    
    Ajoute des informations supplémentaires sur les métadonnées de l'événement.
    """
    has_metadata = serializers.BooleanField()
    formatted_metadata = serializers.SerializerMethodField()
    
    class Meta(EventLogSerializer.Meta):
        fields = EventLogSerializer.Meta.fields + ['has_metadata', 'formatted_metadata']
    
    def get_formatted_metadata(self, obj):
        """
        Formate les métadonnées selon le type d'action.

        Returns:
            dict | None: Métadonnées formatées pour affichage.
        """
        if not obj.metadata or not isinstance(obj.metadata, dict):
            return None

        if obj.action == 'attribution_badge' and 'badge_id' in obj.metadata:
            badge_id = obj.metadata.get('badge_id')
            badge_name = obj.metadata.get('badge_name', 'Badge inconnu')
            return {
                'formatted': f"Badge attribué : {badge_name} (ID: {badge_id})",
                'details': obj.metadata
            }

        if obj.action == 'defi_termine' and 'challenge_id' in obj.metadata:
            challenge_id = obj.metadata.get('challenge_id')
            return {
                'formatted': f"Défi complété (ID: {challenge_id})",
                'details': obj.metadata
            }

        return {
            'formatted': ', '.join([f"{k}: {v}" for k, v in obj.metadata.items()]),
            'details': obj.metadata
        }


class EventLogStatisticsSerializer(serializers.Serializer):
    """
    Serializer pour produire des statistiques sur les événements enregistrés.
    
    Donne des infos sur le volume, la répartition et les tendances des événements.
    """
    period_days = serializers.IntegerField(default=30)
    total_events = serializers.SerializerMethodField()
    events_by_action = serializers.SerializerMethodField()
    events_by_severity = serializers.SerializerMethodField()
    events_by_time = serializers.SerializerMethodField()
    most_recent = serializers.SerializerMethodField()
    
    def get_total_events(self, obj):
        """
        Retourne le nombre total d'événements sur la période demandée.
        """
        user = obj.get('user')
        period_days = obj.get('period_days', 30)
        since = timezone.now() - timedelta(days=period_days)
        query = EventLog.objects.filter(created_at__gte=since)

        if user:
            query = query.filter(user=user)

        return query.count()

    def get_events_by_action(self, obj):
        """
        Retourne la répartition des événements par action.
        """
        user = obj.get('user')
        period_days = obj.get('period_days', 30)
        return EventLog.get_action_counts(days=period_days, user=user)

    def get_events_by_severity(self, obj):
        """
        Retourne la répartition des événements par niveau de gravité.
        """
        user = obj.get('user')
        period_days = obj.get('period_days', 30)
        since = timezone.now() - timedelta(days=period_days)
        query = EventLog.objects.filter(created_at__gte=since)

        if user:
            query = query.filter(user=user)

        aggregated = query.values('severity').annotate(total=Count('id'))
        return {item['severity']: item['total'] for item in aggregated}

    def get_events_by_time(self, obj):
        """
        Retourne la répartition temporelle (24h, 7j, 30j).
        """
        user = obj.get('user')
        now = timezone.now()

        last_day = now - timedelta(days=1)
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        query = EventLog.objects
        if user:
            query = query.filter(user=user)

        return {
            'last_24h': query.filter(created_at__gte=last_day).count(),
            'last_7d': query.filter(created_at__gte=last_week).count(),
            'last_30d': query.filter(created_at__gte=last_month).count()
        }

    def get_most_recent(self, obj):
        """
        Retourne les 5 événements les plus récents.
        """
        user = obj.get('user')
        query = EventLog.objects
        if user:
            query = query.filter(user=user)

        recent = query.order_by('-created_at')[:5]
        return EventLogSerializer(recent, many=True).data


class UserEventLogSerializer(serializers.Serializer):
    """
    Serializer pour l'activité récente d'un utilisateur à partir des événements.
    """
    user_id = serializers.IntegerField(source='id')
    username = serializers.CharField()
    total_events = serializers.SerializerMethodField()
    recent_activity = serializers.SerializerMethodField()
    first_event = serializers.SerializerMethodField()
    last_event = serializers.SerializerMethodField()
    
    def get_total_events(self, user):
        """Retourne le nombre total d'événements liés à l'utilisateur."""
        return user.event_logs.count()
    
    def get_recent_activity(self, user):
        """Retourne les 5 derniers événements de l'utilisateur."""
        recent = user.event_logs.all().order_by('-created_at')[:5]
        return EventLogSerializer(recent, many=True).data
    
    def get_first_event(self, user):
        """Retourne le tout premier événement de l'utilisateur."""
        first = user.event_logs.all().order_by('created_at').first()
        if not first:
            return None
        return EventLogSerializer(first).data
    
    def get_last_event(self, user):
        """Retourne le dernier événement de l'utilisateur."""
        last = user.event_logs.all().order_by('-created_at').first()
        if not last:
            return None
        return EventLogSerializer(last).data



================================================
FILE: Myevol_app/serializers/journal_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.db.models import Avg, Count

from ..models.journal_model import JournalEntry, JournalMedia

User = get_user_model()

class JournalMediaSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle JournalMedia.
    
    Expose les fichiers multimédias associés aux entrées de journal.
    """
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = JournalMedia
        fields = [
            'id', 'entry', 'file', 'type', 'created_at', 
            'file_url', 'file_size', 'file_type_display'
        ]
        read_only_fields = ['created_at', 'file_url', 'file_size', 'file_type_display']
    
    def get_file_url(self, obj):
        """Retourne l'URL complète du fichier média."""
        return obj.file_url()
    
    def get_file_size(self, obj):
        """Retourne la taille du fichier média en octets."""
        return obj.file_size()
    
    def validate(self, data):
        """Valide que le type du fichier correspond bien à son contenu."""
        instance = JournalMedia(**data)
        try:
            instance.validate_file_type()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return data


class JournalEntrySerializer(serializers.ModelSerializer):
    """
    Serializer de base pour le modèle JournalEntry.
    
    Expose les entrées de journal de manière enrichie avec humeur, média et délai.
    """
    mood_emoji = serializers.SerializerMethodField()
    media = JournalMediaSerializer(many=True, read_only=True)
    user_username = serializers.ReadOnlyField(source='user.username')
    time_since_creation = serializers.SerializerMethodField()
    
    class Meta:
        model = JournalEntry
        fields = [
            'id', 'user', 'user_username', 'content', 'mood', 'mood_emoji',
            'category', 'created_at', 'updated_at', 'media', 'time_since_creation'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user_username', 'mood_emoji']
    
    def get_mood_emoji(self, obj):
        """Retourne l'emoji correspondant à la note d'humeur."""
        return obj.get_mood_emoji()
    
    def get_time_since_creation(self, obj):
        """Retourne une description relative du temps écoulé depuis la création."""
        now = timezone.now()
        delta = now - obj.created_at
        
        if delta.days > 0:
            if delta.days == 1:
                return "hier"
            if delta.days < 7:
                return f"il y a {delta.days} jours"
            if delta.days < 30:
                weeks = delta.days // 7
                return f"il y a {weeks} semaine{'s' if weeks > 1 else ''}"
            if delta.days < 365:
                months = delta.days // 30
                return f"il y a {months} mois"
            years = delta.days // 365
            return f"il y a {years} an{'s' if years > 1 else ''}"
        
        hours = delta.seconds // 3600
        if hours > 0:
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        
        minutes = (delta.seconds % 3600) // 60
        if minutes > 0:
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        
        return "à l'instant"
    
    def validate_content(self, value):
        """Valide que le contenu est d'une longueur suffisante."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Le contenu doit comporter au moins 5 caractères.")
        return value
    
    def create(self, validated_data):
        """Crée une entrée de journal pour l'utilisateur courant."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class JournalEntryDetailSerializer(JournalEntrySerializer):
    """
    Serializer détaillé pour une entrée de journal.
    
    Ajoute des informations comme l'éditabilité et le nombre d'entrées du jour.
    """
    is_editable = serializers.SerializerMethodField()
    day_entries_count = serializers.SerializerMethodField()
    
    class Meta(JournalEntrySerializer.Meta):
        fields = JournalEntrySerializer.Meta.fields + ['is_editable', 'day_entries_count']
    
    def get_is_editable(self, obj):
        """Détermine si l'entrée est encore modifiable (24h après création)."""
        now = timezone.now()
        edit_window = timedelta(hours=24)
        return now - obj.created_at <= edit_window
    
    def get_day_entries_count(self, obj):
        """Retourne combien d'entrées ont été créées le même jour par l'utilisateur."""
        created_date = obj.created_at.date()
        return JournalEntry.objects.filter(
            user=obj.user,
            created_at__date=created_date
        ).count()


# ✅ JournalEntryCreateSerializer : valide bien content (min 5 caractères)
class JournalEntryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer une entrée de journal avec fichiers médias.
    """
    media_files = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    media_types = serializers.ListField(
        child=serializers.ChoiceField(choices=JournalMedia._meta.get_field('type').choices),
        required=False, write_only=True
    )
    
    class Meta:
        model = JournalEntry
        fields = ['content', 'mood', 'category', 'media_files', 'media_types']
    
    def validate(self, data):
        """Valide la correspondance entre fichiers et types associés."""
        media_files = data.get('media_files', [])
        media_types = data.get('media_types', [])
        
        if len(media_files) != len(media_types):
            raise serializers.ValidationError(
                "Le nombre de fichiers et de types de médias doit correspondre."
            )
        return data
    
    def validate_content(self, value):
        """Valide que le contenu est d'une longueur suffisante."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Le contenu doit comporter au moins 5 caractères.")
        return value

    def create(self, validated_data):
        """Crée une entrée et ses médias associés."""
        media_files = validated_data.pop('media_files', [])
        media_types = validated_data.pop('media_types', [])
        
        request = self.context.get('request')
        validated_data['user'] = request.user
        entry = JournalEntry.objects.create(**validated_data)
        
        for file, type in zip(media_files, media_types):
            JournalMedia.objects.create(entry=entry, file=file, type=type)
        
        return entry
    
    def validate(self, data):
        """Valide la correspondance entre fichiers et types associés."""
        media_files = data.get('media_files', [])
        media_types = data.get('media_types', [])
        
        if len(media_files) != len(media_types):
            raise serializers.ValidationError(
                "Le nombre de fichiers et de types de médias doit correspondre."
            )
        return data
    
    def create(self, validated_data):
        """Crée une entrée et ses médias associés."""
        media_files = validated_data.pop('media_files', [])
        media_types = validated_data.pop('media_types', [])
        
        request = self.context.get('request')
        validated_data['user'] = request.user
        entry = JournalEntry.objects.create(**validated_data)
        
        for file, type in zip(media_files, media_types):
            JournalMedia.objects.create(entry=entry, file=file, type=type)
        
        return entry


class JournalEntryCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer pour affichage des entrées sous forme de calendrier.
    
    Fournit des métriques condensées (nombre, humeur, catégories).
    """
    day = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True)
    mood_avg = serializers.FloatField(read_only=True)
    categories = serializers.ListField(read_only=True)

    class Meta:
        model = JournalEntry
        fields = ['day', 'count', 'mood_avg', 'categories']
    
    def get_day(self, obj):
        """Retourne la date sans l'heure à partir de created_at."""
        return obj.created_at.date()

class JournalStatsSerializer(serializers.Serializer):
    """
    Serializer pour générer des statistiques sur les entrées de journal d'un utilisateur.
    """
    total_entries = serializers.SerializerMethodField()
    entries_per_category = serializers.SerializerMethodField()
    mood_distribution = serializers.SerializerMethodField()
    monthly_entries = serializers.SerializerMethodField()
    average_mood = serializers.SerializerMethodField()
    entries_streak = serializers.SerializerMethodField()
    
    def get_total_entries(self, user):
        """Retourne le nombre total d'entrées."""
        return user.entries.count()
    
    def get_entries_per_category(self, user):
        """Retourne la répartition des entrées par catégorie."""
        categories = user.entries.values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {cat['category']: cat['count'] for cat in categories}
    
    def get_mood_distribution(self, user):
        """Retourne la distribution des notes d'humeur."""
        moods = user.entries.values('mood').annotate(
            count=Count('id')
        ).order_by('mood')
        
        distribution = {str(i): 0 for i in range(1, 11)}
        for mood in moods:
            distribution[str(mood['mood'])] = mood['count']
        
        return distribution
    
    def get_monthly_entries(self, user):
        """Retourne la distribution des entrées par mois sur 1 an."""
        today = timezone.now().date()
        start_date = today - timedelta(days=365)
        
        entries = user.entries.filter(
            created_at__date__gte=start_date
        ).extra({'month': "to_char(created_at, 'YYYY-MM')"}).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        months = {}
        for i in range(12):
            month_date = today - timedelta(days=30 * i)
            month_key = month_date.strftime('%Y-%m')
            months[month_key] = 0
        
        for entry in entries:
            months[entry['month']] = entry['count']
        
        return months
    
    def get_average_mood(self, user):
        """Retourne l'humeur moyenne actuelle et son évolution."""
        result = {'overall': 0, 'last_week': 0, 'last_month': 0, 'trend': 'stable'}
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        two_months_ago = today - timedelta(days=60)
        
        overall = user.entries.aggregate(avg=Avg('mood'))
        last_week = user.entries.filter(created_at__date__gte=week_ago).aggregate(avg=Avg('mood'))
        last_month = user.entries.filter(created_at__date__gte=month_ago).aggregate(avg=Avg('mood'))
        previous_month = user.entries.filter(
            created_at__date__gte=two_months_ago,
            created_at__date__lt=month_ago
        ).aggregate(avg=Avg('mood'))
        
        result['overall'] = round(overall['avg'] or 0, 1)
        result['last_week'] = round(last_week['avg'] or 0, 1)
        result['last_month'] = round(last_month['avg'] or 0, 1)
        
        if previous_month['avg'] and last_month['avg']:
            diff = last_month['avg'] - previous_month['avg']
            if diff > 0.5:
                result['trend'] = 'up'
            elif diff < -0.5:
                result['trend'] = 'down'
        
        return result
    
    # ✅ Correction dans get_entries_streak
    def get_entries_streak(self, user):
        """Retourne la série actuelle et maximale de jours avec au moins une entrée."""
        today = timezone.now().date()
        dates_with_entries = user.entries.values('created_at__date').distinct().order_by('created_at__date')
        
        if not dates_with_entries:
            return {'current': 0, 'max': 0, 'dates': []}
        
        dates = [entry['created_at__date'] for entry in dates_with_entries]
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        current_active = dates[-1] in (today, today - timedelta(days=1))
        
        return {
            'current': current_streak if current_active else 0,
            'max': max_streak,
            'current_active': current_active,
            'last_entry_date': dates[-1].isoformat()
        }


class CategorySuggestionSerializer(serializers.Serializer):
    """
    Serializer pour retourner des suggestions de catégories.
    """
    categories = serializers.SerializerMethodField()
    
    def get_categories(self, user):
        """Retourne les catégories les plus utilisées par l'utilisateur."""
        return JournalEntry.get_category_suggestions(user)



================================================
FILE: Myevol_app/serializers/notification_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models.notification_model import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Notification.
    Expose les notifications avec temps écoulé et type affiché.
    """
    type_display = serializers.CharField(read_only=True)
    time_since_created = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_username', 'message', 'notif_type', 'type_display',
            'is_read', 'read_at', 'created_at', 'archived', 'scheduled_at',
            'time_since_created'
        ]
        read_only_fields = ['created_at', 'read_at', 'type_display']

    def get_time_since_created(self, obj):
        """Retourne le temps écoulé depuis la création de la notification sous forme lisible."""
        now = timezone.now()
        delta = now - obj.created_at

        if delta.days > 0:
            if delta.days == 1:
                return "hier"
            if delta.days < 7:
                return f"il y a {delta.days} jours"
            if delta.days < 30:
                weeks = delta.days // 7
                return f"il y a {weeks} semaine{'s' if weeks > 1 else ''}"
            if delta.days < 365:
                months = delta.days // 30
                return f"il y a {months} mois"
            years = delta.days // 365
            return f"il y a {years} an{'s' if years > 1 else ''}"

        hours = delta.seconds // 3600
        if hours > 0:
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"

        minutes = (delta.seconds % 3600) // 60
        if minutes > 0:
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"

        return "à l'instant"


class NotificationListSerializer(NotificationSerializer):
    """
    Serializer simplifié pour afficher une liste de notifications.
    """
    class Meta(NotificationSerializer.Meta):
        fields = [
            'id', 'message', 'notif_type', 'type_display', 
            'is_read', 'created_at', 'time_since_created'
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'une notification par un utilisateur.
    """
    class Meta:
        model = Notification
        fields = ['message', 'notif_type', 'scheduled_at']

    def create(self, validated_data):
        """Créé une notification associée à l'utilisateur courant."""
        request = self.context.get('request')
        user = request.user if request else None
        if not user:
            raise serializers.ValidationError("L'utilisateur est requis pour créer une notification.")

        return Notification.create_notification(
            user=user,
            message=validated_data['message'],
            notif_type=validated_data.get('notif_type', 'info'),
            scheduled_at=validated_data.get('scheduled_at')
        )


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour mettre à jour l'état d'une notification (lue/archivée).
    """
    mark_as_read = serializers.BooleanField(required=False, write_only=True)
    archive = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Notification
        fields = ['is_read', 'archived', 'mark_as_read', 'archive']
        read_only_fields = ['read_at']

    def update(self, instance, validated_data):
        """Met à jour l'instance selon les actions demandées."""
        if validated_data.pop('mark_as_read', False):
            instance.mark_as_read()

        if validated_data.pop('archive', False):
            instance.archive()

        return super().update(instance, validated_data)


class NotificationCountSerializer(serializers.Serializer):
    """
    Serializer pour compter les notifications par statut et type.
    """
    total = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    today = serializers.SerializerMethodField()
    by_type = serializers.SerializerMethodField()

    def get_total(self, user):
        return user.notifications.filter(archived=False).count()

    def get_unread(self, user):
        return user.notifications.filter(is_read=False, archived=False).count()

    def get_today(self, user):
        today = timezone.now().date()
        return user.notifications.filter(created_at__date=today, archived=False).count()

    def get_by_type(self, user):
        result = {}
        for notif_type, _ in Notification.NOTIF_TYPES:
            notifications = user.notifications.filter(notif_type=notif_type, archived=False)
            result[notif_type] = {
                'total': notifications.count(),
                'unread': notifications.filter(is_read=False).count()
            }
        return result


class NotificationBulkActionSerializer(serializers.Serializer):
    """
    Serializer pour effectuer des actions de masse sur les notifications.
    """
    action = serializers.ChoiceField(
        choices=['mark_all_read', 'archive_all', 'archive_read'],
        help_text="Action à effectuer"
    )
    notif_type = serializers.ChoiceField(
        choices=[choice[0] for choice in Notification.NOTIF_TYPES] + ['all'],
        default='all',
        help_text="Type de notification concerné"
    )

    def save(self, **kwargs):
        """Applique l'action en masse sur les notifications de l'utilisateur."""
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("L'utilisateur est requis pour cette action.")

        action = self.validated_data['action']
        notif_type = self.validated_data['notif_type']

        queryset = user.notifications.all()
        if notif_type != 'all':
            queryset = queryset.filter(notif_type=notif_type)

        if action == 'mark_all_read':
            count = queryset.filter(is_read=False).update(is_read=True, read_at=timezone.now())
            message = f"{count} notifications marquées comme lues"
        elif action == 'archive_all':
            count = queryset.filter(archived=False).update(archived=True)
            message = f"{count} notifications archivées"
        elif action == 'archive_read':
            count = queryset.filter(is_read=True, archived=False).update(archived=True)
            message = f"{count} notifications lues archivées"
        else:
            raise serializers.ValidationError("Action inconnue.")

        return {'success': True, 'count': count, 'message': message}



================================================
FILE: Myevol_app/serializers/objective_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.db.models import Count

from ..models.objective_model import Objective

User = get_user_model()


class ObjectiveSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Objective.
    
    Expose les objectifs définis par l'utilisateur avec leurs métadonnées
    et les champs calculés comme progress_percent, days_remaining, etc.
    """
    progress_percent = serializers.IntegerField(read_only=True)
    days_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    is_achieved = serializers.SerializerMethodField()
    is_due_today = serializers.SerializerMethodField()
    entries_done = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Objective
        fields = [
            'id', 'user', 'user_username', 'title', 'category', 'done',
            'target_date', 'target_value', 'created_at',
            'progress_percent', 'days_remaining', 'is_overdue',
            'is_achieved', 'is_due_today', 'entries_done', 'status'
        ]
        read_only_fields = ['created_at', 'progress_percent', 'days_remaining', 
                           'is_overdue', 'is_achieved', 'is_due_today', 'entries_done', 'status']
    
    def get_days_remaining(self, obj):
        """Retourne le nombre de jours restants avant la date cible."""
        return obj.days_remaining()
    
    def get_is_overdue(self, obj):
        """Vérifie si l'objectif est en retard."""
        return obj.is_overdue()
    
    def get_is_achieved(self, obj):
        """Vérifie si l'objectif est atteint."""
        return obj.is_achieved()
    
    def get_is_due_today(self, obj):
        """Vérifie si la date cible de l'objectif est aujourd'hui."""
        return obj.is_due_today()
    
    def get_entries_done(self, obj):
        """Compte le nombre d'entrées correspondant à la catégorie de cet objectif."""
        return obj.entries_done()
    
    def get_status(self, obj):
        """
        Retourne le statut textuel de l'objectif.
        
        Statuts possibles:
        - 'completed': objectif terminé
        - 'overdue': objectif en retard
        - 'due_today': échéance aujourd'hui
        - 'upcoming': à venir
        """
        if obj.done:
            return 'completed'
        if obj.is_overdue():
            return 'overdue'
        if obj.is_due_today():
            return 'due_today'
        return 'upcoming'
    
    def validate_target_date(self, value):
        """Vérifie que la date cible n'est pas dans le passé."""
        if value < timezone.now().date():
            raise serializers.ValidationError("La date cible ne peut pas être dans le passé.")
        return value
    
    def create(self, validated_data):
        """Création d'un objectif avec l'utilisateur courant."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class ObjectiveListSerializer(ObjectiveSerializer):
    """
    Serializer pour la liste des objectifs.
    
    Version allégée pour l'affichage dans une liste.
    """
    class Meta(ObjectiveSerializer.Meta):
        fields = [
            'id', 'title', 'category', 'done', 'target_date',
            'progress_percent', 'days_remaining', 'status'
        ]


class ObjectiveDetailSerializer(ObjectiveSerializer):
    """
    Serializer pour les détails d'un objectif.
    
    Version étendue pour l'affichage détaillé d'un objectif.
    """
    formatted_target_date = serializers.SerializerMethodField()
    time_until_due = serializers.SerializerMethodField()
    
    class Meta(ObjectiveSerializer.Meta):
        fields = ObjectiveSerializer.Meta.fields + ['formatted_target_date', 'time_until_due']
    
    def get_formatted_target_date(self, obj):
        """Formatte la date cible de façon lisible."""
        return obj.target_date.strftime("%d %B %Y")
    
    def get_time_until_due(self, obj):
        """
        Retourne le temps restant avant l'échéance sous forme lisible.
        Par exemple: "3 jours", "Aujourd'hui", "En retard de 2 jours"
        """
        days = obj.days_remaining()
        
        if days < 0:
            return f"En retard de {abs(days)} jour{'s' if abs(days) > 1 else ''}"
        elif days == 0:
            return "Aujourd'hui"
        elif days == 1:
            return "Demain"
        elif days < 7:
            return f"{days} jours"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} semaine{'s' if weeks > 1 else ''}"
        else:
            months = days // 30
            return f"{months} mois"


class ObjectiveCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer pour marquer un objectif comme complété.
    
    Utilisé uniquement pour mettre à jour le champ 'done'.
    """
    class Meta:
        model = Objective
        fields = ['done']


class ObjectiveStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques des objectifs.
    
    Fournit des statistiques globales sur les objectifs d'un utilisateur.
    """
    total = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    overdue = serializers.SerializerMethodField()
    by_category = serializers.SerializerMethodField()
    upcoming_today = serializers.SerializerMethodField()
    upcoming_week = serializers.SerializerMethodField()
    recent_completions = serializers.SerializerMethodField()
    
    def get_total(self, user):
        """Nombre total d'objectifs."""
        return user.objectives.count()

    def get_completed(self, user):
        """Nombre total d'objectifs complétés."""
        return user.objectives.filter(done=True).count()

    def get_completion_rate(self, user):
        """Taux de complétion en pourcentage."""
        total = self.get_total(user)
        if total == 0:
            return 0.0
        completed = self.get_completed(user)
        return round((completed / total) * 100, 1)

    def get_overdue(self, user):
        """Nombre d'objectifs en retard."""
        today = timezone.now().date()
        return user.objectives.filter(done=False, target_date__lt=today).count()

    def get_by_category(self, user):
        """Répartition des objectifs par catégorie."""
        categories = user.objectives.values('category').annotate(count=Count('category')).order_by('-count')
        return {cat['category']: cat['count'] for cat in categories}

    def get_upcoming_today(self, user):
        """Nombre d'objectifs dus aujourd'hui."""
        today = timezone.now().date()
        return user.objectives.filter(done=False, target_date=today).count()

    def get_upcoming_week(self, user):
        """Nombre d'objectifs dont l'échéance est dans les 7 prochains jours."""
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        return user.objectives.filter(done=False, target_date__gt=today, target_date__lte=end_of_week).count()

    def get_recent_completions(self, user):
        """Liste des objectifs récemment complétés (7 derniers jours)."""
        last_week = timezone.now().date() - timedelta(days=7)
        recent = user.objectives.filter(done=True, target_date__gte=last_week).order_by('-target_date')[:5]
        return ObjectiveListSerializer(recent, many=True).data


class ObjectiveUpcomingSerializer(serializers.Serializer):
    """
    Serializer pour les objectifs à venir.
    
    Regroupe les objectifs par échéance (aujourd'hui, cette semaine, ce mois).
    """
    today = serializers.SerializerMethodField()
    this_week = serializers.SerializerMethodField()
    this_month = serializers.SerializerMethodField()

    def get_queryset(self, user):
        """Base queryset filtré sur l'utilisateur et non terminé."""
        return Objective.objects.filter(user=user, done=False)

    def get_today(self, user):
        """Objectifs dus aujourd'hui."""
        today = timezone.now().date()
        return ObjectiveListSerializer(
            self.get_queryset(user).filter(target_date=today).order_by('title'), many=True
        ).data

    def get_this_week(self, user):
        """Objectifs dus cette semaine (hors aujourd'hui)."""
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        end_of_week = today + timedelta(days=7)
        return ObjectiveListSerializer(
            self.get_queryset(user).filter(target_date__gte=tomorrow, target_date__lte=end_of_week).order_by('target_date'), many=True
        ).data

    def get_this_month(self, user):
        """Objectifs dus ce mois-ci (hors cette semaine)."""
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        end_of_month = today + timedelta(days=30)
        return ObjectiveListSerializer(
            self.get_queryset(user).filter(target_date__gt=end_of_week, target_date__lte=end_of_month).order_by('target_date'), many=True
        ).data


class ObjectiveCategorySerializer(serializers.Serializer):
    """
    Serializer pour les suggestions de catégories d'objectifs.
    
    Retourne les catégories les plus utilisées par l'utilisateur.
    """
    categories = serializers.SerializerMethodField()

    def get_categories(self, user):
        """Liste des catégories les plus utilisées."""
        categories = Objective.objects.filter(user=user) \
            .values('category') \
            .annotate(count=Count('category')) \
            .order_by('-count')[:10]
        return [item['category'] for item in categories]



================================================
FILE: Myevol_app/serializers/quote_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count

from ..models.quote_model import Quote


class QuoteSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Quote.
    
    Expose les citations inspirantes avec leurs métadonnées.
    """
    length = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'text', 'author', 'mood_tag', 'length'
        ]
    
    def get_length(self, obj):
        """Retourne la longueur du texte de la citation."""
        return obj.length()


class QuoteDetailSerializer(QuoteSerializer):
    """
    Serializer pour les détails d'une citation.
    
    Version étendue pour l'affichage détaillé d'une citation.
    """
    author_quote_count = serializers.SerializerMethodField()
    formatted_quote = serializers.SerializerMethodField()
    
    class Meta(QuoteSerializer.Meta):
        fields = QuoteSerializer.Meta.fields + ['author_quote_count', 'formatted_quote']
    
    def get_author_quote_count(self, obj):
        """Retourne le nombre de citations disponibles de cet auteur."""
        if not obj.author:
            return 0
        return Quote.objects.filter(author=obj.author).count()
    
    def get_formatted_quote(self, obj):
        """Retourne la citation formatée pour l'affichage."""
        author = obj.author if obj.author else "Inconnu"
        return {
            'text': obj.text,
            'author': author,
            'display': f'"{obj.text}" — {author}'
        }


class RandomQuoteSerializer(serializers.Serializer):
    """
    Serializer pour obtenir une citation aléatoire.
    
    Prend en charge un filtre de mood_tag optionnel.
    """
    mood_tag = serializers.CharField(required=False, allow_blank=True)
    
    def to_representation(self, instance):
        """
        Retourne une citation aléatoire selon le mood_tag spécifié.
        """
        mood_tag = instance.get('mood_tag')
        quote = Quote.get_random(mood_tag)
        
        if not quote:
            return {
                'success': False,
                'message': f"Aucune citation trouvée{f' avec le tag {mood_tag}' if mood_tag else ''}."
            }
            
        return {
            'success': True,
            'quote': QuoteDetailSerializer(quote).data
        }


class DailyQuoteSerializer(serializers.Serializer):
    """
    Serializer pour obtenir la citation du jour.
    
    Prend en charge une personnalisation selon l'utilisateur.
    """
    def to_representation(self, instance):
        """
        Retourne la citation du jour, potentiellement personnalisée.
        """
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        quote = Quote.get_daily_quote(user if user and getattr(user, 'is_authenticated', False) else None)
        
        if not quote:
            return {
                'success': False,
                'message': "Aucune citation du jour disponible."
            }
            
        return {
            'success': True,
            'date': timezone.now().date().isoformat(),
            'quote': QuoteDetailSerializer(quote).data
        }


class AuthorListSerializer(serializers.Serializer):
    """
    Serializer pour obtenir la liste des auteurs avec leur nombre de citations.
    """
    
    def to_representation(self, instance):
        """
        Retourne la liste des auteurs disponibles avec des statistiques.
        """
        authors = Quote.get_authors_list()
        total_quotes = Quote.objects.count()
        unknown_quotes = Quote.objects.filter(author='').count()
        
        return {
            'success': True,
            'total_quotes': total_quotes,
            'unknown_author_quotes': unknown_quotes,
            'authors_count': len(authors),
            'authors': [{
                'name': author['author'],
                'quotes_count': author['count']
            } for author in authors]
        }


class MoodTagSerializer(serializers.Serializer):
    """
    Serializer pour obtenir la liste des mood_tags avec leur nombre de citations.
    """
    
    def to_representation(self, instance):
        """
        Retourne la liste des mood_tags disponibles avec des statistiques.
        """
        mood_tags = Quote.objects.values('mood_tag').annotate(
            count=Count('id')
        ).order_by('mood_tag')
        
        return {
            'success': True,
            'mood_tags': [{
                'tag': tag['mood_tag'] or 'untagged',
                'count': tag['count']
            } for tag in mood_tags]
        }


class QuoteSearchSerializer(serializers.Serializer):
    """
    Serializer pour rechercher des citations.
    """
    query = serializers.CharField(required=True)
    author = serializers.CharField(required=False, allow_blank=True)
    mood_tag = serializers.CharField(required=False, allow_blank=True)
    
    def to_representation(self, instance):
        """
        Effectue une recherche dans les citations selon les critères fournis.
        """
        query = instance.get('query', '').strip()
        author = instance.get('author', '').strip()
        mood_tag = instance.get('mood_tag', '').strip()
        
        if not query and not author and not mood_tag:
            return {
                'success': False,
                'message': "Veuillez fournir au moins un critère de recherche."
            }
        
        quotes = Quote.objects.all()
        
        if query:
            quotes = quotes.filter(text__icontains=query)
        
        if author:
            quotes = quotes.filter(author__icontains=author)
        
        if mood_tag:
            quotes = quotes.filter(mood_tag=mood_tag)
        
        results = quotes.order_by('author') if quotes.exists() else Quote.objects.none()
        
        return {
            'success': True,
            'count': results.count(),
            'results': QuoteSerializer(results, many=True).data
        }



================================================
FILE: Myevol_app/serializers/stats_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from collections import OrderedDict
from django.contrib.auth import get_user_model

from ..models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat

User = get_user_model()

class DailyStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques journalières."""
    day_of_week = serializers.SerializerMethodField()
    is_weekend = serializers.SerializerMethodField()
    date_formatted = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = DailyStat
        fields = [
            'id', 'user', 'user_username', 'date', 'date_formatted',
            'entries_count', 'mood_average', 'categories',
            'day_of_week', 'is_weekend', 'top_category'
        ]
        read_only_fields = fields

    def get_day_of_week(self, obj):
        return obj.day_of_week()

    def get_is_weekend(self, obj):
        return obj.is_weekend()

    def get_date_formatted(self, obj):
        return obj.date.strftime('%d %B %Y')

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]


class WeeklyStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques hebdomadaires."""
    week_end = serializers.SerializerMethodField()
    week_number = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    date_range = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = WeeklyStat
        fields = [
            'id', 'user', 'user_username', 'week_start', 'week_end',
            'week_number', 'entries_count', 'mood_average',
            'categories', 'top_category', 'date_range'
        ]
        read_only_fields = fields

    def get_week_end(self, obj):
        return obj.week_end()

    def get_week_number(self, obj):
        return obj.week_number()

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]

    def get_date_range(self, obj):
        week_end = obj.week_end()
        return {
            'start': obj.week_start.strftime('%d/%m/%Y'),
            'end': week_end.strftime('%d/%m/%Y'),
            'display': f"Du {obj.week_start.strftime('%d %B')} au {week_end.strftime('%d %B %Y')}"
        }


class MonthlyStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques mensuelles."""
    month_end = serializers.SerializerMethodField()
    month_name = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    date_range = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = MonthlyStat
        fields = [
            'id', 'user', 'user_username', 'month_start', 'month_end',
            'month_name', 'entries_count', 'mood_average',
            'categories', 'top_category', 'date_range'
        ]
        read_only_fields = fields

    def get_month_end(self, obj):
        """Retourne le dernier jour du mois."""
        next_month = (obj.month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        return next_month - timedelta(days=1)

    def get_month_name(self, obj):
        return obj.month_start.strftime('%B %Y')

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]

    def get_date_range(self, obj):
        month_end = self.get_month_end(obj)
        return {
            'start': obj.month_start.strftime('%d/%m/%Y'),
            'end': month_end.strftime('%d/%m/%Y'),
            'display': f"Du {obj.month_start.strftime('%d %B')} au {month_end.strftime('%d %B %Y')}"
        }



class AnnualStatSerializer(serializers.ModelSerializer):
    """Serializer pour les statistiques annuelles."""
    year_end = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AnnualStat
        fields = [
            'id', 'user', 'user_username', 'year_start', 'year_end',
            'year', 'entries_count', 'mood_average',
            'categories', 'top_category'
        ]
        read_only_fields = fields

    def get_year_end(self, obj):
        return obj.year_start.replace(month=12, day=31)

    def get_year(self, obj):
        return obj.year_start.year

    def get_top_category(self, obj):
        if not obj.categories:
            return None
        return max(obj.categories.items(), key=lambda x: x[1])[0]


class StatsOverviewSerializer(serializers.Serializer):
    """Serializer pour afficher un résumé global des statistiques."""
    daily = serializers.SerializerMethodField()
    weekly = serializers.SerializerMethodField()
    monthly = serializers.SerializerMethodField()
    annual = serializers.SerializerMethodField()
    trends = serializers.SerializerMethodField()

    def get_daily(self, user):
        today = timezone.now().date()
        stat, _ = DailyStat.objects.get_or_create(user=user, date=today)
        return DailyStatSerializer(stat).data

    def get_weekly(self, user):
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        stat, _ = WeeklyStat.objects.get_or_create(user=user, week_start=week_start)
        return WeeklyStatSerializer(stat).data

    def get_monthly(self, user):
        today = timezone.now().date()
        month_start = today.replace(day=1)
        stat, _ = MonthlyStat.objects.get_or_create(user=user, month_start=month_start)
        return MonthlyStatSerializer(stat).data

    def get_annual(self, user):
        today = timezone.now().date()
        year_start = today.replace(month=1, day=1)
        stat, _ = AnnualStat.objects.get_or_create(user=user, year_start=year_start)
        return AnnualStatSerializer(stat).data

    def get_trends(self, user):
        today = timezone.now().date()
        daily_stats = DailyStat.objects.filter(user=user, date__gte=today - timedelta(days=30)).order_by('date')

        if not daily_stats.exists():
            return {
                'entries_trend': 'stable',
                'mood_trend': 'stable',
                'entries_change': 0,
                'mood_change': 0,
                'most_active_day': None,
                'best_mood_day': None
            }

        past_15_days = daily_stats.filter(date__gte=today - timedelta(days=15))
        previous_15_days = daily_stats.filter(date__lt=today - timedelta(days=15))

        recent_entries_avg = sum(s.entries_count for s in past_15_days) / max(1, len(past_15_days))
        previous_entries_avg = sum(s.entries_count for s in previous_15_days) / max(1, len(previous_15_days))

        recent_moods = [s.mood_average for s in past_15_days if s.mood_average is not None]
        previous_moods = [s.mood_average for s in previous_15_days if s.mood_average is not None]

        recent_mood_avg = sum(recent_moods) / max(1, len(recent_moods)) if recent_moods else 0
        previous_mood_avg = sum(previous_moods) / max(1, len(previous_moods)) if previous_moods else 0

        entries_change = recent_entries_avg - previous_entries_avg
        mood_change = recent_mood_avg - previous_mood_avg

        entries_trend = 'up' if entries_change > 0.5 else ('down' if entries_change < -0.5 else 'stable')
        mood_trend = 'up' if mood_change > 0.5 else ('down' if mood_change < -0.5 else 'stable')

        most_active = max(daily_stats, key=lambda s: s.entries_count, default=None)
        best_mood = max((s for s in daily_stats if s.mood_average is not None), key=lambda s: s.mood_average, default=None)

        return {
            'entries_trend': entries_trend,
            'mood_trend': mood_trend,
            'entries_change': round(entries_change, 1),
            'mood_change': round(mood_change, 1),
            'most_active_day': {
                'date': most_active.date.strftime('%d/%m/%Y'),
                'day_of_week': most_active.day_of_week(),
                'entries_count': most_active.entries_count
            } if most_active else None,
            'best_mood_day': {
                'date': best_mood.date.strftime('%d/%m/%Y'),
                'day_of_week': best_mood.day_of_week(),
                'mood_average': best_mood.mood_average
            } if best_mood else None
        }

class StatsCategoryAnalysisSerializer(serializers.Serializer):
    """Serializer pour l'analyse des catégories."""
    period = serializers.ChoiceField(choices=['week', 'month', 'year', 'all'], default='month')

    def to_representation(self, instance):
        user = instance.get('user')
        period = instance.get('period', 'month')

        if not user:
            return {'error': 'Utilisateur non spécifié'}

        today = timezone.now().date()

        if period == 'week':
            start_date = today - timedelta(days=today.weekday())
            stat, _ = WeeklyStat.objects.get_or_create(user=user, week_start=start_date)
        elif period == 'month':
            start_date = today.replace(day=1)
            stat, _ = MonthlyStat.objects.get_or_create(user=user, month_start=start_date)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
            stat, _ = AnnualStat.objects.get_or_create(user=user, year_start=start_date)
        else:  # all
            stats = AnnualStat.objects.filter(user=user)
            if not stats.exists():
                return {
                    'title': "Analyse de toutes les entrées",
                    'categories': {},
                    'total_entries': 0,
                    'period': period
                }
            categories = {}
            total_entries = 0
            for stat in stats:
                total_entries += stat.entries_count
                for category, count in stat.categories.items():
                    categories[category] = categories.get(category, 0) + count
            return {
                'title': "Analyse de toutes les entrées",
                'categories': OrderedDict(sorted({
                    k: {'count': v, 'percentage': round((v/total_entries)*100, 1) if total_entries > 0 else 0}
                    for k, v in categories.items()
                }.items(), key=lambda x: x[1]['count'], reverse=True)),
                'total_entries': total_entries,
                'period': period
            }

        categories = {
            k: {
                'count': v,
                'percentage': round((v / stat.entries_count) * 100, 1) if stat.entries_count > 0 else 0
            }
            for k, v in stat.categories.items()
        }

        return {
            'title': f"Analyse des entrées - {period}",
            'categories': OrderedDict(sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True)),
            'total_entries': stat.entries_count,
            'period': period,
            'date_range': {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': (start_date + timedelta(days=6) if period == 'week' else
                        (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                        if period == 'month' else
                        start_date.replace(month=12, day=31)
                    ).strftime('%d/%m/%Y')
            }
        }




================================================
FILE: Myevol_app/serializers/user_serializers.py
================================================
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from collections import OrderedDict
from django.db.models import Count

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User.
    
    Expose les informations de base de l'utilisateur.
    """
    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    total_entries = serializers.ReadOnlyField()
    current_streak = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'short_name',
            'avatar_url', 'xp', 'total_entries', 'current_streak',
            'longest_streak', 'level', 'level_progress', 'date_joined',
            'last_login'
        ]
        read_only_fields = [
            'total_entries', 'current_streak', 'longest_streak',
            'level', 'level_progress', 'date_joined', 'last_login'
        ]
    
    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur."""
        return obj.get_full_name()
    
    def get_short_name(self, obj):
        """Retourne le prénom ou le username si le prénom est vide."""
        return obj.get_short_name()
    
    def get_current_streak(self, obj):
        """Retourne la série actuelle de jours consécutifs avec entrées."""
        return obj.current_streak()
    
    def get_level(self, obj):
        """Retourne le niveau actuel de l'utilisateur."""
        return obj.level()
    
    def get_level_progress(self, obj):
        """Retourne la progression du niveau actuel en pourcentage."""
        return obj.level_progress()


class UserProfileSerializer(UserSerializer):
    """
    Serializer pour le profil complet d'un utilisateur.
    
    Étend UserSerializer avec des statistiques supplémentaires.
    """
    mood_average = serializers.SerializerMethodField()
    stats_summary = serializers.SerializerMethodField()
    activity_summary = serializers.SerializerMethodField()
    badges_count = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'mood_average', 'stats_summary', 'activity_summary',
            'badges_count'
        ]
    
    def get_mood_average(self, obj):
        """Retourne la moyenne d'humeur sur différentes périodes."""
        mood_7d = obj.mood_average(days=7)
        mood_30d = obj.mood_average(days=30)
        mood_all = obj.mood_average(days=None)
        
        return {
            'week': round(mood_7d, 1) if mood_7d is not None else None,
            'month': round(mood_30d, 1) if mood_30d is not None else None,
            'all_time': round(mood_all, 1) if mood_all is not None else None
        }
    
    def get_stats_summary(self, obj):
        """Retourne un résumé des statistiques de l'utilisateur."""
        return {
            'total_entries': obj.total_entries,
            'current_streak': obj.current_streak(),
            'longest_streak': obj.longest_streak,
            'level': obj.level(),
            'xp': obj.xp
        }
    
    def get_activity_summary(self, obj):
        """Retourne un résumé de l'activité récente de l'utilisateur."""
        today = timezone.now().date()
        entries_today = obj.entries_today()
        
        # Calculer les entrées des 7 derniers jours
        last_week = today - timedelta(days=7)
        entries_last_week = obj.entries.filter(
            created_at__date__gte=last_week
        ).count()
        
        # Calculer les entrées des 30 derniers jours
        last_month = today - timedelta(days=30)
        entries_last_month = obj.entries.filter(
            created_at__date__gte=last_month
        ).count()
        
        # Déterminer si l'utilisateur est actif
        is_active = entries_today > 0
        
        return {
            'entries_today': entries_today,
            'entries_last_week': entries_last_week,
            'entries_last_month': entries_last_month,
            'is_active_today': is_active,
            'days_since_last_entry': 0 if is_active else self._days_since_last_entry(obj)
        }
    
    def get_badges_count(self, obj):
        """Retourne le nombre de badges de l'utilisateur."""
        return obj.badges.count()
    
    def _days_since_last_entry(self, obj):
        """Calcule le nombre de jours depuis la dernière entrée."""
        today = timezone.now().date()
        last_entry = obj.entries.order_by('-created_at').first()
        
        if not last_entry:
            return None
            
        last_date = last_entry.created_at.date()
        return (today - last_date).days


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour mettre à jour les informations de l'utilisateur.
    
    Permet de modifier le profil sans toucher aux champs sensibles.
    """
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Mot de passe actuel (requis pour changer le mot de passe)"
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Nouveau mot de passe"
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'avatar_url', 'current_password', 'new_password'
        ]
    
    def validate(self, data):
        """Validation des données de mise à jour du profil."""
        # Si on essaie de changer le mot de passe
        if 'new_password' in data:
            # Le mot de passe actuel est obligatoire
            if not data.get('current_password'):
                raise serializers.ValidationError({
                    'current_password': "Le mot de passe actuel est requis pour changer le mot de passe."
                })
            
            # Vérifier que le mot de passe actuel est correct
            if not self.instance.check_password(data.get('current_password')):
                raise serializers.ValidationError({
                    'current_password': "Le mot de passe actuel est incorrect."
                })
        
        return data
    
    def update(self, instance, validated_data):
        """Mise à jour de l'utilisateur avec gestion du mot de passe."""
        # Gérer le changement de mot de passe séparément
        if 'new_password' in validated_data:
            instance.set_password(validated_data.pop('new_password'))
        
        # Supprimer le mot de passe actuel des données à mettre à jour
        validated_data.pop('current_password', None)
        
        # Mettre à jour les autres champs
        return super().update(instance, validated_data)


class UserStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques détaillées d'un utilisateur.
    
    Fournit des insights sur l'activité et les performances de l'utilisateur.
    """
    mood_stats = serializers.SerializerMethodField()
    streak_stats = serializers.SerializerMethodField()
    activity_stats = serializers.SerializerMethodField()
    category_distribution = serializers.SerializerMethodField()
    
    def get_mood_stats(self, user):
        """Statistiques détaillées sur les humeurs de l'utilisateur."""
        # Moyennes d'humeur sur différentes périodes
        mood_7d = user.mood_average(days=7)
        mood_30d = user.mood_average(days=30)
        mood_90d = user.mood_average(days=90)
        mood_all = user.mood_average(days=None)
        
        # Calcul de la tendance
        trend = 'stable'
        if mood_7d is not None and mood_30d is not None:
            diff = mood_7d - mood_30d
            if diff > 0.5:
                trend = 'up'
            elif diff < -0.5:
                trend = 'down'
        
        # Répartition des humeurs
        mood_distribution = list(user.entries.values('mood')
                                 .annotate(count=Count('id'))
                                 .order_by('mood'))
        
        return {
            'averages': {
                'week': round(mood_7d, 1) if mood_7d is not None else None,
                'month': round(mood_30d, 1) if mood_30d is not None else None,
                'quarter': round(mood_90d, 1) if mood_90d is not None else None,
                'all_time': round(mood_all, 1) if mood_all is not None else None
            },
            'trend': trend,
            'distribution': {
                str(item['mood']): item['count'] for item in mood_distribution if item['mood'] is not None
            }
        }
    
    def get_streak_stats(self, user):
        """Statistiques sur les séries d'entrées consécutives."""
        return {
            'current': user.current_streak(),
            'longest': user.longest_streak,
            'has_entry_today': user.entries_today() > 0
        }
    
    def get_activity_stats(self, user):
        """Statistiques sur l'activité générale de l'utilisateur."""
        today = timezone.now().date()
        
        # Entrées par jour de la semaine
        from django.db.models import Count
        from django.db.models.functions import ExtractWeekDay
        
        weekday_counts = list(user.entries
                              .annotate(weekday=ExtractWeekDay('created_at'))
                              .values('weekday')
                              .annotate(count=Count('id'))
                              .order_by('weekday'))
        
        # Convertir en format jour de la semaine (0=Lundi, 6=Dimanche)
        weekday_names = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        weekday_distribution = {}
        
        for day in range(7):
            # Rechercher le jour dans les résultats
            count_entry = next((item for item in weekday_counts if item['weekday'] == day + 1), None)
            weekday_distribution[weekday_names[day]] = count_entry['count'] if count_entry else 0
        
        # Calculer les entrées par mois (12 derniers mois)
        from django.db.models.functions 