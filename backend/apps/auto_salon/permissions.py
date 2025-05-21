from rest_framework.permissions import BasePermission


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff



class IsSalonOwnerAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user


        if user.is_superuser or user.is_staff:
            return True


        if hasattr(user, 'salon_role'):
            salon_role = user.salon_role

            return (
                salon_role.auto_salon.id == obj.id and
                salon_role.role in ['superuser', 'admin']
            )

        return False
