from __future__ import absolute_import, unicode_literals

# Initialise celery à l’import du projet
from .celery import app as celery_app

__all__ = ("celery_app",)
