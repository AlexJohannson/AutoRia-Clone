from rest_framework.permissions import BasePermission

from apps.salon_role.models import SalonRoleModels


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsSalonStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser or getattr(user, 'is_staff', False):
            return True

        salon_role = SalonRoleModels.objects.filter(user=user)
        return salon_role.filter(role__in = ['superuser', 'admin', 'seller']).exists()









