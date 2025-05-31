from random import choices

from django_filters import rest_framework as filters

from .models import SalonRoleModels


class SalonRoleFilter(filters.FilterSet):
    role = filters.ChoiceFilter('role', choices=SalonRoleModels.ROLE_CHOICES)

    order = filters.OrderingFilter(
        fields=(
            'id',
            'role'
        )
    )