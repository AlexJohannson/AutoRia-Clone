from django_filters import rest_framework as filters


class CarModelFilter(filters.FilterSet):
    model = filters.CharFilter(field_name='car_brand', lookup_expr='icontains')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'car_model'
        )
    )