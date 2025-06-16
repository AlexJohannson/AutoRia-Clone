from django.test import TestCase

from rest_framework.test import APIRequestFactory

from apps.auto_salon.models import AutoSalonModel
from apps.auto_salon_listings.models import AutoSalonListingModel
from apps.auto_salon_listings.serializers import AutoSalonListingSerializer
from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.premium_account.models import PremiumAccountModel
from apps.user.models import UserModel


class ListingSerializerTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='password'
        )

        self.auto_salon = AutoSalonModel.objects.create(
            name='Fast Cars',
            location='Kyiv',
            user=self.user
        )
        
        self.brand = CarBrandModel.objects.create(brand='Toyota')
        self.car_model = CarModelModel.objects.create(car_model='Camry', car_brand=self.brand)
        self.factory = APIRequestFactory()

    def test_validate_price_positive(self):
        serializer = AutoSalonListingSerializer(data={
            'brand_id': self.brand.pk,
            'car_model_id': self.car_model.pk,
            'year': 2020,
            'country': 'Ukraine',
            'region': 'Kyiv',
            'city': 'Kyiv',
            'price': -10,
            'currency': 'USD',
            'description': 'Good car',
            'auto_salon': self.auto_salon.pk
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
            'auto_salon': self.auto_salon.pk,
        }
        serializer = AutoSalonListingSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        listing = serializer.save()
        self.assertEqual(listing.brand, self.brand)
        self.assertEqual(listing.car_model, self.car_model)
        self.assertEqual(listing.price, 15000)
        self.assertEqual(listing.auto_salon, self.auto_salon)

    def test_get_brand_returns_brand_name(self):
        listing = AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test',
            auto_salon=self.auto_salon,
        )
        serializer = AutoSalonListingSerializer(instance=listing)
        self.assertEqual(serializer.data['brand'], 'Toyota')



    def test_to_representation_shows_stats_for_premium(self):
        premium_account = PremiumAccountModel.objects.create(auto_salon=self.auto_salon)
        self.auto_salon.premium_account = premium_account
        self.auto_salon.save()


        AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2021,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=10000,
            currency='USD',
            description='Active car 1',
            auto_salon=self.auto_salon,
            is_active=True,
        )
        AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2022,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=20000,
            currency='USD',
            description='Active car 2',
            auto_salon=self.auto_salon,
            is_active=True,
        )

        listing = AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2023,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test premium',
            auto_salon=self.auto_salon,
            is_active=True,
        )

        request = self.factory.get('/')
        request.user = self.user
        serializer = AutoSalonListingSerializer(instance=listing, context={'request': request})
        data = serializer.data

        self.assertIn('views', data)
        self.assertIn('avg_city_price', data)
        self.assertIn('avg_region_price', data)
        self.assertIn('avg_country_price', data)


        self.assertAlmostEqual(data['avg_city_price'], 15000, delta=5000)
        self.assertAlmostEqual(data['avg_region_price'], 15000, delta=5000)
        self.assertAlmostEqual(data['avg_country_price'], 15000, delta=5000)

    def test_update_listing(self):
        listing = AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='Ukraine',
            region='Kyiv',
            city='Kyiv',
            price=15000,
            currency='USD',
            description='Test update',
            auto_salon=self.auto_salon,
        )
        new_brand = CarBrandModel.objects.create(brand='Honda')
        new_car_model = CarModelModel.objects.create(car_model='Accord', car_brand=new_brand)

        data = {
            'brand_id': new_brand.pk,
            'car_model_id': new_car_model.pk,
            'price': 18000,
        }
        serializer = AutoSalonListingSerializer(instance=listing, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.brand, new_brand)
        self.assertEqual(updated.car_model, new_car_model)
        self.assertEqual(updated.price, 18000)