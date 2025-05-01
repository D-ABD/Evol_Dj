from django.urls import path
from . import views

app_name = "myevol"

urlpatterns = [
    # Pages principales
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Entrées et objectifs
    path('add-entry/', views.add_entry_view, name='add_entry'),
    path('add-objective/', views.add_objective_view, name='add_objective'),

    # Badges
    path('badges/', views.badge_list_view, name='badge_list'),
    path('badges/explorer/', views.badge_explore_view, name='badge_explore'),

    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),

    # Authentification
    path('logout/', views.logout_view, name='logout'),  # à ajuster si besoin
]
