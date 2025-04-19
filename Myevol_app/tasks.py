from celery import shared_task
from django.utils.timezone import now
from .models import Notification

@shared_task
def send_scheduled_notifications():
    """
    Tâche périodique pour envoyer les notifications programmées.
    
    Cette tâche est exécutée par Celery selon une planification définie dans les paramètres.
    Elle identifie toutes les notifications programmées dont la date d'échéance est atteinte
    et n'ont pas encore été lues, puis effectue les actions nécessaires pour les envoyer.
    
    Returns:
        str: Message indiquant le nombre de notifications traitées
    """
    # Récupère toutes les notifications programmées dont la date d'envoi est arrivée
    # et qui n'ont pas encore été lues
    qs = Notification.objects.filter(scheduled_at__lte=now(), is_read=False)
    
    count = 0  # Compteur pour suivre le nombre de notifications traitées
    
    for notif in qs:
        # Ici, implémentez la logique d'envoi appropriée selon le type de notification
        # Par exemple : envoi d'email, notification push, SMS, etc.
        # Exemple : send_push_notification(notif.user.device_token, notif.message)
        
        notif.mark_as_read()  # Marque la notification comme lue après l'envoi
        count += 1
    
    # Retourne un message descriptif pour les logs Celery
    return f"{count} notifications envoyées"