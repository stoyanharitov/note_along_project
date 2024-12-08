from django.shortcuts import redirect
from NoteAlongProject.accounts.models import Profile
from django.contrib.auth.models import Group

class EnsureProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith('/admin/'):
            if not hasattr(request.user, 'profile'):
                Profile.objects.create(user=request.user)
        response = self.get_response(request)
        return response


class SuperAdminGroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            self.handle_super_admin_group(request.user)
        response = self.get_response(request)
        return response

    def handle_super_admin_group(self, user):
        full_crud_admin_group, created = Group.objects.get_or_create(name='Full_CRUD_admin')

        if user.is_superuser and full_crud_admin_group not in user.groups.all():
            user.groups.add(full_crud_admin_group)
            user.save()

        elif not user.is_superuser and full_crud_admin_group in user.groups.all():
            user.groups.remove(full_crud_admin_group)
            user.save()