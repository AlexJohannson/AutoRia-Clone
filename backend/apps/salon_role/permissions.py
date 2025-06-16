from rest_framework.permissions import BasePermission

from apps.salon_role.models import SalonRoleModels


class IsSalonMemberOrAdmin(BasePermission):
   def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return hasattr(request.user, 'salon_role')



class CanManageSalonRole(BasePermission):
    def has_object_permission(self, request, view, obj: SalonRoleModels):
        user = request.user

        if user.is_superuser or user.is_staff:
            return True

        if not hasattr(user, 'salon_role'):
            return False

        user_role = user.salon_role
        target_role = obj


        if user_role.auto_salon != target_role.auto_salon:
            return False


        if user_role.role == 'superuser':
            return True


        if user_role.role == 'admin':
            if target_role.user == user:
                return True
            return target_role.role in ['seller', 'mechanic', 'superuser']


        if user_role.role in ['seller', 'mechanic']:
            return target_role.user == user

        return False



