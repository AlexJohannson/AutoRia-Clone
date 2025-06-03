from rest_framework.permissions import BasePermission


class IsParticipantOrAdmin(BasePermission):
   def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        return obj.messages.filter(user=user).exists()


class IsMessageOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.user == user or user.is_staff or user.is_superuser
