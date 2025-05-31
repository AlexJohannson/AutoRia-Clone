from django_filters import rest_framework as filters


class ListingFilter(filters.FilterSet):
    lt_year = filters.NumberFilter(field_name='year', lookup_expr='lt')
    gt_year = filters.NumberFilter(field_name='year', lookup_expr='gt')
    lt_price = filters.NumberFilter(field_name='price', lookup_expr='lt')
    gt_price = filters.NumberFilter(field_name='price', lookup_expr='gt')

    icontains_city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    icontains_region = filters.CharFilter(field_name='region', lookup_expr='icontains')
    icontains_country = filters.CharFilter(field_name='country', lookup_expr='icontains')


    range_price = filters.RangeFilter(field_name='price')
    range_year = filters.RangeFilter(field_name='year')
    price_in = filters.BaseInFilter(field_name='price')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'price',
            'year'
        )
    )
