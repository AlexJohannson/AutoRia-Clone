from rest_framework.permissions import BasePermission


class IsSalonAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return hasattr(request.user, 'salon_role') and request.user.salon_role.role in ['superuser', 'admin']
