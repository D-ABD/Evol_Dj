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
