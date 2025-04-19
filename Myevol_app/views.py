from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import JournalEntryForm, ObjectiveForm
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from .models import JournalEntry
from .utils.stats import get_weekly_entry_stats
from .utils.levels import get_user_level, get_user_progress
from .models import BadgeTemplate
from .models import Notification
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import Objective



def home_view(request):
    if request.user.is_authenticated:
        return redirect("myevol:dashboard")
    return render(request, "myevol/home.html")

# Formulaire d'inscription personnalisé
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Compte créé avec succès. Connecte-toi !")
            return redirect("myevol:login")
    else:
        form = RegisterForm()
    return render(request, "myevol/users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("myevol:dashboard")
        else:
            messages.error(request, "Identifiants incorrects.")
    else:
        form = AuthenticationForm()
    return render(request, "myevol/users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Déconnexion réussie.")
    return redirect("myevol:login")


@login_required
def add_entry_view(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Entrée ajoutée avec succès ✅")
            return redirect("myevol:dashboard")
    else:
        form = JournalEntryForm()
    
    return render(request, "myevol/add_entry.html", {"form": form})



@login_required
def dashboard_view(request):
    entries = request.user.entries.order_by('-created_at')
    objectives = request.user.objectives.order_by('target_date')
    
    total_entries = entries.count()
    avg_mood = entries.aggregate(avg=Avg("mood"))["avg"] or 0
    categories_stats = entries.values("category").annotate(count=Count("id")).order_by("-count")
    
    week_stats = get_weekly_entry_stats(request.user)
    user_level = get_user_level(total_entries)
    progression = get_user_progress(total_entries)
    
    # Notifications non lues
    notifications = request.user.notifications.filter(is_read=False)
    
    # Crée le contexte complet
    context = {
        "entries": entries,
        "objectives": objectives,
        "total_entries": total_entries,
        "avg_mood": round(avg_mood, 1),
        "categories_stats": categories_stats,
        "week_stats": week_stats,
        "user_level": user_level,
        "progression": progression,
        "notifications": notifications,
    }

    # Marque les notifications comme lues
    request.user.notifications.filter(is_read=False).update(is_read=True)

    return render(request, "myevol/dashboard.html", context)


@login_required
def add_objective_view(request):
    if request.method == "POST":
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.user = request.user
            objective.save()
            messages.success(request, "Objectif ajouté avec succès 🎯")
            return redirect("myevol:dashboard")
    else:
        form = ObjectiveForm()
    return render(request, "myevol/add_objective.html", {"form": form})



@login_required
def edit_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrée mise à jour ✅")
            return redirect("myevol:dashboard")
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, "myevol/edit_entry.html", {"form": form})


@login_required
def delete_entry_view(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.warning(request, "Entrée supprimée ❌")
        return redirect("myevol:dashboard")
    return render(request, "myevol/delete_entry.html", {"entry": entry})



@login_required
def badge_list_view(request):
    badges = request.user.badges.order_by('-date_obtenue')
    return render(request, "myevol/badges/badge_list.html", {"badges": badges})



@login_required
def explore_badges_view(request):
    templates = BadgeTemplate.objects.all()
    earned_names = request.user.badges.values_list("name", flat=True)

    for template in templates:
        template.obtenu = template.name in earned_names

    return render(request, "myevol/badges/badge_explore.html", {
        "templates": templates
    })



@login_required
def notification_list_view(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, "myevol/notifications.html", {"notifications": notifications})



@login_required
def weekly_mood_chart(request):
    today = now().date()
    start = today - timedelta(days=6)
    data = (
        JournalEntry.objects.filter(user=request.user, created_at__date__range=(start, today))
        .extra(select={'day': "DATE(created_at)"})
        .values('day')
        .annotate(avg_mood=Avg("mood"))
        .order_by("day")
    )

    labels = []
    values = []

    for i in range(7):
        day = (start + timedelta(days=i))
        labels.append(day.strftime("%a %d"))
        found = next((d for d in data if d["day"] == str(day)), None)
        values.append(round(found["avg_mood"], 1) if found else 0)

    return JsonResponse({"labels": labels, "data": values})


@login_required
def monthly_objectives_chart(request):
    current_year = now().year
    data = (
        Objective.objects.filter(user=request.user, done=True, target_date__year=current_year)
        .annotate(month=TruncMonth("target_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    labels = []
    values = []

    for i in range(1, 13):
        month_name = now().replace(month=i).strftime("%b")
        labels.append(month_name)
        found = next((d for d in data if d["month"].month == i), None)
        values.append(found["count"] if found else 0)

    return JsonResponse({"labels": labels, "data": values})

@login_required
def objectives_by_category_chart(request):
    data = (
        Objective.objects.filter(user=request.user, done=True)
        .values("category")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    labels = [item["category"] for item in data]
    values = [item["count"] for item in data]

    return JsonResponse({"labels": labels, "data": values})

@login_required
def mood_objectives_over_time(request):
    start_date = now().date() - timedelta(days=30)
    moods = (
        JournalEntry.objects.filter(user=request.user, created_at__date__gte=start_date)
        .extra(select={'day': "DATE(created_at)"})
        .values("day")
        .annotate(avg_mood=Avg("mood"))
        .order_by("day")
    )
    goals = (
        Objective.objects.filter(user=request.user, done=True, target_date__gte=start_date)
        .extra(select={'day': "DATE(target_date)"})
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    labels = []
    moods_by_day = {}
    goals_by_day = {}

    for i in range(31):
        d = start_date + timedelta(days=i)
        labels.append(d.strftime("%d/%m"))
        moods_by_day[str(d)] = next((x["avg_mood"] for x in moods if x["day"] == str(d)), 0)
        goals_by_day[str(d)] = next((x["count"] for x in goals if x["day"] == str(d)), 0)

    return JsonResponse({
        "labels": labels,
        "moods": list(moods_by_day.values()),
        "objectives": list(goals_by_day.values())
    })
