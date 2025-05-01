import factory
from django.utils import timezone
from django.contrib.auth import get_user_model

from Myevol_app.models.badge_model import Badge, BadgeTemplate
from Myevol_app.models.journal_model import JournalEntry
from Myevol_app.models.notification_model import Notification
from Myevol_app.models.objective_model import Objective
from Myevol_app.models.challenge_model import Challenge, ChallengeProgress
from Myevol_app.models.quote_model import Quote
from Myevol_app.models.userPreference_model import UserPreference
from Myevol_app.models.event_log_model import EventLog
from Myevol_app.models.stats_model import DailyStat, WeeklyStat, MonthlyStat, AnnualStat

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class BadgeTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BadgeTemplate

    name = factory.Sequence(lambda n: f"BadgeTemplate {n}")
    description = "Un badge test généré automatiquement."


class BadgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Badge

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Badge {n}")
    description = "Badge de test"


class JournalEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JournalEntry

    user = factory.SubFactory(UserFactory)
    content = "Contenu test"
    mood = 3
    category = "Travail"
    created_at = factory.LazyFunction(timezone.now)


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UserFactory)
    message = factory.Sequence(lambda n: f"Notification {n}")
    notif_type = "badge"
    is_read = False
    archived = False
    created_at = factory.LazyFunction(timezone.now)


class ObjectiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Objective

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f"Objectif {n}")
    category = "Santé"
    target_date = factory.LazyFunction(lambda: timezone.now().date())


class ChallengeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Challenge

    title = factory.Sequence(lambda n: f"Défi {n}")
    description = "Défi test"
    start_date = factory.LazyFunction(lambda: timezone.now().date())
    end_date = factory.LazyFunction(lambda: timezone.now().date())


class ChallengeProgressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChallengeProgress

    user = factory.SubFactory(UserFactory)
    challenge = factory.SubFactory(ChallengeFactory)


class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote

    text = factory.Sequence(lambda n: f"Quote text {n}")
    author = "Author Test"
    mood_tag = "happy"


class UserPreferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserPreference
        django_get_or_create = ('user',)  # cette ligne suffit souvent

    user = factory.SubFactory(UserFactory)
    dark_mode = False
    accent_color = "#6C63FF"
    font_choice = "Roboto"
    enable_animations = True



class EventLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventLog

    user = factory.SubFactory(UserFactory)
    action = "login"
    description = "Connexion test"
    severity = "info"
    created_at = factory.LazyFunction(timezone.now)


class DailyStatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DailyStat

    user = factory.SubFactory(UserFactory)
    date = factory.LazyFunction(lambda: timezone.now().date())
    mood_average = 3
    entries_count = 5 

class WeeklyStatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeeklyStat

    user = factory.SubFactory(UserFactory)
    week_start = factory.LazyFunction(lambda: timezone.now().date())
    mood_average = 3
    entries_count = 5 



class MonthlyStatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MonthlyStat

    user = factory.SubFactory(UserFactory)
    month_start = factory.LazyFunction(lambda: timezone.now().date().replace(day=1))
    mood_average = 3
    entries_count = 5 


class AnnualStatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnnualStat

    user = factory.SubFactory(UserFactory)
    year_start = factory.LazyFunction(lambda: timezone.now().date().replace(month=1, day=1))
    mood_average = 3
    entries_count = 5 
