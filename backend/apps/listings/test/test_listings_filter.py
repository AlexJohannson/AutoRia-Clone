from django.test import TestCase

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.listings.filter import ListingFilter
from apps.listings.models import ListingSellersModel
from apps.sellers.models import SellersModel
from apps.user.models import UserModel


class ListingFilterTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@example.com', password='password')

        self.seller = SellersModel.objects.create(user=self.user)

        self.brand = CarBrandModel.objects.create(brand='Toyota')

        self.car_model = CarModelModel.objects.create(car_model='Corolla', car_brand=self.brand)


        ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2010,
            country='Germany',
            region='Bavaria',
            city='Munich',
            price=5000,
            currency='EUR',
            description='Car 2010',
            seller=self.seller,
        )

        ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2015,
            country='Germany',
            region='Berlin',
            city='Berlin',
            price=15000,
            currency='EUR',
            description='Car 2015',
            seller=self.seller,
        )

        ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='France',
            region='Ile-de-France',
            city='Paris',
            price=25000,
            currency='EUR',
            description='Car 2020',
            seller=self.seller,
        )

    def test_filter_lt_year(self):
        qs = ListingSellersModel.objects.all()
        data = {'lt_year': 2016}
        filtered_qs = ListingFilter(data, queryset=qs).qs
        self.assertEqual(filtered_qs.count(), 2)
        years = set(filtered_qs.values_list('year', flat=True))
        self.assertTrue(all(year < 2016 for year in years))

    def test_filter_gt_price(self):
        qs = ListingSellersModel.objects.all()
        data = {'gt_price': 10000}
        filtered_qs = ListingFilter(data, queryset=qs).qs
        self.assertEqual(filtered_qs.count(), 2)
        prices = set(filtered_qs.values_list('price', flat=True))
        self.assertTrue(all(price > 10000 for price in prices))

    def test_filter_icontains_city(self):
        qs = ListingSellersModel.objects.all()
        data = {'icontains_city': 'ber'}
        filtered_qs = ListingFilter(data, queryset=qs).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first().city.lower(), 'berlin')

    def test_filter_range_price(self):
        qs = ListingSellersModel.objects.all()
        data = {'range_price_min': 7000, 'range_price_max': 20000}
        filtered_qs = ListingFilter(data, queryset=qs).qs
        self.assertEqual(filtered_qs.count(), 1)
        price = filtered_qs.first().price
        self.assertTrue(7000 <= price <= 20000)

    def test_filter_ordering(self):
        qs = ListingSellersModel.objects.all()
        data = {'order': '-price'}
        filtered_qs = ListingFilter(data, queryset=qs).qs
        prices = list(filtered_qs.values_list('price', flat=True))
        self.assertEqual(prices, sorted(prices, reverse=True))
