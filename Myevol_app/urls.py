from django.urls import path
from . import views

app_name = "myevol"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("add-entry/", views.add_entry_view, name="add_entry"),
    path("add-objective/", views.add_objective_view, name="add_objective"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("entry/<int:entry_id>/edit/", views.edit_entry_view, name="edit_entry"),
    path("entry/<int:entry_id>/delete/", views.delete_entry_view, name="delete_entry"),
    path("badges/", views.badge_list_view, name="badge_list"),
    path("badges/explorer/", views.explore_badges_view, name="badge_explore"),
    path("notifications/", views.notification_list_view, name="notifications"),
    path("api/mood/week/", views.weekly_mood_chart, name="weekly_mood_chart"),
    path("api/objectives/monthly/", views.monthly_objectives_chart, name="monthly_objectives_chart"),
    path("api/objectives/by-category/", views.objectives_by_category_chart, name="objectives_by_category_chart"),
    path("api/mood-objectives/timeline/", views.mood_objectives_over_time, name="mood_objectives_chart"),


]
