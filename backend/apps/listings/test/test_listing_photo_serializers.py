import os
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PIL import Image

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.listings.models import ListingSellersModel
from apps.listings.serializer import ListingPhotoSerializer
from apps.sellers.models import SellersModel
from apps.user.models import UserModel


class ListingPhotoSerializerTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='user2@example.com', password='password')

        self.seller = SellersModel.objects.create(user=self.user)

        self.brand = CarBrandModel.objects.create(brand='BMW')

        self.car_model = CarModelModel.objects.create(car_model='X5', car_brand=self.brand)

        self.listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2021,
            country='Germany',
            region='Bavaria',
            city='Munich',
            price=50000,
            currency='EUR',
            description='Luxury car',
            seller=self.seller,
        )

    def generate_photo_file(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'JPEG')
        file.name = 'test.jpg'
        file.seek(0)
        return SimpleUploadedFile(file.name, file.read(), content_type='image/jpeg')

    def test_photo_serialization_and_update(self):
        photo = self.generate_photo_file()
        self.assertFalse(self.listing.photo)

        data = {'photo': photo}

        serializer = ListingPhotoSerializer(instance=self.listing, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_listing = serializer.save()


        self.assertTrue(updated_listing.photo)
        from django.db.models.fields.files import ImageFieldFile
        self.assertIsInstance(updated_listing.photo, ImageFieldFile)


        self.assertIsInstance(updated_listing.photo.name, str)
        self.assertNotEqual(updated_listing.photo.name, '')


        from django.conf import settings
        file_path = os.path.join(settings.MEDIA_ROOT, updated_listing.photo.name)
        self.assertTrue(os.path.exists(file_path))



