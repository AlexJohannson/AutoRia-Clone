import os
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.listings.models import ListingSellersModel
from apps.sellers.models import SellersModel
from apps.user.models import UserModel


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ListingSellersModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='user@example.com',
            password='password123'
        )


        self.seller = SellersModel.objects.create(user=self.user)


        self.brand = CarBrandModel.objects.create(brand='Tesla')

        self.car_model = CarModelModel.objects.create(car_model='Model S', car_brand=self.brand)


        self.photo_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04',
            content_type='image/jpeg'
        )

    def test_full_listing_creation_and_deletion(self):
        listing = ListingSellersModel.objects.create(
            photo=self.photo_file,
            brand=self.brand,
            car_model=self.car_model,
            year=2022,
            country='Ukraine',
            region='Kyivska',
            city='Kyiv',
            price=30000.0,
            currency='USD',
            price_usd=30000.0,
            price_eur=27000.0,
            price_uah=1100000.0,
            exchange_rate_used='Bank of Ukraine source',
            description='Good car!',
            seller=self.seller,
            is_active=True,
            avg_city_price=31000.0,
            avg_region_price=30500.0,
            avg_country_price=29500.0,
            views=10,
            daily_views=3,
            weekly_views=7,
            monthly_views=10,
            bad_word_attempts=0
        )


        self.assertEqual(listing.brand.brand, 'Tesla')
        self.assertEqual(listing.car_model.car_model, 'Model S')
        self.assertEqual(listing.year, 2022)
        self.assertEqual(listing.country, 'Ukraine')
        self.assertEqual(listing.price, 30000.0)
        self.assertEqual(listing.currency, 'USD')
        self.assertEqual(listing.price_usd, 30000.0)
        self.assertEqual(listing.price_eur, 27000.0)
        self.assertEqual(listing.price_uah, 1100000.0)
        self.assertEqual(listing.exchange_rate_used, 'Bank of Ukraine source')
        self.assertEqual(listing.seller, self.seller)
        self.assertTrue(listing.is_active)
        self.assertEqual(listing.views, 10)
        self.assertEqual(listing.bad_word_attempts, 0)
        self.assertTrue(os.path.exists(listing.photo.path))


        photo_path = listing.photo.path
        listing.delete()
        self.assertFalse(os.path.exists(photo_path))
