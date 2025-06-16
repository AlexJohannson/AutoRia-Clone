from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    lt_house = filters.NumberFilter(field_name='profile__house', lookup_expr='lt')
    gt_house = filters.NumberFilter(field_name='profile__house', lookup_expr='gt')
    lt_age = filters.NumberFilter(field_name='profile__age', lookup_expr='lt')
    gt_age = filters.NumberFilter(field_name='profile__age', lookup_expr='gt')



    icontains_name = filters.CharFilter(field_name='profile__name', lookup_expr='icontains')
    icontains_surname = filters.CharFilter(field_name='profile__surname', lookup_expr='icontains')
    icontains_street = filters.CharFilter(field_name='profile__street', lookup_expr='icontains')
    icontains_city = filters.CharFilter(field_name='profile__city', lookup_expr='icontains')
    icontains_region = filters.CharFilter(field_name='profile__region', lookup_expr='icontains')
    icontains_country = filters.CharFilter(field_name='profile__country', lookup_expr='icontains')
    gender = filters.CharFilter(field_name='profile__gender', lookup_expr='iexact')




    order = filters.OrderingFilter(
        fields=(
            ('profile__id', 'profile_id'),
            ('profile__name', 'profile_name'),
            ('profile__surname', 'profile_surname'),
            ('profile__age', 'profile_age'),
        )
    )

