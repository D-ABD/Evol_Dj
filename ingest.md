voici mon projet cherche la solution: 
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
python_files = tests/test_*.py



================================================
FILE: requirements.txt
================================================
amqp==5.3.1
asgiref==3.8.1
async-timeout==5.0.1
billiard==4.2.1
celery==5.5.1
click==8.1.8
click-didyoumean==0.3.1
click-plugins==1.1.1
click-repl==0.3.0
cron-descriptor==1.4.5
Django==4.2.20
django-celery-beat==2.8.0
django-timezone-field==7.1
kombu==5.5.3
prompt_toolkit==3.0.51
psycopg2-binary==2.9.10
python-crontab==3.2.0
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
redis==5.2.1
six==1.17.0
sqlparse==0.5.3
typing_extensions==4.13.2
tzdata==2025.2
vine==5.1.0
wcwidth==0.2.13



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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
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
        import Myevol_app.signals.event_log_signals



================================================
FILE: Myevol_app/forms.py
================================================



================================================
FILE: Myevol_app/tasks.py
================================================
from celery import shared_task
from django.utils.timezone import now
from .models import Notification

@shared_task
def send_scheduled_notifications():
    """
    Tâche périodique pour envoyer les notifications programmées.
    
    Cette tâche est exécutée par Celery selon une planification définie dans les paramètres.
    Elle identifie toutes les notifications programmées dont la date d'échéance est atteinte
    et n'ont pas encore été lues, puis effectue les actions nécessaires pour les envoyer.
    
    Returns:
        str: Message indiquant le nombre de notifications traitées
    """
    # Récupère toutes les notifications programmées dont la date d'envoi est arrivée
    # et qui n'ont pas encore été lues
    qs = Notification.objects.filter(scheduled_at__lte=now(), is_read=False)
    
    count = 0  # Compteur pour suivre le nombre de notifications traitées
    
    for notif in qs:
        # Ici, implémentez la logique d'envoi appropriée selon le type de notification
        # Par exemple : envoi d'email, notification push, SMS, etc.
        # Exemple : send_push_notification(notif.user.device_token, notif.message)
        
        notif.mark_as_read()  # Marque la notification comme lue après l'envoi
        count += 1
    
    # Retourne un message descriptif pour les logs Celery
    return f"{count} notifications envoyées"


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
FILE: Myevol_app/migrations/__init__.py
================================================



================================================
FILE: Myevol_app/models/__init__.py
================================================
# Myevol_app/models/__init__.py

from .user_model import User
from .journal_model import JournalEntry, JournalMedia
from .notification_model import Notification
from .objective_model import Objective
from .badge_model import Badge, BadgeTemplate
from .challenge_model import Challenge, ChallengeProgress
from .stats_model import DailyStat, WeeklyStat
from .event_log_model import EventLog
from .userPreference_model import UserPreference 
from .quote_model import Quote



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

        if is_new:
            logger.info(f"Nouvelle progression créée pour {self.user.username} sur le défi '{self.challenge.title}'")



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
        logger.info(f"[LOG] {user.username if user else 'System'} > {action} > {description} > Severity: {severity}")
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
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date et heure de création de l’entrée")
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
        
        Utilisation dans l'API:
            La création d'une entrée via l'API déclenchera automatiquement
            toutes ces actions associées. Pas besoin de code supplémentaire
            dans les vues API pour ces fonctionnalités.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # ⏱ Import local pour éviter les imports circulaires
            from .stats_model import DailyStat
            from .challenge_model import check_challenges

            # ➕ Mise à jour des statistiques journalières
            DailyStat.generate_for_user(self.user, self.created_at.date())

            # ✅ Vérification des défis
            check_challenges(self.user)

            # 🏅 Mise à jour des badges
            self.user.update_badges()

            # 🔥 Mise à jour des séries de jours consécutifs
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


