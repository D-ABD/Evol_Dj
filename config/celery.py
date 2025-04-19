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
