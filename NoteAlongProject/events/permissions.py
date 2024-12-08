from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMusicianOwnerOrReadOnly(BasePermission):
    """
    Custom permission: Only the musician of the concert can modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only methods for all users
        if request.method in SAFE_METHODS:
            return True

        # Allow write/delete only if the logged-in user is the musician of the concert
        return request.user == obj.musician

    def has_permission(self, request, view):
        # Allow GET for everyone
        if request.method in SAFE_METHODS:
            return True

        # For POST, ensure the user is a musician
        if request.method == "POST":
            return hasattr(request.user, 'profile') and request.user.profile.is_musician

        # Other methods (PUT, DELETE) are handled in has_object_permission
        return True


class IsSuperAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow full CRUD for superadmins,
    and read-only access for all other users.
    """
    def has_permission(self, request, view):
        # Allow read-only methods for all users
        if request.method in SAFE_METHODS:
            return True
        # Allow full access only for superadmins
        return request.user.is_superuser