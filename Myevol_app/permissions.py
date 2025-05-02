from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Autorise l'accès si l'utilisateur est authentifié :
    - Et soit administrateur
    - Soit propriétaire de l'objet (dans le cas d'une instance)
    """

    def has_permission(self, request, view):
        # Ajout de prints pour le débogage
        is_auth = request.user and request.user.is_authenticated
        print(f"has_permission: user={request.user}, is_authenticated={is_auth}")
        print(f"Token payload: {getattr(request.auth, 'payload', 'No payload')}")
        print(f"User ID: {getattr(request.user, 'id', 'No ID')}")
        return is_auth

    def has_object_permission(self, request, view, obj):
        # Ajout de prints pour le débogage
        is_admin = request.user.is_staff or request.user.is_superuser
        is_owner = hasattr(obj, 'user') and obj.user == request.user
        print(f"has_object_permission: user={request.user}, is_admin={is_admin}, is_owner={is_owner}")
        print(f"Object user: {getattr(obj, 'user', 'No user attribute')}")
        
        # ✅ Si admin, toujours autorisé
        if is_admin:
            print("Access granted: User is admin")
            return True

        # ✅ Sinon, il faut que l'objet ait un champ `user` correspondant
        if is_owner:
            print("Access granted: User is owner")
            return True
            
        print("Access denied: User is neither admin nor owner")
        return False