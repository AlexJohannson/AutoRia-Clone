from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff or request.user.is_superuser


class IsSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser