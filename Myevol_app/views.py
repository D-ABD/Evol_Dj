from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def home_view(request):
    return render(request, "myevol/home.html")

def dashboard_view(request):
    return render(request, "myevol/dashboard.html")

def add_entry_view(request):
    return render(request, "myevol/add_entry.html")

def add_objective_view(request):
    return render(request, "myevol/add_objective.html")

def badge_list_view(request):
    return render(request, "myevol/badge_list.html")

def badge_explore_view(request):
    return render(request, "myevol/badge_explore.html")

def notifications_view(request):
    return render(request, "myevol/notifications.html")

def logout_view(request):
    logout(request)
    return redirect("myevol:home")