# 📎 Médias associés à une entrée de journal
class JournalMedia(models.Model):
    """
    Modèle pour stocker les fichiers multimédias associés aux entrées de journal.
    Permet aux utilisateurs d'enrichir leurs entrées avec des images ou des enregistrements audio.
    
    API Endpoints suggérés:
    - POST /api/journal-entries/{id}/media/ - Ajouter un média à une entrée
    - DELETE /api/journal-entries/media/{id}/ - Supprimer un média
    - GET /api/journal-entries/{id}/media/ - Lister les médias d'une entrée
    
    Exemple de sérialisation JSON:
    {
        "id": 45,
        "entry": 123,
        "type": "image",
        "file": "/media/journal_media/image123.jpg",
        "created_at": "2025-04-19T15:31:12Z"
    }
    """
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="journal_media/")
    type = models.CharField(
        max_length=10,
        choices=[("image", "Image"), ("audio", "Audio")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ['created_at']
        
        """
        Permissions API:
        - Un utilisateur ne doit accéder qu'aux médias liés à ses propres entrées
        - Limiter la taille des uploads
        - Valider les types MIME des fichiers
        """

    def __str__(self):
        return f"{self.get_type_display()} pour {self.entry}"
        
    def file_url(self):
        """
        Retourne l'URL complète du fichier.
        
        Returns:
            str: URL du fichier média
            
        Utilisation dans l'API:
            Ce champ doit être inclus dans la sérialisation pour faciliter
            l'affichage direct dans l'interface.
            
        Exemple dans un sérialiseur:
            @property
            def file_url(self):
                return self.instance.file.url if self.instance.file else None
        """
        if self.file:
            return self.file.url
        return None
        
    def file_size(self):
        """
        Retourne la taille du fichier en octets.
        
        Returns:
            int: Taille du fichier en octets
            
        Utilisation dans l'API:
            Utile pour l'affichage dans l'interface ou pour les quotas.
        """
        if self.file:
            return self.file.size
        return 0
        
    def validate_file_type(self):
        """
        Vérifie si le type de fichier correspond au type déclaré.
        
        Raises:
            ValidationError: Si le type de fichier ne correspond pas
            
        Utilisation dans l'API:
            Cette validation doit être reproduite dans le sérialiseur
            pour assurer la cohérence des données.
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
# MyEvol_app/models/notification_model.py

from django.db import models
from django.conf import settings
from django.utils.timezone import now
import logging

User = settings.AUTH_USER_MODEL

logger = logging.getLogger(__name__)

class Notification(models.Model):
    """
    Modèle représentant une notification pour un utilisateur.
    Permet d'informer l'utilisateur d'événements importants dans l'application.
    """

    NOTIF_TYPES = [
        ('badge', 'Badge débloqué'),
        ('objectif', 'Objectif atteint'),
        ('statistique', 'Mise à jour statistique'),
        ('info', 'Information générale'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(help_text="Contenu de la notification")
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info', help_text="Type de notification")
    is_read = models.BooleanField(default=False, help_text="Indique si la notification a été lue")
    read_at = models.DateTimeField(null=True, blank=True, help_text="Date de lecture de la notification")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de la notification")
    archived = models.BooleanField(default=False, help_text="Indique si la notification est archivée")
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text="Date programmée pour l'envoi de la notification")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'archived']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

    @property
    def type_display(self):
        """
        Retourne le label lisible du type de notification.
        """
        return dict(self.NOTIF_TYPES).get(self.notif_type, "Information générale")

    def archive(self):
        """
        Archive la notification sans suppression.
        """
        if not self.archived:
            self.archived = True
            self.save(update_fields=['archived'])

    def mark_as_read(self):
        """
        Marque la notification comme lue et enregistre la date de lecture.
        """
        if not self.is_read:
            self.is_read = True
            self.read_at = now()
            self.save(update_fields=['is_read', 'read_at'])

    @classmethod
    def mark_all_as_read(cls, user):
        """
        Marque toutes les notifications non lues d'un utilisateur comme lues.
        """
        unread = cls.objects.filter(user=user, is_read=False, archived=False)
        return unread.update(is_read=True, read_at=now())

    @classmethod
    def create_notification(cls, user, message, notif_type='info', scheduled_at=None):
        """
        Crée une nouvelle notification pour un utilisateur.
        """
        return cls.objects.create(
            user=user,
            message=message,
            notif_type=notif_type,
            scheduled_at=scheduled_at
        )

# Signal : créer une notification lorsque l'utilisateur atteint un objectif
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def notify_user_of_new_goal(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de l'atteinte d'un objectif par un utilisateur.
    Crée une notification pour informer l'utilisateur de cet accomplissement.
    """
    if created:
        # Exemple d'objectif atteint
        Notification.create_notification(
            user=instance,
            message="Félicitations, vous avez atteint un nouvel objectif !",
            notif_type="objectif"
        )
        logger.info(f"Notification de succès d'objectif envoyée à {instance.username}")



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
from .notification_model import Notification
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
        Une notification est créée uniquement si l'objectif vient d'être complété.
        """
        create_notification = kwargs.pop('create_notification', True)
        self.full_clean()  # Appelle clean()

        # Log avant de sauvegarder l'objectif
        logger.info(f"Sauvegarde de l'objectif: {self.title} (État: {'Complété' if self.done else 'En cours'})")

        # Détection du changement d'état
        if not self.done and self.progress() >= 100:
            self.done = True

            if create_notification:
                # Envoi d'une notification si l'objectif est complété
                Notification.objects.create(
                    user=self.user,
                    message=f"🎯 Objectif atteint : {self.title}",
                    notif_type="objectif"
                )
                logger.info(f"Objectif atteint: {self.title} pour {self.user.username}")

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
from datetime import datetime
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

# Signaux pour logguer la création et suppression des citations
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Quote)
def log_quote_creation(sender, instance, created, **kwargs):
    """ Log la création de chaque citation. """
    if created:
        logger.info(f"Nouveau quote créé : {instance.text[:50]}... — {instance.author if instance.author else 'Inconnu'}")

@receiver(post_delete, sender=Quote)
def log_quote_deletion(sender, instance, **kwargs):
    """ Log la suppression de chaque citation. """
    logger.info(f"Citation supprimée : {instance.text[:50]}... — {instance.author if instance.author else 'Inconnu'}")



================================================
FILE: Myevol_app/models/stats_model.py
================================================
from datetime import timedelta
import logging
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from collections import defaultdict
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete

from django.conf import settings
User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)

class WeeklyStat(models.Model):
    """
    Modèle pour stocker les statistiques hebdomadaires d'un utilisateur.
    Agrège les données d'entrées pour fournir des insights sur une période d'une semaine.
    Permet de suivre les tendances et l'évolution sur une échelle de temps plus large que les stats quotidiennes.
    """

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
        """
        Calcule le dernier jour de la semaine.
        """
        return self.week_start + timedelta(days=6)

    def week_number(self):
        """
        Retourne le numéro de semaine dans l'année.
        """
        return self.week_start.isocalendar()[1]

    def top_category(self):
        """
        Retourne la catégorie la plus fréquente.
        """
        if not self.categories:
            return None
        return max(self.categories.items(), key=lambda x: x[1])[0]

    @classmethod
    def generate_for_user(cls, user, reference_date=None):
        """
        Génère ou met à jour les statistiques hebdomadaires pour un utilisateur.
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

        stat, created = cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        return stat

    @classmethod
    def get_trends(cls, user, weeks=10):
        """
        Récupère l'évolution des statistiques sur plusieurs semaines.
        """
        current_week_start = now().date() - timedelta(days=now().date().weekday())
        start_date = current_week_start - timedelta(weeks=weeks)
        
        stats = cls.objects.filter(user=user, week_start__gte=start_date).order_by('week_start')
        
        weeks_labels, entries_data, mood_data = [], [], []
        
        for i in range(weeks + 1):
            week_date = start_date + timedelta(weeks=i)
            week_label = f"{week_date.year}-W{week_date.isocalendar()[1]}"
            weeks_labels.append(week_label)

            stat = next((s for s in stats if s.week_start == week_date), None)
            entries_data.append(stat.entries_count if stat else 0)
            mood_data.append(stat.mood_average if stat else None)
        
        return {
            'weeks': weeks_labels,
            'entries': entries_data,
            'mood': mood_data
        }

@receiver(post_save, sender=WeeklyStat)
def log_weekly_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques hebdomadaires.
    """
    if created:
        logger.info(f"Statistiques hebdomadaires créées pour {instance.user.username} - Semaine du {instance.week_start}")


@receiver(post_delete, sender=WeeklyStat)
def log_weekly_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques hebdomadaires.
    """
    logger.info(f"Statistiques hebdomadaires supprimées pour {instance.user.username} - Semaine du {instance.week_start}")



class DailyStat(models.Model):
    """
    Modèle pour stocker les statistiques journalières d'un utilisateur.
    Agrège les données d'entrées de journal pour une analyse et un affichage efficaces.
    """

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
        """
        Retourne le jour de la semaine en format lisible.
        """
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return days[self.date.weekday()]

    def is_weekend(self):
        """
        Vérifie si la date tombe un weekend.
        """
        return self.date.weekday() >= 5

    @classmethod
    def generate_for_user(cls, user, date=None):
        """
        Génère ou met à jour les statistiques journalières pour une date donnée.
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

        stat, created = cls.objects.update_or_create(
            user=user,
            date=date,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(cat_stats),
            }
        )
        return stat

    @classmethod
    def get_calendar_data(cls, user, month=None, year=None):
        """
        Génère des données pour une visualisation de type calendrier heatmap.
        """
        from datetime import datetime
        if year is None:
            year = now().year
        
        date_filter = {'user': user, 'date__year': year}
        if month is not None:
            date_filter['date__month'] = month

        stats = cls.objects.filter(**date_filter).order_by('date')

        max_count = max([stat.entries_count for stat in stats], default=1)

        result = []
        for stat in stats:
            intensity = stat.entries_count / max_count if max_count > 0 else 0
            result.append({
                'date': stat.date.isoformat(),
                'count': stat.entries_count,
                'mood': stat.mood_average,
                'intensity': round(intensity, 2)
            })
        return result

@receiver(post_save, sender=DailyStat)
def log_daily_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques journalières.
    """
    if created:
        logger.info(f"Statistiques journalières créées pour {instance.user.username} - {instance.date}")


@receiver(post_delete, sender=DailyStat)
def log_daily_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques journalières.
    """
    logger.info(f"Statistiques journalières supprimées pour {instance.user.username} - {instance.date}")

class MonthlyStat(models.Model):
    """
    Modèle pour stocker les statistiques mensuelles d'un utilisateur.
    Permet de suivre les tendances et l'évolution sur une période d'un mois.
    """

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
        """
        Génère ou met à jour les statistiques mensuelles pour un utilisateur.
        """
        if not reference_date:
            reference_date = now().date()

        month_start = reference_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        entries = user.entries.filter(created_at__date__range=(month_start, month_end))
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1

        stat, created = cls.objects.update_or_create(
            user=user,
            month_start=month_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        return stat


class AnnualStat(models.Model):
    """
    Modèle pour stocker les statistiques annuelles d'un utilisateur.
    Permet de suivre les tendances et l'évolution sur une période d'une année.
    """

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
        """
        Génère ou met à jour les statistiques annuelles pour un utilisateur.
        """
        if not reference_date:
            reference_date = now().date()

        year_start = reference_date.replace(month=1, day=1)
        year_end = year_start.replace(month=12, day=31)

        entries = user.entries.filter(created_at__date__range=(year_start, year_end))
        entries_count = entries.count()

        mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
        mood_avg = round(mood_avg, 1) if mood_avg is not None else None

        categories = defaultdict(int)
        for entry in entries:
            categories[entry.category] += 1

        stat, created = cls.objects.update_or_create(
            user=user,
            year_start=year_start,
            defaults={
                "entries_count": entries_count,
                "mood_average": mood_avg,
                "categories": dict(categories),
            }
        )
        return stat



================================================
FILE: Myevol_app/models/user_model.py
================================================
# MyEvol_app/models/user_model.py

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

from ..services.badge_service import update_user_badges
from ..services.streak_service import update_user_streak

from ..services.userpreference_service import create_or_update_preferences
from ..services.user_stats_service import (
    compute_mood_average,
    compute_current_streak,
   
)

# Initialisation du logger
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


def cache_result(timeout=60):
    """
    Décorateur qui met en cache le résultat de la fonction pendant un délai donné.
    Cette méthode est utilisée pour les statistiques comme la répartition des entrées par catégorie.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{self.__class__.__name__}_entries_by_category_{args}_{kwargs}"
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
    Modèle d'utilisateur personnalisé.
    Étend le modèle utilisateur standard avec des fonctionnalités supplémentaires
    pour l'application de suivi personnel.
    """
    email = models.EmailField(
        unique=True,
        help_text="L'email de l'utilisateur, utilisé pour l'authentification."
    )
    longest_streak = models.PositiveIntegerField(
        default=0, editable=False, help_text="La plus longue série d'entrées consécutives."
    )
    avatar_url = models.URLField(
        blank=True, null=True, help_text="URL de l'image de l'avatar de l'utilisateur."
    )
    xp = models.PositiveIntegerField(
        default=0, help_text="Le nombre total de points d'expérience cumulés par l'utilisateur."
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Retourne le nom complet de l'utilisateur.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Retourne le prénom ou le username si le prénom est vide.
        """
        return self.first_name or self.username

    def to_dict(self):
        """
        Représentation de l'utilisateur sous forme de dictionnaire (utile pour les API).
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.get_full_name(),
            "entries": self.total_entries(),
            "current_streak": self.current_streak(),
            "mood_average": self.mood_average(),
            "level": self.level(),
            "level_progress": self.level_progress(),
        }

    @property
    def total_entries(self):
        """
        Retourne le nombre total d'entrées de journal de l'utilisateur.
        """
        return self.entries.count()

    @property
    def mood_average(self, days=7, reference_date=None):
        """
        Calcule la moyenne d'humeur sur les X derniers jours.
        Délégué à user_stats_service.
        """
        return compute_mood_average(self, days, reference_date)

    @property
    def current_streak(self, reference_date=None):
        """
        Calcule la série actuelle de jours consécutifs avec au moins une entrée.
        Utilise le service user_stats.
        """
        return compute_current_streak(self, reference_date)

    @cache_result(timeout=300)  # Cache pendant 5 minutes
    def entries_by_category(self, days=None):
        """
        Renvoie une répartition des entrées par catégorie.
        Délégué à user_stats_service.
        """
        entries = self.entries.all()
        if days:
            entries = entries.filter(created_at__gte=now() - timedelta(days=days))
        return dict(entries.select_related('category').values('category').annotate(count=Count('id')).values_list('category', 'count'))

    def level(self):
        """
        Calcule le niveau actuel de l'utilisateur basé sur le nombre d'entrées.
        Utilise le service `get_user_progress` pour récupérer les données du niveau.
        """
        from ..services.user_stats_service import get_user_progress
        progress = get_user_progress(self.total_entries)
        return progress['level']

    def level_progress(self):
        """
        Retourne la progression du niveau actuel en pourcentage.
        Utilise le service `get_user_progress` pour récupérer la progression.
        """
        from ..services.user_stats_service import get_user_progress
        progress = get_user_progress(self.total_entries)
        return progress['progress']

    def update_badges(self):
        """
        Met à jour les badges débloqués pour l'utilisateur.
        Géré par le service `badge_service`.
        """
        try:
            update_user_badges(self)
            logger.info(f"Badges mis à jour pour l'utilisateur {self.username} (ID: {self.id})")
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des badges pour {self.username} (ID: {self.id}): {e}")

    def update_streaks(self):
        """
        Met à jour la plus longue série d'entrées consécutives.
        Géré par le service `streak_service`.
        """
        update_user_streak(self)
        logger.info(f"Série d'entrées consécutives mise à jour pour l'utilisateur {self.username} (ID: {self.id})")

    def create_default_preferences(self):
        """
        Crée les préférences utilisateur par défaut si elles n'existent pas.
        Utilise le service 'create_or_update_preferences' pour gérer les préférences.
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
        logger.info(f"Préférences par défaut créées pour l'utilisateur {self.username} (ID: {self.id})")
        return preferences

    def add_xp(self, amount):
        """
        Ajoute des points d'expérience à l'utilisateur.
        """
        if amount < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")
        self.xp += amount
        self.save(update_fields=['xp'])
        logger.info(f"{amount} points d'expérience ajoutés à l'utilisateur {self.username} (ID: {self.id}). Total XP: {self.xp}")

    def clean(self):
        """
        Validation avant enregistrement de l'utilisateur.
        """
        if self.xp < 0:
            raise ValidationError("Les points d'expérience ne peuvent pas être négatifs.")
        logger.debug(f"Validation avant enregistrement de l'utilisateur {self.username} (ID: {self.id})")

    def save(self, *args, **kwargs):
        """
        Méthode de sauvegarde personnalisée pour mettre à jour les streaks et badges avant l'enregistrement.
        """
        if self.is_new:
            self.create_default_preferences()
            logger.info(f"Nouvel utilisateur {self.username} (ID: {self.id}) créé avec des préférences par défaut.")
        super(User, self).save(*args, **kwargs)

    @property
    def is_new(self):
        """
        Vérifie si l'utilisateur est nouveau (non encore sauvegardé).
        """
        return self.pk is None

    def get_absolute_url(self):
        """
        Retourne l'URL absolue de l'utilisateur.
        """
        return f"/users/{self.id}/"
        
    def __repr__(self):
        """
        Retourne une représentation de l'objet utilisateur sous forme de chaîne de caractères.
        """
        return f"<User username={self.username}>"

# Invalidation du cache lors de modifications d'entrée
@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def invalidate_cache(sender, instance, **kwargs):
    """
    Fonction pour invalider le cache des résultats liés aux entrées de l'utilisateur
    lorsque des entrées sont ajoutées ou supprimées.
    """
    cache_key = f"{sender.__name__}_entries_by_category_{instance.pk}"
    cache.delete(cache_key)
    logger.info(f"Cache invalidé pour l'utilisateur {instance.username} (ID: {instance.id})")


# ------------------------------------
# Signaux dans signals/user_signals.py
# ------------------------------------
"""""
    @receiver(post_save, sender=User)
    def handle_user_creation(sender, instance, created, **kwargs):
        Signal appelé après la création d'un utilisateur pour :
        - Créer ses préférences par défaut
        - Mettre à jour ses badges
        - Mettre à jour sa série d'entrées consécutives (streak)
        
        Ce signal est déclenché uniquement lors de la création d'un nouvel utilisateur.
    """


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
FILE: Myevol_app/serializers/badge_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/challenge_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/event_log_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/journal_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/notification_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/objective_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/quote_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/stats_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/user_serializer.md
================================================



================================================
FILE: Myevol_app/serializers/user_serializer.py
================================================



================================================
FILE: Myevol_app/serializers/userPreference_serializer.py
================================================



================================================
FILE: Myevol_app/services/badge_service.py
================================================
# services/badge_service.py

import logging
from typing import List, Optional
from ..models.badge_model import Badge, BadgeTemplate
from ..models.event_log_model import EventLog

logger = logging.getLogger(__name__)

def update_user_badges(user, *, log_events: bool = True, return_new_badges: bool = False) -> Optional[List[Badge]]:
    """
    Vérifie tous les BadgeTemplates et attribue les badges éligibles à l’utilisateur.

    Args:
        user (User): L'utilisateur concerné
        log_events (bool): Active l'enregistrement d'un EventLog (True par défaut)
        return_new_badges (bool): Retourne les badges créés si True

    Returns:
        Optional[List[Badge]]: Liste des badges créés, ou None si aucun n’a été créé
    """
    existing_badge_names = set(user.badges.values_list("name", flat=True))
    new_badges = []

    for template in BadgeTemplate.objects.all():
        if template.name in existing_badge_names:
            continue  # L’utilisateur a déjà ce badge

        if template.check_unlock(user):
            try:
                badge = __create_badge(user, template)
                new_badges.append(badge)

                if log_events:
                    EventLog.objects.create(
                        user=user,
                        action="attribution_auto_badge",
                        description=f"Badge automatique '{template.name}' attribué à {user.username}"
                    )

                logger.info(f"[BADGE] ✅ {user.username} a débloqué : {template.name}")

            except Exception as e:
                logger.error(f"[BADGE] ❌ Erreur pour '{template.name}' → {user.username}: {e}")

    if log_events and not new_badges:
        logger.info(f"[BADGE] Aucun nouveau badge attribué à {user.username}")

    return new_badges if return_new_badges else None

def __create_badge(user, template: BadgeTemplate) -> Badge:
    """
    Crée et retourne un badge à partir d’un modèle.

    Args:
        user (User): Utilisateur cible
        template (BadgeTemplate): Modèle du badge

    Returns:
        Badge: Instance créée et enregistrée
    """
    return Badge.objects.create(
        user=user,
        name=template.name,
        icon=template.icon,
        description=template.description,
        level=template.level,
    )



================================================
FILE: Myevol_app/services/challenge_service.py
================================================
# Myevol_app/services/challenge_service.py

# services/challenge_service.py

import logging
from ..models import ChallengeProgress, Challenge, Notification
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def update_challenge_progress(progress_instance):
    """
    Met à jour la progression d'un utilisateur sur un défi.
    Cette méthode vérifie si un utilisateur a complété son défi, envoie des notifications,
    et enregistre l'état de complétion.

    Args:
        progress_instance (ChallengeProgress): Instance de progression du défi
    """
    # Vérifie si l'utilisateur a atteint son objectif
    challenge = progress_instance.challenge
    user = progress_instance.user

    if challenge.is_completed(user):
        progress_instance.completed = True
        progress_instance.completed_at = now()
        progress_instance.save()

        # Notifie l'utilisateur que le défi est terminé
        Notification.objects.create(
            user=user,
            message=f"🎯 Félicitations ! Vous avez complété le défi : {challenge.title}",
            notif_type="objectif"
        )

        logger.info(f"[CHALLENGE] {user.username} a complété le défi '{challenge.title}'")

def check_user_challenges(user):
    """
    Vérifie tous les défis actifs de l'utilisateur et met à jour sa progression.
    Cette fonction peut être appelée régulièrement pour vérifier l'état de tous les défis de l'utilisateur.

    Args:
        user (User): Utilisateur dont les défis doivent être vérifiés
    """
    today = now().date()

    # Récupère tous les défis actifs
    active_challenges = Challenge.objects.filter(start_date__lte=today, end_date__gte=today)

    for challenge in active_challenges:
        # Récupère ou crée une instance de progression pour chaque défi
        progress, created = ChallengeProgress.objects.get_or_create(user=user, challenge=challenge)

        # Si c'est une nouvelle progression, on vérifie si l'utilisateur a déjà atteint l'objectif
        if created:
            logger.info(f"[CHALLENGE] Progression créée pour {user.username} sur le défi '{challenge.title}'")
        else:
            logger.info(f"[CHALLENGE] Progression mise à jour pour {user.username} sur le défi '{challenge.title}'")

        # Met à jour la progression de l'utilisateur
        update_challenge_progress(progress)



================================================
FILE: Myevol_app/services/event_log_service.py
================================================
# services/event_log_service.py

from datetime import timedelta
import logging
from ..models import EventLog
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def log_event(action, description="", user=None, severity="INFO", **metadata):
    """
    Enregistre un événement dans le modèle EventLog. Cette méthode est utilisée pour tous les types d'événements.
    
    Args:
        action (str): Type d'action (ex : "connexion", "attribution_badge", etc.)
        description (str): Détails supplémentaires sur l'événement
        user (User, optional): Utilisateur concerné par l'événement
        severity (str): Niveau de gravité de l'événement ('INFO', 'WARN', 'ERROR', 'CRITICAL')
        **metadata (dict): Données supplémentaires liées à l'événement
    
    Returns:
        EventLog: Instance de l'événement créé
    """
    try:
        # Crée un log dans la base de données
        event = EventLog.objects.create(
            action=action,
            description=description,
            user=user,
            severity=severity,
            metadata=metadata or None
        )
        logger.info(f"[LOG] {user.username if user else 'System'} > {action} > {description} > Severity: {severity}")
        return event
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'événement {action} pour {user.username if user else 'System'}: {str(e)}")
        return None

def get_event_statistics(days=30, user=None):
    """
    Récupère des statistiques agrégées des événements sur une période donnée.
    
    Args:
        days (int): Nombre de jours à considérer depuis aujourd’hui
        user (User, optional): Filtrer par utilisateur
    
    Returns:
        dict: Statistiques des événements {action: count}
    """
    from django.db.models import Count
    
    # Filtre des événements pour les derniers 'days' jours
    since = now() - timedelta(days=days)
    events = EventLog.objects.filter(created_at__gte=since)
    
    # Si un utilisateur est spécifié, filtre par utilisateur
    if user:
        events = events.filter(user=user)

    return dict(events.values('action')
                .annotate(count=Count('id'))
                .values_list('action', 'count'))



================================================
FILE: Myevol_app/services/journal_service.py
================================================
# services/journal_service.py

from datetime import timedelta
from ..models import JournalEntry

def create_journal_entry(user, content, mood, category):
    """
    Crée une entrée de journal pour l'utilisateur.
    
    Args:
        user (User): L'utilisateur à qui l'entrée est associée
        content (str): Contenu de l'entrée
        mood (int): Note d'humeur
        category (str): Catégorie de l'entrée
    
    Returns:
        JournalEntry: L'entrée de journal nouvellement créée
    """
    entry = JournalEntry.objects.create(
        user=user,
        content=content,
        mood=mood,
        category=category
    )
    return entry

def get_journal_entries(user, start_date, end_date):
    """
    Récupère les entrées de journal dans une plage de dates.
    
    Args:
        user (User): L'utilisateur concerné
        start_date (date): Date de début
        end_date (date): Date de fin
    
    Returns:
        QuerySet: Ensemble des entrées de journal
    """
    return JournalEntry.get_entries_by_date_range(user, start_date, end_date)



================================================
FILE: Myevol_app/services/levels_services.py
================================================

#: Liste des seuils fixes correspondant aux 5 premiers niveaux de l'utilisateur.
#: Utilisée pour calculer la progression jusqu'au niveau 5.
#: Au-delà, la progression se fait par palier de 15 entrées par niveau.
LEVEL_THRESHOLDS = [1, 5, 10, 20, 35]

def get_user_level(entry_count: int) -> int:
    """
    Calcule le niveau d’un utilisateur en fonction du nombre d’entrées.
    Le niveau augmente selon un palier fixe puis par incrément après le niveau 5.
    """
    if entry_count < 1:
        return 0
    elif entry_count < 5:
        return 1
    elif entry_count < 10:
        return 2
    elif entry_count < 20:
        return 3
    elif entry_count < 35:
        return 4
    else:
        # Progression régulière tous les 15 journaux après le niveau 4
        return 5 + ((entry_count - 35) // 15)
LEVEL_THRESHOLDS = [1, 5, 10, 20, 35, 50, 75, 100, 150, 200]


def get_user_progress(entry_count: int) -> dict:
    """
    Retourne un dictionnaire contenant :
    - le niveau actuel,
    - la progression en pourcentage vers le niveau suivant,
    - le seuil du niveau suivant,
    - le nombre total d’entrées.
    """
    level = get_user_level(entry_count)

    # Liste des seuils fixes jusqu’au niveau 5
    thresholds = [1, 5, 10, 20, 35]

    # Définition des seuils actuel et suivant
    if level < 5:
        current_threshold = thresholds[level - 1] if level > 0 else 0
        next_threshold = thresholds[level]
    else:
        current_threshold = 35 + (level - 5) * 15
        next_threshold = current_threshold + 15

    # Calcul de la progression (0-100 %)
    if next_threshold > current_threshold:
        raw_progress = (entry_count - current_threshold) / (next_threshold - current_threshold)
        progress = min(100, max(0, int(raw_progress * 100)))
    else:
        progress = 100

    return {
        "level": level,
        "progress": progress,
        "next_threshold": next_threshold,
        "entries": entry_count,
    }


================================================
FILE: Myevol_app/services/notification_service.py
================================================
# services/notification_service.py

import logging
from django.utils.timezone import now
from ..models import Notification

logger = logging.getLogger(__name__)

def create_user_notification(user, message, notif_type="info", scheduled_at=None):
    """
    Service qui crée une notification pour un utilisateur.
    
    Args:
        user (User): L'utilisateur auquel la notification est destinée.
        message (str): Le message de la notification.
        notif_type (str): Le type de notification, ex. 'badge', 'objectif'.
        scheduled_at (datetime, optional): Date de programmation de la notification.
        
    Returns:
        Notification: Notification créée et stockée dans la base de données.
    """
    notification = Notification.objects.create(
        user=user,
        message=message,
        notif_type=notif_type,
        scheduled_at=scheduled_at
    )
    
    # Optionnel : Ajouter une logique de notification ici (comme des emails, web push, etc.)
    # par exemple : send_notification_to_user(user, message)

    return notification


def send_scheduled_notifications():
    """
    Service qui envoie les notifications programmées à la date actuelle.
    """
    notifications = Notification.objects.filter(scheduled_at__lte=now(), is_read=False, archived=False)
    
    for notification in notifications:
        # Logique d'envoi de notification (ex : via un service de messagerie, email, etc.)
        # send_notification(notification)
        
        # Marque comme lue la notification envoyée
        notification.mark_as_read()

        logger.info(f"Notification envoyée à {notification.user.username} : {notification.message}")


def archive_user_notifications(user):
    """
    Archive toutes les notifications d'un utilisateur.
    
    Args:
        user (User): L'utilisateur dont les notifications seront archivées.
        
    Returns:
        int: Nombre de notifications archivées.
    """
    notifications = Notification.objects.filter(user=user, archived=False)
    archived_count = notifications.update(archived=True)
    
    logger.info(f"{archived_count} notifications archivées pour {user.username}")
    return archived_count




================================================
FILE: Myevol_app/services/objective_service.py
================================================
# services/objective_service.py

import logging
from django.db import IntegrityError
from ..models.objective_model import Objective, Notification
from django.utils.timezone import now

logger = logging.getLogger(__name__)

class ObjectiveService:
    """
    Classe de service pour gérer la logique métier associée aux objectifs utilisateurs.
    """

    @staticmethod
    def create_objective(user, title, category, target_date, target_value):
        """
        Crée un nouvel objectif pour un utilisateur.
        
        Args:
            user (User): L'utilisateur qui crée l'objectif.
            title (str): Titre de l'objectif.
            category (str): Catégorie de l'objectif.
            target_date (date): La date cible pour accomplir l'objectif.
            target_value (int): La valeur à atteindre pour accomplir l'objectif.

        Returns:
            Objective: L'objectif créé.
        """
        try:
            objective = Objective.objects.create(
                user=user,
                title=title,
                category=category,
                target_date=target_date,
                target_value=target_value
            )
            logger.info(f"Objectif créé pour {user.username}: {title}")
            return objective
        except IntegrityError as e:
            logger.error(f"Erreur lors de la création de l'objectif pour {user.username}: {e}")
            raise

    @staticmethod
    def update_objective(objective, title=None, category=None, target_date=None, target_value=None):
        """
        Met à jour un objectif existant.

        Args:
            objective (Objective): L'objectif à mettre à jour.
            title (str, optional): Nouveau titre de l'objectif.
            category (str, optional): Nouvelle catégorie.
            target_date (date, optional): Nouvelle date cible.
            target_value (int, optional): Nouvelle valeur cible.
        
        Returns:
            Objective: L'objectif mis à jour.
        """
        if title:
            objective.title = title
        if category:
            objective.category = category
        if target_date:
            objective.target_date = target_date
        if target_value:
            objective.target_value = target_value
        
        objective.save(create_notification=False)  # Ne pas créer de notification lors de la mise à jour
        logger.info(f"Objectif mis à jour pour {objective.user.username}: {objective.title}")
        return objective

    @staticmethod
    def mark_as_complete(objective):
        """
        Marque un objectif comme complété et envoie une notification.

        Args:
            objective (Objective): L'objectif à marquer comme complété.
        
        Returns:
            Objective: L'objectif mis à jour.
        """
        if not objective.done:
            objective.done = True
            objective.save(create_notification=True)  # Crée une notification lors de la complétion
            logger.info(f"Objectif complété pour {objective.user.username}: {objective.title}")
        return objective

    @staticmethod
    def get_user_objectives(user):
        """
        Récupère tous les objectifs d'un utilisateur.

        Args:
            user (User): L'utilisateur concerné.
        
        Returns:
            QuerySet: Ensemble des objectifs de l'utilisateur.
        """
        return Objective.objects.filter(user=user).order_by('target_date')

    @staticmethod
    def get_statistics(user):
        """
        Calcule des statistiques globales pour les objectifs d'un utilisateur.

        Args:
            user (User): L'utilisateur concerné.

        Returns:
            dict: Statistiques des objectifs de l'utilisateur.
        """
        objectives = Objective.objects.filter(user=user)
        total = objectives.count()
        completed = objectives.filter(done=True).count()
        overdue = objectives.filter(done=False, target_date__lt=now().date()).count()

        completion_rate = (completed / total * 100) if total > 0 else 0

        logger.info(f"Statistiques des objectifs pour {user.username}: Total: {total}, Complétés: {completed}, Taux de complétion: {completion_rate}%")
        return {
            'total': total,
            'completed': completed,
            'completion_rate': round(completion_rate, 1),
            'overdue': overdue
        }



================================================
FILE: Myevol_app/services/quote_service.py
================================================
# services/quote_service.py

from datetime import timedelta
import hashlib
import random
from django.utils.timezone import now

from ..models.quote_model import Quote

def get_random_quote(mood_tag=None):
    """
    Retourne une citation aléatoire, optionnellement filtrée par mood_tag.
    
    Args:
        mood_tag (str, optional): Étiquette d'humeur pour filtrer les citations
        
    Returns:
        Quote: Une citation aléatoire ou None si aucune ne correspond
    """
    queryset = Quote.objects.all()
    if mood_tag:
        queryset = queryset.filter(mood_tag=mood_tag)
        
    count = queryset.count()
    if count == 0:
        return None
        
    random_index = random.randint(0, count - 1)
    return queryset[random_index]

def get_daily_quote(user=None):
    """
    Retourne la citation du jour, potentiellement personnalisée selon l'utilisateur.
    
    Args:
        user (User, optional): Utilisateur pour personnalisation basée sur son humeur
        
    Returns:
        Quote: Citation du jour
    """
    today = now().date().strftime("%Y%m%d")

    mood_filter = None
    if user:
        # Logique pour personnaliser la citation selon l'humeur de l'utilisateur
        from django.db.models import Avg
        recent_entries = user.entries.filter(created_at__gte=now() - timedelta(days=3))
        if recent_entries.exists():
            avg_mood = recent_entries.aggregate(avg=Avg('mood'))['avg']
            if avg_mood is not None:
                if avg_mood < 4:
                    mood_filter = 'low'
                elif avg_mood > 7:
                    mood_filter = 'positive'
                else:
                    mood_filter = 'neutral'
    
    quotes = Quote.objects.all()
    if mood_filter:
        quotes = quotes.filter(mood_tag=mood_filter)
        
    count = quotes.count()
    if count == 0:
        return None
    
    # Sélection déterministe de la citation du jour
    hash_obj = hashlib.md5(today.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    index = hash_int % count
    
    return quotes[index]



================================================
FILE: Myevol_app/services/stats_service.py
================================================
# services/stats_service.py

import logging
from collections import defaultdict
from datetime import timedelta
from django.db.models import Avg
from django.utils.timezone import now
from ..models.stats_model import WeeklyStat, MonthlyStat, AnnualStat, DailyStat

# Initialisation du logger
logger = logging.getLogger(__name__)

def generate_weekly_stats(user, reference_date=None):
    """
    Génère ou met à jour les statistiques hebdomadaires pour un utilisateur.
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

    stat, created = WeeklyStat.objects.update_or_create(
        user=user,
        week_start=week_start,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"Création des statistiques hebdomadaires pour {user.username} - Semaine du {week_start}")
    else:
        logger.info(f"Mise à jour des statistiques hebdomadaires pour {user.username} - Semaine du {week_start}")
    
    return stat

def generate_daily_stats(user, date=None):
    """
    Génère ou met à jour les statistiques journalières pour un utilisateur.
    """
    if not date:
        date = now().date()

    entries = user.entries.filter(created_at__date=date)
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = DailyStat.objects.update_or_create(
        user=user,
        date=date,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"Création des statistiques journalières pour {user.username} - {date}")
    else:
        logger.info(f"Mise à jour des statistiques journalières pour {user.username} - {date}")
    
    return stat

def generate_monthly_stats(user, reference_date=None):
    """
    Génère ou met à jour les statistiques mensuelles pour un utilisateur.
    """
    if not reference_date:
        reference_date = now().date()

    month_start = reference_date.replace(day=1)
    next_month = (month_start + timedelta(days=32)).replace(day=1)
    month_end = next_month - timedelta(days=1)

    entries = user.entries.filter(created_at__date__range=(month_start, month_end))
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = MonthlyStat.objects.update_or_create(
        user=user,
        month_start=month_start,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"Création des statistiques mensuelles pour {user.username} - Mois de {month_start.strftime('%B %Y')}")
    else:
        logger.info(f"Mise à jour des statistiques mensuelles pour {user.username} - Mois de {month_start.strftime('%B %Y')}")
    
    return stat

def generate_annual_stats(user, reference_date=None):
    """
    Génère ou met à jour les statistiques annuelles pour un utilisateur.
    """
    if not reference_date:
        reference_date = now().date()

    year_start = reference_date.replace(month=1, day=1)
    year_end = year_start.replace(month=12, day=31)

    entries = user.entries.filter(created_at__date__range=(year_start, year_end))
    entries_count = entries.count()
    mood_avg = entries.aggregate(avg=Avg("mood"))["avg"]
    mood_avg = round(mood_avg, 1) if mood_avg is not None else None

    categories = defaultdict(int)
    for entry in entries:
        categories[entry.category] += 1

    stat, created = AnnualStat.objects.update_or_create(
        user=user,
        year_start=year_start,
        defaults={
            "entries_count": entries_count,
            "mood_average": mood_avg,
            "categories": dict(categories),
        }
    )

    if created:
        logger.info(f"Création des statistiques annuelles pour {user.username} - Année {year_start.year}")
    else:
        logger.info(f"Mise à jour des statistiques annuelles pour {user.username} - Année {year_start.year}")
    
    return stat



================================================
FILE: Myevol_app/services/streak_service.py
================================================
# services/streak_service.py

def update_user_streak(user):
    current = user.current_streak()
    if current > user.longest_streak:
        user.longest_streak = current
        user.save(update_fields=['longest_streak'])



================================================
FILE: Myevol_app/services/user_service.py
================================================
# services/user_service.py

from ..models.userPreference_model import UserPreference
from ..models.user_model import User
from .badge_service import update_user_badges
from .streak_service import update_user_streak
from .userpreference_service import create_preferences_for_user
import logging

logger = logging.getLogger(__name__)

def handle_user_badges(user):
    """
    Met à jour les badges pour l'utilisateur.
    """
    try:
        update_user_badges(user)
        logger.info(f"Badges mis à jour pour {user.username}.")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des badges pour {user.username}: {e}")

def handle_user_streak(user):
    """
    Met à jour les streaks de l'utilisateur.
    """
    try:
        update_user_streak(user)
        logger.info(f"Streaks mis à jour pour {user.username}.")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des streaks pour {user.username}: {e}")

def handle_user_preferences(user):
    """
    Crée les préférences par défaut pour l'utilisateur si elles n'existent pas.
    """
    try:
        create_preferences_for_user(user)
        logger.info(f"Préférences par défaut créées pour {user.username}.")
    except Exception as e:
        logger.error(f"Erreur lors de la création des préférences pour {user.username}: {e}")



================================================
FILE: Myevol_app/services/user_stats_service.py
================================================
# services/user_stats_service.py

from datetime import timedelta
from django.db import models
from django.db.models import Avg, Count
from django.utils.timezone import now
from django.db.models.functions import TruncDate

def compute_mood_average(entries, days=7, reference_date=None):
    """
    Calcule la moyenne d'humeur sur les X derniers jours.

    Args:
        entries: Les entrées de journal de l'utilisateur
        days (int): Nombre de jours à considérer
        reference_date (date): Date de référence

    Returns:
        float: Moyenne d'humeur arrondie à 1 décimale
    """
    if reference_date is None:
        reference_date = now()
        
    entries = entries.filter(created_at__gte=reference_date - timedelta(days=days))
    avg = entries.aggregate(avg=Avg('mood'))['avg']
    return round(avg, 1) if avg is not None else None

def compute_current_streak(entries, reference_date=None):
    """
    Calcule la série actuelle de jours consécutifs avec au moins une entrée.
    
    Args:
        entries: Les entrées de journal de l'utilisateur
        reference_date (date): Date de référence

    Returns:
        int: Nombre de jours consécutifs avec une entrée
    """
    if reference_date is None:
        reference_date = now().date()

    streak = 0
    for i in range(0, 365):
        day = reference_date - timedelta(days=i)
        if entries.filter(created_at__date=day).exists():
            streak += 1
        else:
            break
    return streak

def compute_entries_per_category(entries, days=None):
    """
    Calcule la distribution des entrées par catégorie.

    Args:
        entries: Les entrées de journal de l'utilisateur
        days (int, optional): Limite aux N derniers jours si spécifié

    Returns:
        dict: Dictionnaire avec catégories comme clés et nombre d'entrées comme valeurs
    """
    if days:
        entries = entries.filter(created_at__gte=now() - timedelta(days=days))
    
    return dict(entries.values('category').annotate(count=Count('id')).values_list('category', 'count'))



================================================
FILE: Myevol_app/services/userpreference_service.py
================================================
# services/userPreference_service.py
import logging
from django.shortcuts import get_object_or_404
from ..models.userPreference_model import UserPreference

logger = logging.getLogger(__name__)

def create_or_update_preferences(user, preferences_data=None):
    """
    Crée ou met à jour les préférences de l'utilisateur.
    
    Args:
        user: L'utilisateur pour lequel les préférences doivent être créées ou mises à jour.
        preferences_data: Données de préférences (optionnel, si fourni, cela écrase les préférences existantes).
        
    Returns:
        UserPreference: L'instance mise à jour ou créée des préférences.
        
    Cette fonction interagit directement avec le modèle `UserPreference` pour :
    - Créer ou récupérer les préférences existantes.
    - Mettre à jour les préférences avec de nouvelles valeurs.
    - Enregistrer les changements dans la base de données.
    """
    prefs, created = UserPreference.objects.get_or_create(user=user)
    logger.info(f"{'Création' if created else 'Mise à jour'} des préférences pour l'utilisateur {user.username}.")
    
    if preferences_data:
        # Valider et mettre à jour les préférences
        for key, value in preferences_data.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
            else:
                logger.warning(f"Clé '{key}' non valide pour les préférences de {user.username}.")
        
        prefs.save()
        logger.info(f"Préférences mises à jour pour l'utilisateur {user.username}.")
    else:
        logger.info(f"Aucune mise à jour des préférences pour {user.username}.")

    return prefs


def reset_preferences_to_defaults(user):
    """
    Réinitialise les préférences aux valeurs par défaut pour un utilisateur donné.
    
    Args:
        user: L'utilisateur pour lequel les préférences doivent être réinitialisées.
        
    Returns:
        UserPreference: L'instance réinitialisée des préférences.
        
    Cette fonction utilise la méthode `reset_to_defaults` du modèle `UserPreference` 
    pour réinitialiser les préférences aux valeurs par défaut.
    """
    prefs = get_object_or_404(UserPreference, user=user)
    prefs.reset_to_defaults()
    logger.info(f"Préférences réinitialisées aux valeurs par défaut pour l'utilisateur {user.username}.")
    return prefs



================================================
FILE: Myevol_app/signals/badge_signals.py
================================================
# signals/badge_signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from ..services.notification_service import create_user_notification
from ..models import Badge, JournalEntry, Notification, DailyStat, UserPreference, User
from ..services.badge_service import update_user_badges
from ..services.challenge_service import check_user_challenges

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def check_badges_and_stats(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque création d’entrée de journal :
    - Met à jour les stats journalières
    - Vérifie les badges débloqués
    - Vérifie les défis en cours
    """
    user = instance.user
    date = instance.created_at.date()

    # 🔁 Mise à jour ou création des statistiques du jour
    DailyStat.generate_for_user(user=user, date=date)

    # ❌ Ne continue pas si ce n’est pas une nouvelle entrée
    if not created:
        return

    total = user.entries.count()

    # Vérifie les badges via le service
    try:
        new_badges = update_user_badges(user, log_events=True, return_new_badges=True)

        if new_badges:
            # Envoi d'une notification pour chaque nouveau badge débloqué
            for badge in new_badges:
                Notification.objects.create(
                    user=user,
                    message=f"🏅 Félicitations ! Tu as débloqué le badge : {badge.name}",
                    notif_type="badge"
                )
                logger.info(f"[BADGE] {user.username} a débloqué le badge '{badge.name}' (ID: {badge.id})")

    except Exception as e:
        logger.error(f"[BADGE] Erreur lors de la vérification des badges pour {user.username}: {e}")

    # Vérifie les défis en cours (centralisé)
    try:
        check_user_challenges(user)
    except Exception as e:
        logger.error(f"[CHALLENGE] Erreur lors de la vérification des défis pour {user.username}: {e}")

@receiver(post_delete, sender=JournalEntry)
def update_stats_on_delete(sender, instance, **kwargs):
    """
    Recalcule ou supprime les statistiques journalières après suppression d’une entrée.
    """
    user = instance.user
    date = instance.created_at.date()

    remaining_entries = user.entries.filter(created_at__date=date)

    if remaining_entries.exists():
        # Si des entrées restent pour cette date, recalculer les stats
        DailyStat.generate_for_user(user=user, date=date)
    else:
        # Si plus d'entrées, supprimer les stats de cette date
        DailyStat.objects.filter(user=user, date=date).delete()
        logger.info(f"[STATS] Statistiques supprimées pour {user.username} - {date}")

@receiver(post_save, sender=Badge)
def notify_user_of_new_badge(sender, instance, created, **kwargs):
    """
    Signal qui est déclenché lors de la création d'un badge.
    Crée une notification pour informer l'utilisateur de l'attribution du badge.
    """
    if created:
        try:
            # Créer une notification pour l'utilisateur à propos du badge
            create_user_notification(
                user=instance.user,
                message=f"🏅 Nouveau badge débloqué : {instance.name}",
                notif_type="badge"
            )
            logger.info(f"[NOTIFICATION] Notification envoyée à {instance.user.username} pour le badge '{instance.name}' (ID: {instance.id})")

        except Exception as e:
            logger.error(f"[NOTIFICATION] Erreur lors de la création de la notification pour {instance.user.username}: {e}")



================================================
FILE: Myevol_app/signals/challenge_signals.py
================================================
# signals/challenge_signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from ..models import Challenge, ChallengeProgress, Notification
from ..services.challenge_service import update_challenge_progress
from ..services.badge_service import update_user_badges

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Challenge)
def log_challenge_creation(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque fois qu'un défi est créé.
    Enregistre un log pour l'événement de création et envoie une notification.
    """
    if created:
        logger.info(f"Défi créé : {instance.title} (ID: {instance.id})")
        # Envoi de notification à l'utilisateur ou à un groupe
        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Nouveau défi créé : {instance.title}",
            notif_type="defi"
        )

@receiver(post_save, sender=ChallengeProgress)
def update_progress(sender, instance, created, **kwargs):
    """
    Signal déclenché à chaque fois que la progression d'un utilisateur sur un défi est mise à jour.
    Appelle la méthode de mise à jour de la progression et vérifie si l'utilisateur a complété le défi.
    """
    if created:
        logger.info(f"Progression ajoutée pour l'utilisateur {instance.user.username} sur le défi {instance.challenge.title}")
        # On vérifie la progression de l'utilisateur sur ce défi
        update_challenge_progress(instance)
        
        # Vérification des badges et mise à jour si nécessaire
        update_user_badges(instance.user)

@receiver(post_delete, sender=ChallengeProgress)
def remove_progress(sender, instance, **kwargs):
    """
    Signal déclenché lors de la suppression d'une progression de défi.
    Met à jour les statistiques et enregistre un log de l'événement.
    """
    logger.info(f"Progression supprimée pour l'utilisateur {instance.user.username} sur le défi {instance.challenge.title}")
    
    # Mettre à jour les statistiques après suppression
    # Vous pouvez ajouter une logique pour recalculer les statistiques des utilisateurs ici, si nécessaire.
    # Exemple : DailyStat.update_user_stats(instance.user)

@receiver(post_save, sender=Challenge)
def check_challenge_end(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsque la date de fin d'un défi est atteinte.
    Ce signal peut être utilisé pour effectuer des actions comme attribuer des badges,
    envoyer une notification à l'utilisateur ou effectuer des calculs statistiques.
    """
    today = now().date()
    if not created and instance.end_date == today:
        logger.info(f"Le défi '{instance.title}' a pris fin aujourd'hui.")
        
        # Exemple : Attribuer un badge ou envoyer une notification à l'utilisateur
        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Le défi '{instance.title}' est terminé. Félicitations !",
            notif_type="defi_achèvement"
        )

        # Vous pouvez ajouter un service pour gérer la logique de fin de défi (par exemple, attribuer des badges)
        # update_user_badges(instance.user)



================================================
FILE: Myevol_app/signals/event_log_signals.py
================================================
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..services.event_log_service import log_event

from ..models.challenge_model import ChallengeProgress
from ..models import EventLog, Challenge, Badge, JournalEntry, User

logger = logging.getLogger(__name__)

# Signal de création d'un badge
@receiver(post_save, sender=Badge)
def log_badge_creation(sender, instance, created, **kwargs):
    """
    Enregistre un événement chaque fois qu'un badge est attribué à un utilisateur.
    """
    if created:
        log_event(
            action="attribution_badge",
            description=f"Badge {instance.name} attribué à {instance.user.username}",
            user=instance.user,
            severity="INFO",
            metadata={"badge_name": instance.name, "level": instance.level}
        )

# Signal de création d'une entrée de journal
@receiver(post_save, sender=JournalEntry)
def log_journal_entry(sender, instance, created, **kwargs):
    """
    Enregistre un événement chaque fois qu'une entrée de journal est ajoutée.
    """
    if created:
        log_event(
            action="ajout_entrée_journal",
            description=f"Nouvelle entrée de journal ajoutée par {instance.user.username}",
            user=instance.user,
            severity="INFO",
            metadata={"journal_entry_id": instance.id}
        )

# Signal de création ou mise à jour de la progression du défi
@receiver(post_save, sender=Challenge)
def log_challenge_creation(sender, instance, created, **kwargs):
    """
    Enregistre un événement chaque fois qu'un défi est créé.
    """
    if created:
        log_event(
            action="création_défi",
            description=f"Nouveau défi créé : {instance.title}",
            severity="INFO",
            metadata={"challenge_id": instance.id}
        )

# Signal de suppression de la progression du défi
@receiver(post_delete, sender=ChallengeProgress)
def log_challenge_progress_removal(sender, instance, **kwargs):
    """
    Enregistre un événement chaque fois qu'une progression de défi est supprimée.
    """
    log_event(
        action="suppression_progression_défi",
        description=f"Progression du défi {instance.challenge.title} supprimée pour {instance.user.username}",
        user=instance.user,
        severity="WARN",
        metadata={"challenge_id": instance.challenge.id}
    )



================================================
FILE: Myevol_app/signals/journal_signals.py
================================================
# signals/journal_signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from ..models import JournalEntry, DailyStat, Notification, JournalMedia
from ..services.challenge_service import check_challenges
from ..services.badge_service import update_user_badges

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def handle_journal_entry_created(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une entrée de journal est créée.
    Met à jour les statistiques journalières, vérifie les défis en cours,
    et met à jour les badges de l'utilisateur.
    """
    if created:
        logger.info(f"Nouvelle entrée de journal créée pour {instance.user.username} le {instance.created_at.date()}")
        
        # ➕ Mise à jour des statistiques journalières
        DailyStat.generate_for_user(instance.user, instance.created_at.date())
        
        # ✅ Vérification des défis
        check_challenges(instance.user)
        
        # 🏅 Mise à jour des badges de l'utilisateur
        update_user_badges(instance.user)

        # 🔥 Mise à jour des streaks de l'utilisateur
        instance.user.update_streaks()

        # 🔔 Envoi d'une notification de création
        Notification.objects.create(
            user=instance.user,
            message=f"Votre nouvelle entrée du {instance.created_at.date()} a été enregistrée.",
            notif_type="journal_created"
        )


@receiver(post_save, sender=JournalEntry)
def handle_journal_entry_updated(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une entrée de journal est mise à jour.
    Envoie une notification à l'utilisateur pour l'informer de la mise à jour.
    """
    if not created:
        # On envoie une notification seulement si l'entrée est mise à jour
        logger.info(f"Entrée de journal mise à jour pour {instance.user.username} le {instance.updated_at.date()}")
        
        Notification.objects.create(
            user=instance.user,
            message=f"Votre entrée de journal du {instance.created_at.date()} a été mise à jour.",
            notif_type="journal_update"
        )


@receiver(post_delete, sender=JournalEntry)
def handle_media_cleanup(sender, instance, **kwargs):
    """
    Supprime les médias associés à l'entrée de journal lorsqu'elle est supprimée.
    """
    logger.info(f"Suppression des médias associés à l'entrée de journal pour {instance.user.username}")
    
    # Supprimer les fichiers multimédia associés à cette entrée
    for media in instance.media.all():
        logger.info(f"Suppression du fichier média {media.file.url} associé à l'entrée {instance.id}")
        media.file.delete(save=False)  # Suppression du fichier
        media.delete()  # Suppression de l'objet media

    logger.info(f"Médias supprimés pour l'entrée de journal {instance.id}")

    # 🔔 Envoi d'une notification pour informer l'utilisateur de la suppression
    Notification.objects.create(
        user=instance.user,
        message=f"L'entrée de journal du {instance.created_at.date()} a été supprimée avec succès.",
        notif_type="journal_deleted"
    )




================================================
FILE: Myevol_app/signals/objective_signals.py
================================================
# signals/objective_signals.py

import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from ..models.objective_model import Objective
from ..models.notification_model import Notification
from django.utils.timezone import now

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Objective)
def handle_objective_creation(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de la création d'un objectif.
    Envoie une notification si l'objectif est marqué comme complété.
    """
    if created:
        logger.info(f"Création d'un nouvel objectif pour {instance.user.username}: {instance.title}")
    
    if instance.done:
        # Si l'objectif est marqué comme fait lors de la création
        Notification.objects.create(
            user=instance.user,
            message=f"🎯 Objectif atteint : {instance.title}",
            notif_type="objectif"
        )
        logger.info(f"Objectif complété : {instance.title} pour {instance.user.username}")


@receiver(post_save, sender=Objective)
def handle_objective_update(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de la mise à jour d'un objectif.
    Si l'objectif est marqué comme complété, envoie une notification.
    """
    if not created:
        if instance.done:
            Notification.objects.create(
                user=instance.user,
                message=f"🎯 Objectif atteint : {instance.title}",
                notif_type="objectif"
            )
            logger.info(f"Objectif mis à jour comme complété : {instance.title} pour {instance.user.username}")


@receiver(pre_delete, sender=Objective)
def handle_objective_delete(sender, instance, **kwargs):
    """
    Signal déclenché avant la suppression d'un objectif.
    Log de la suppression.
    """
    logger.info(f"Suppression de l'objectif {instance.title} pour {instance.user.username}")



================================================
FILE: Myevol_app/signals/quote_signals.py
================================================

# signals/quote_signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models.quote_model import Quote
from ..services.notification_service import create_user_notification

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Quote)
def notify_user_of_new_quote(sender, instance, created, **kwargs):
    """
    Signal déclenché lorsqu'une nouvelle citation est créée.
    Crée une notification pour informer l'utilisateur de la nouvelle citation.
    """
    if created:
        logger.info(f"Nouvelle citation créée : '{instance.text}'")
        
        # Crée une notification pour chaque nouvelle citation (par exemple, pour l'administrateur)
        create_user_notification(
            user=instance.user,  # Vous pouvez définir un utilisateur ou un admin pour recevoir la notification
            message=f"Une nouvelle citation a été ajoutée : {instance.text}",
            notif_type="info"
        )



================================================
FILE: Myevol_app/signals/stats_signals.py
================================================
# signals/stats_signals.py

from django.db.models.signals import post_save, post_delete
import logging
from django.dispatch import receiver
from ..models.stats_model import WeeklyStat, DailyStat, MonthlyStat, AnnualStat, JournalEntry
from ..services.stats_service import generate_weekly_stats, generate_daily_stats, generate_monthly_stats, generate_annual_stats

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JournalEntry)
def update_statistics(sender, instance, created, **kwargs):
    """
    Signal déclenché lors de la création d'une entrée de journal.
    Met à jour les statistiques hebdomadaires, journalières, mensuelles et annuelles de l'utilisateur.
    """
    if created:
        # Mise à jour des statistiques pour chaque entrée de journal
        generate_weekly_stats(instance.user)
        generate_daily_stats(instance.user)
        generate_monthly_stats(instance.user)
        generate_annual_stats(instance.user)

@receiver(post_save, sender=WeeklyStat)
def log_weekly_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques hebdomadaires.
    """
    if created:
        logger.info(f"Statistiques hebdomadaires créées pour {instance.user.username} - Semaine du {instance.week_start}")

@receiver(post_delete, sender=WeeklyStat)
def log_weekly_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques hebdomadaires.
    """
    logger.info(f"Statistiques hebdomadaires supprimées pour {instance.user.username} - Semaine du {instance.week_start}")

@receiver(post_save, sender=DailyStat)
def log_daily_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques journalières.
    """
    if created:
        logger.info(f"Statistiques journalières créées pour {instance.user.username} - {instance.date}")

@receiver(post_delete, sender=DailyStat)
def log_daily_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques journalières.
    """
    logger.info(f"Statistiques journalières supprimées pour {instance.user.username} - {instance.date}")

@receiver(post_save, sender=MonthlyStat)
def log_monthly_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques mensuelles.
    """
    if created:
        logger.info(f"Statistiques mensuelles créées pour {instance.user.username} - Mois de {instance.month_start.strftime('%B %Y')}")

@receiver(post_delete, sender=MonthlyStat)
def log_monthly_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques mensuelles.
    """
    logger.info(f"Statistiques mensuelles supprimées pour {instance.user.username} - Mois de {instance.month_start.strftime('%B %Y')}")

@receiver(post_save, sender=AnnualStat)
def log_annual_stat_creation(sender, instance, created, **kwargs):
    """
    Log l'événement de création de statistiques annuelles.
    """
    if created:
        logger.info(f"Statistiques annuelles créées pour {instance.user.username} - Année {instance.year_start.year}")

@receiver(post_delete, sender=AnnualStat)
def log_annual_stat_deletion(sender, instance, **kwargs):
    """
    Log l'événement de suppression de statistiques annuelles.
    """
    logger.info(f"Statistiques annuelles supprimées pour {instance.user.username} - Année {instance.year_start.year}")



================================================
FILE: Myevol_app/signals/user_signals.py
================================================
# signals/user_signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from ..models.user_model import User
from ..services.user_service import handle_user_badges, handle_user_streak, handle_user_preferences

# Initialisation du logger pour la gestion des logs
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def handle_user_creation(sender, instance, created, **kwargs):
    """
    Signal appelé après la création d'un utilisateur pour :
    - Créer ses préférences par défaut
    - Mettre à jour ses badges
    - Mettre à jour sa série d'entrées consécutives (streak)
    
    Ce signal est déclenché uniquement lors de la création d'un nouvel utilisateur.
    """

    # Vérifie si l'utilisateur vient d'être créé
    if created:
        # Crée les préférences utilisateur par défaut
        handle_user_preferences(instance)

        # Met à jour les badges de l'utilisateur
        handle_user_badges(instance)

        # Met à jour la série d'entrées consécutives de l'utilisateur
        handle_user_streak(instance)

        # Ajout d'une entrée de log pour indiquer que l'initialisation a été effectuée avec succès
        logger.info(f"Utilisateur {instance.username} créé. Initialisation des préférences, badges et streaks.")



================================================
FILE: Myevol_app/signals/userpreference_signals.py
================================================
# signals/userPreference_signals.py

import logging
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from ..models.userPreference_model import UserPreference
from ..services.userpreference_service import create_or_update_preferences

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserPreference)
def handle_user_preference_update(sender, instance, created, **kwargs):
    """
    Signal qui gère la mise à jour des préférences après la création ou la modification d'un objet UserPreference.
    
    Args:
        sender: Le modèle ayant envoyé le signal (UserPreference).
        instance: L'instance de l'objet UserPreference créé ou mis à jour.
        created: Boolean indiquant si l'instance est nouvellement créée.
        **kwargs: Autres arguments du signal.
    """
    if created:
        logger.info(f"Préférences créées pour l'utilisateur {instance.user.username}")
    else:
        logger.info(f"Préférences mises à jour pour l'utilisateur {instance.user.username}")
    
    # Action supplémentaire après la création ou mise à jour (par exemple, notifications)
    try:
        instance.user.update_badges()
    except ValidationError as e:
        logger.error(f"Erreur lors de la mise à jour des badges pour {instance.user.username}: {e}")

@receiver(post_save, sender=UserPreference)
def create_default_preferences(sender, instance, created, **kwargs):
    """
    Crée les préférences par défaut pour l'utilisateur si elles n'ont pas été créées automatiquement.
    """
    if created:
        logger.info(f"Préférences créées pour l'utilisateur {instance.user.username}")
        instance.create_default_preferences()
    else:
        logger.info(f"Préférences mises à jour pour l'utilisateur {instance.user.username}")


@receiver(pre_save, sender=UserPreference)
def validate_preferences(sender, instance, **kwargs):
    """
    Valider les préférences avant leur enregistrement.
    """
    if len(instance.accent_color) > 7:
        logger.warning(f"Couleur accent trop longue pour {instance.user.username}, modification nécessaire.")
        instance.accent_color = instance.accent_color[:7]  # Couper à la longueur correcte
    if instance.xp < 0:
        raise ValidationError("XP ne peut pas être négatif.")
    logger.info(f"Préférences validées avant l'enregistrement pour {instance.user.username}.")

def send_preference_update_notification(user):
    """
    Envoie une notification par email à l'utilisateur lorsque ses préférences sont modifiées.
    """
    subject = "Mise à jour de vos préférences"
    message = f"Bonjour {user.username},\n\nVos préférences d'application ont été mises à jour avec succès.\n\nCordialement,\nL'équipe de MyEvol."
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, message, from_email, [user.email])
        logger.info(f"Email de notification envoyé à {user.email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email de notification à {user.email}: {e}")

@receiver(post_save, sender=UserPreference)
def send_notification_on_preference_change(sender, instance, created, **kwargs):
    """
    Envoie une notification à l'utilisateur lorsque ses préférences sont mises à jour.
    """
    if not created:
        # Exemple d'envoi d'email de notification sur mise à jour des préférences
        logger.info(f"Envoi de notification à {instance.user.username} après mise à jour des préférences.")
        # L'appel à la méthode de notification (ex: email ou enregistrement dans une file d'attente de notification)
        send_preference_update_notification(instance.user)

@receiver(post_save, sender=UserPreference)
def log_preferences_change(sender, instance, created, **kwargs):
    """
    Log les modifications des préférences d'un utilisateur pour un suivi.
    """
    if not created:
        logger.info(f"Changement de préférence pour l'utilisateur {instance.user.username}.")
        logger.info(f"Paramètre changé: {instance.accent_color}, Mode sombre: {instance.dark_mode}.")



