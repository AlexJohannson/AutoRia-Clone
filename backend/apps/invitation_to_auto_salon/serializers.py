from rest_framework import serializers

from apps.invitation_to_auto_salon.models import JoinRequestModel
from apps.salon_role.models import SalonRoleModels


class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequestModel
        fields = (
            'id',
            'user',
            'auto_salon',
            'role',
            'status',
            'created_at'
        )
        read_only_fields = (
            'id',
            'user',
            'status',
            'created_at'
        )

    def validate(self, attrs):
        if SalonRoleModels.is_role_taken(attrs['auto_salon'], attrs['role']):
            raise serializers.ValidationError(
                f"The role {attrs['role']} is already taken in this auto_salon."
            )
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'
        return super().create(validated_data)
