from django.apps import AppConfig

class MyevolAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Myevol_app'

    def ready(self):
        import Myevol_app.signals.event_log_signals
