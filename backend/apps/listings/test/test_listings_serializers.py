from django.test import TestCase

from rest_framework.test import APIRequestFactory

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.listings.models import ListingSellersModel
from apps.listings.serializer import ListingSerializer
from apps.premium_account.models import PremiumAccountModel
from apps.sellers.models import SellersModel
from apps.user.models import UserModel


class ListingSerializerTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user@example.com', password='password')

        self.seller = SellersModel.objects.create(user=self.user)

        self.brand = CarBrandModel.objects.create(brand='Toyota')

        self.car_model = CarModelModel.objects.create(car_model='Camry', car_brand=self.brand)
        self.factory = APIRequestFactory()

    def test_validate_price_positive(self):
        serializer = ListingSerializer(data={
            'brand_id': self.brand.pk,
            'car_model_id': self.car_model.pk,
            'year': 2020,
            'country': 'Ukraine',
            'region': 'Kyiv',
            'city': 'Kyiv',
            'price': -10,
            'currency': 'USD',
            'description': 'Good car',
            'seller': self.seller.pk
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertEqual(serializer.errors['price'][0], 'Price must be greater than 0')

    def test_create_listing(self):
        data = {
            'brand_id': self.brand.pk,
            'car_model_id': self.car_model.pk,
            'year': 2020,
            'country': 'Ukraine',
            'region': 'Kyiv',
            'city': 'Kyiv',
            'price': 15000,
            'currency': 'USD',
            'description': 'Nice car',
            'seller': self.seller.pk,
        }
        serializer = ListingSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        listing = serializer.save()
        self.assertEqual(listing.brand, self.brand)
        self.assertEqual(listing.car_model, self.car_model)
        self.assertEqual(listing.price, 15000)
        self.assertEqual(listing.seller, self.seller)

    def test_get_brand_returns_brand_name(self):
        listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test',
            seller=self.seller,
        )
        serializer = ListingSerializer(instance=listing)
        self.assertEqual(serializer.data['brand'], 'Toyota')

    def test_to_representation_hides_stats_for_non_premium(self):

        if not hasattr(self.seller, 'base_account'):
            from apps.base_account.models import BaseAccountModel
            BaseAccountModel.objects.create(seller=self.seller)

        listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test',
            seller=self.seller,
            views=100,
            daily_views=10,
            weekly_views=20,
            monthly_views=30,
        )


        request = self.factory.get('/')
        request.user = self.user

        serializer = ListingSerializer(instance=listing, context={'request': request})
        data = serializer.data

        self.assertNotIn('views', data)
        self.assertNotIn('daily_views', data)
        self.assertNotIn('weekly_views', data)
        self.assertNotIn('monthly_views', data)

    def test_to_representation_shows_stats_for_premium(self):
        premium_account = PremiumAccountModel.objects.create(seller=self.seller)
        self.seller.premium_account = premium_account
        self.seller.save()


        ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2021,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=10000,
            currency='USD',
            description='Active car 1',
            seller=self.seller,
            is_active=True,
        )

        ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2022,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=20000,
            currency='USD',
            description='Active car 2',
            seller=self.seller,
            is_active=True,
        )

        listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2023,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test premium',
            seller=self.seller,
            is_active=True,
        )

        request = self.factory.get('/')
        request.user = self.user
        serializer = ListingSerializer(instance=listing, context={'request': request})
        data = serializer.data

        self.assertIn('views', data)
        self.assertIn('avg_city_price', data)
        self.assertIn('avg_region_price', data)
        self.assertIn('avg_country_price', data)


        self.assertAlmostEqual(data['avg_city_price'], 15000, delta=5000)
        self.assertAlmostEqual(data['avg_region_price'], 15000, delta=5000)
        self.assertAlmostEqual(data['avg_country_price'], 15000, delta=5000)

    def test_update_listing(self):
        listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test update',
            seller=self.seller,
        )
        new_brand = CarBrandModel.objects.create(brand='Honda')
        new_car_model = CarModelModel.objects.create(car_model='Accord', car_brand=new_brand)

        data = {
            'brand_id': new_brand.pk,
            'car_model_id': new_car_model.pk,
            'price': 18000,
        }
        serializer = ListingSerializer(instance=listing, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.brand, new_brand)
        self.assertEqual(updated.car_model, new_car_model)
        self.assertEqual(updated.price, 18000)


