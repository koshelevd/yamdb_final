from rest_framework import permissions


class IsGetOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_staff and request.user.is_authenticated


class IsGetOrPostOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated and request.method == 'POST':
            return True
        if (request.method == 'PATCH' or request.method == 'DELETE') and (
                obj.author == request.user or request.user.is_admin
                or request.user.is_moderator):
            return True
