# Myevol_app/permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Autorise l'accès si l'utilisateur est soit le propriétaire de l'objet, soit administrateur.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return hasattr(obj, 'user') and obj.user == request.user
