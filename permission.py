from rest_framework import permissions

class IsPublisherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role == 'publisher' or user.is_staff)
