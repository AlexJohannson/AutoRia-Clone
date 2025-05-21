from rest_framework import serializers

from apps.auto_salon.serializers import AutoSalonSerializer
from apps.salon_role.models import SalonRoleModels
from apps.user.serializers import UserSerializer


class SalonRoleSerializer(serializers.ModelSerializer):
    auto_salon = AutoSalonSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = SalonRoleModels
        fields = (
            'id',
            'user',
            'auto_salon',
            'role',
        )

    def validate(self, attrs):
        auto_salon = attrs['auto_salon']
        role = attrs['role']

        if SalonRoleModels.is_role_taken(auto_salon, role):
            raise serializers.ValidationError(f'The role {role} already exists in this auto_salon')

        return attrs