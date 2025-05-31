from django_filters import rest_framework as filters


class SellerFilter(filters.FilterSet):
    order = filters.OrderingFilter(
        fields=(
            'id',
        )
    )