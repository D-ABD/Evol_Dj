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
    path('logout/', views.logout_view, name='logout'),  # logout à définir selon ton auth
]
