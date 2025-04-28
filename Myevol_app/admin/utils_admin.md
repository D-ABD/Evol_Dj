from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.urls import reverse
from django.utils.timezone import now
from django.utils.safestring import mark_safe

# Import de tous les modèles
from ..models import (
    Badge,
    BadgeTemplate,
    Challenge,
    ChallengeProgress,
    EventLog,
    JournalEntry,
    JournalMedia,
    Notification,
    Objective,
    Quote,
    DailyStat,
    WeeklyStat,
    User,
    UserPreference
)

# Configuration des groupes d'administration
admin.site.site_header = "Administration MyEvol"
admin.site.site_title = "MyEvol Admin"
admin.site.index_title = "Tableau de bord d'administration"

# Organisation des modèles par sections dans l'admin
class MyEvolAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Organise les modèles par groupes fonctionnels pour une navigation plus intuitive
        """
        app_list = super().get_app_list(request)
        
        # Créer des sections personnalisées
        custom_app_list = []
        
        # Section Utilisateurs
        users_app = {
            'name': 'Utilisateurs',
            'app_label': 'users',
            'app_url': '/admin/users/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Journal
        journal_app = {
            'name': 'Journal',
            'app_label': 'journal',
            'app_url': '/admin/journal/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Engagement
        engagement_app = {
            'name': 'Engagement',
            'app_label': 'engagement',
            'app_url': '/admin/engagement/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Statistiques
        stats_app = {
            'name': 'Statistiques',
            'app_label': 'stats',
            'app_url': '/admin/stats/',
            'has_module_perms': True,
            'models': []
        }
        
        # Section Système
        system_app = {
            'name': 'Système',
            'app_label': 'system',
            'app_url': '/admin/system/',
            'has_module_perms': True,
            'models': []
        }
        
        # Dictionnaire pour mapper les modèles aux sections
        model_mapping = {
            'users': ['User', 'UserPreference', 'Badge', 'BadgeTemplate'],
            'journal': ['JournalEntry', 'JournalMedia', 'Objective'],
            'engagement': ['Challenge', 'ChallengeProgress', 'Notification', 'Quote'],
            'stats': ['DailyStat', 'WeeklyStat'],
            'system': ['EventLog']
        }
        
        # Obtenir tous les modèles
        all_models = []
        for app in app_list:
            all_models.extend(app['models'])
        
        # Répartir les modèles dans les sections personnalisées
        for model in all_models:
            model_name = model['object_name']
            
            if model_name in model_mapping['users']:
                users_app['models'].append(model)
            elif model_name in model_mapping['journal']:
                journal_app['models'].append(model)
            elif model_name in model_mapping['engagement']:
                engagement_app['models'].append(model)
            elif model_name in model_mapping['stats']:
                stats_app['models'].append(model)
            elif model_name in model_mapping['system']:
                system_app['models'].append(model)
        
        # Ajouter les sections à la liste personnalisée
        custom_app_list.append(users_app)
        custom_app_list.append(journal_app)
        custom_app_list.append(engagement_app)
        custom_app_list.append(stats_app)
        custom_app_list.append(system_app)
        
        # Garder les autres applications non classées
        for app in app_list:
            if app['app_label'] not in ['users', 'journal', 'engagement', 'stats', 'system']:
                custom_app_list.append(app)
        
        return custom_app_list

