from rest_framework import permissions

class IsPostAuthorOrSuperAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return obj.author == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True


class IsCommentAuthorOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True


        if request.method in ['PUT', 'DELETE']:
            return obj.author == request.user or request.user.is_superuser

        return False