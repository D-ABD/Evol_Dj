# Myevol_app/api_urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from Myevol_app.viewsets.badge_viewset import BadgeTemplateViewSet, BadgeViewSet
from Myevol_app.viewsets.challenge_viewset import ChallengeProgressViewSet, ChallengeViewSet
from Myevol_app.viewsets.event_log_viewset import EventLogViewSet
from Myevol_app.viewsets.journal_viewset import JournalEntryViewSet
from Myevol_app.viewsets.notification_viewset import NotificationViewSet
from Myevol_app.viewsets.objective_viewset import ObjectiveViewSet
from Myevol_app.viewsets.quote_viewset import QuoteViewSet
from Myevol_app.viewsets.stats_viewset import StatsViewSet
from Myevol_app.viewsets.temporaire_viewset import test_token_view
from Myevol_app.viewsets.userPreference_viewset import UserPreferenceViewSet
from Myevol_app.viewsets.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'badges/templates', BadgeTemplateViewSet, basename='badgetemplate')

router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'challenges/progress', ChallengeProgressViewSet, basename='challengeprogress')

router.register(r'logs', EventLogViewSet, basename='eventlog')

router.register(r'journal-entries', JournalEntryViewSet, basename='journalentry')

router.register(r'notifications', NotificationViewSet, basename='notification')

router.register(r'objectives', ObjectiveViewSet, basename='objective')

router.register(r'quotes', QuoteViewSet, basename='quote')

router.register(r'stats', StatsViewSet, basename='stats')

router.register(r'users', UserViewSet, basename='user')

router.register(r'user-preferences', UserPreferenceViewSet, basename='userpreference')  # 👈 à ajouter


urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('test-token/', test_token_view),

]