from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import timedelta

def get_weekly_entry_stats(user):
    today = now().date()
    week_start = today - timedelta(days=today.weekday())

    entries = user.entries.filter(created_at__date__gte=week_start)
    daily_stats = (
        entries.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    # Pré-remplissage des jours
    result = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        stat = next((item for item in daily_stats if item["day"] == day), None)
        result.append({
            "day": day.strftime('%A'),  # lundi, mardi…
            "total": stat["total"] if stat else 0,
        })
    return result
