from django_filters import rest_framework as filters


class AutoSalonFilter(filters.FilterSet):
    icontains_name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    icontains_location = filters.CharFilter(field_name='location', lookup_expr='icontains')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'name',
            'location'
        )
    )