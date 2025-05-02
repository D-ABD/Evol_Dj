import os
import socket
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
from celery.schedules import crontab

# Load environment variables
load_dotenv()

# === BASE PATH ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === SÉCURITÉ ===
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-default')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# === APPS ===
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App locale
    'Myevol_app',

    # Tiers
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'django_extensions',
    'corsheaders',
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === CORS ===
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'
CORS_ALLOW_CREDENTIALS = True

# === URL / WSGI ===
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# === TEMPLATES ===
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

# === DATABASE ===
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

# === AUTHENTIFICATION ===
AUTH_USER_MODEL = 'Myevol_app.User'

LOGIN_URL = 'myevol:login'
LOGIN_REDIRECT_URL = 'myevol:dashboard'
LOGOUT_REDIRECT_URL = 'myevol:login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === INTERNATIONALISATION ===
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# === STATIC FILES ===
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === DRF ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'Myevol_app.paginations.MyEvolPagination',
    'PAGE_SIZE': 10,
}

# === SIMPLE JWT ===
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 1))),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# === DJANGO SPECTACULAR ===
SPECTACULAR_SETTINGS = {
    'TITLE': 'MyEvol API',
    'DESCRIPTION': "Documentation complète de l'API MyEvol pour l'application mobile et web.",
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'CONTACT': {'name': 'Équipe MyEvol', 'email': 'support@myevol.app'},
    'LICENSE': {'name': 'Propriétaire'},
    'TAGS': [
        {'name': 'Journal', 'description': 'Entrées de journal'},
        {'name': 'Objectifs', 'description': 'Objectifs personnels'},
        {'name': 'Badges', 'description': 'Système de progression'},
        {'name': 'Statistiques', 'description': 'Analyses et tendances'},
        {'name': 'Utilisateurs', 'description': 'Comptes et préférences'},
        {'name': 'Notifications', 'description': 'Alertes et rappels'},
        {'name': 'Challenges', 'description': 'Défis et compétitions'},
    ],
}

# === CELERY ===
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'ask_user_daily_activity': {
        'task': 'Myevol_app.tasks.ask_user_daily_activity',
        'schedule': crontab(hour=19, minute=0),
    },
    'generate_daily_stats': {
        'task': 'Myevol_app.tasks.generate_all_daily_stats',
        'schedule': crontab(hour=0, minute=0),
    },
    'generate_weekly_stats': {
        'task': 'Myevol_app.tasks.generate_all_weekly_stats',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
    'generate_monthly_stats': {
        'task': 'Myevol_app.tasks.generate_all_monthly_stats',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),
    },
    'generate_annual_stats': {
        'task': 'Myevol_app.tasks.generate_all_annual_stats',
        'schedule': crontab(hour=9, minute=0, day_of_month=1, month_of_year=1),
    },
    'clean_old_notifications': {
        'task': 'Myevol_app.tasks.clean_old_notifications',
        'schedule': crontab(hour=3, minute=0),
    },
    'update_user_streaks': {
        'task': 'Myevol_app.tasks.recalculate_all_streaks',
        'schedule': crontab(hour=0, minute=30),
    },
    'remind_inactive_users': {
        'task': 'Myevol_app.tasks.remind_inactive_users',
        'schedule': crontab(hour=18, minute=0),
    },
}

# === EMAIL ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# === LOGGING ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# === UI / Alerts ===
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# === ADMIN ===
DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@monapp.com')
