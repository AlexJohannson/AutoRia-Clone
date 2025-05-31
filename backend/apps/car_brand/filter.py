from django_filters import rest_framework as filters


class CarBrandFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'brand'
        )
    )