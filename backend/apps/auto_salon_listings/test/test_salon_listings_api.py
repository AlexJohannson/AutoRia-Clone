from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from PIL import Image

from apps.auto_salon.models import AutoSalonModel
from apps.auto_salon_listings.models import AutoSalonListingModel
from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.forbiddenword.models import Forbiddenwords
from apps.salon_role.models import SalonRoleModels
from apps.user.models import ProfileModel

User = get_user_model()

class ListingApiTestCase(APITestCase):
    def setUp(self):
        AutoSalonListingModel.objects.all().delete()
        cache.clear()

        self.brand = CarBrandModel.objects.create(brand="Toyota")

        self.car_model = CarModelModel.objects.create(
            car_model="Camry",
            car_brand=self.brand
        )

        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='password',
            is_staff=True,
            is_superuser=True
        )


        self.admin_user = User.objects.create_user(
            email="adminuser@test.com",
            password="pass",
            is_staff=True
        )
        self.admin_user.profile = ProfileModel.objects.create(
            user=self.admin_user,
            name="Adminuser",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )

        self.seller_user = User.objects.create_user(
            email="seller@test.com",
            password="pass"
        )
        self.seller_user.profile = ProfileModel.objects.create(
            user=self.seller_user,
            name="Seller",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )

        self.unauthorized_user = User.objects.create_user(
            email="unauth@test.com",
            password="pass"
        )
        self.unauthorized_user.profile = ProfileModel.objects.create(
            user=self.unauthorized_user,
            name="Test",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Male"
        )

        self.user = User.objects.create_user(
            email="user@test.com",
            password="pass"
        )
        self.user.profile = ProfileModel.objects.create(
            user=self.user,
            name="User",
            surname="Test",
            age=30,
            house=10,
            street="Main",
            city="Test",
            region="Test",
            country="Test",
            gender="Female"
        )

        self.auto_salon = AutoSalonModel.objects.create(
            user=self.admin_user,
            name="BestCars"
        )

        SalonRoleModels.objects.create(
            user=self.seller_user,
            auto_salon=self.auto_salon,
            role="seller"
        )

        self.list_url = reverse("auto-salon-listing-create")
        self.active_listing = AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country="Ukraine",
            region="Kyiv",
            city="Kyiv",
            price=10000,
            currency="USD",
            price_usd=10000,
            price_eur=9200,
            price_uah=380000,
            exchange_rate_used="2024-01-01",
            auto_salon=self.auto_salon,
            is_active=True
        )

        self.inactive_listing = AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country="Ukraine",
            region="Kyiv",
            city="Kyiv",
            price=10000,
            currency="USD",
            price_usd=10000,
            price_eur=9200,
            price_uah=380000,
            exchange_rate_used="2024-01-01",
            auto_salon=self.auto_salon,
            is_active=False
        )

        self.detail_url = reverse(
            "auto-salon-listing-retrieve",
            kwargs={"pk": self.active_listing.id}
        )

        self.data = {
            "brand_id": self.brand.id,
            "car_model_id": self.car_model.id,
            "year": 2020,
            "country": "Ukraine",
            "region": "Kyiv",
            "city": "Kyiv",
            "price": 10000,
            "currency": "USD",
            "description": "A nice car",
            "exchange_rate_used": "2024-01-01",
            "auto_salon": self.auto_salon.id
        }

    def test_get_listings_returns_only_active(self):
        url = reverse('auto-salon-listing-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        results = data.get('data', [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.active_listing.id)

    def test_get_active_listing_detail_success(self):
        url = reverse('auto-salon-listing-retrieve', kwargs={'pk': self.active_listing.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.active_listing.id)

    def test_create_listing_by_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_listing_by_seller_success(self):
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_listing_forbidden_for_unauthorized_user(self):
        self.client.force_authenticate(user=self.unauthorized_user)
        response = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_listing_unauthenticated(self):
        response = self.client.post(self.list_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_listing_by_salon_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        updated_payload = self.data.copy()
        updated_payload["price"] = 12000
        response = self.client.put(self.detail_url, updated_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_listing_by_seller_success(self):
        self.client.force_authenticate(user=self.seller_user)
        updated_payload = self.data.copy()
        updated_payload["price"] = 13000
        response = self.client.put(self.detail_url, updated_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_listing_by_unauthorized_user_forbidden(self):
        self.client.force_authenticate(user=self.unauthorized_user)
        updated_payload = self.data.copy()
        updated_payload["price"] = 14000
        response = self.client.put(self.detail_url, updated_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_listing_by_unauthorized_user_forbidden(self):
        self.client.force_authenticate(user=self.unauthorized_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_listing_by_seller_success(self):
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_listing_by_admin_success(self):
        listing = AutoSalonListingModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country="Ukraine",
            region="Kyiv",
            city="Kyiv",
            price=11000,
            currency="USD",
            price_usd=11000,
            price_eur=10100,
            price_uah=420000,
            exchange_rate_used="2024-01-01",
            auto_salon=self.auto_salon,
            is_active=True
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "auto-salon-listing-retrieve",
            kwargs={"pk": listing.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_inactive_listing_detail_not_found(self):
        url = reverse(
            'auto-salon-listing-retrieve',
            kwargs={'pk': self.inactive_listing.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_photo_to_listing_success(self):
        self.client.force_authenticate(user=self.seller_user)

        file = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'JPEG')
        file.name = 'test_photo.jpg'
        file.seek(0)
        photo_file = SimpleUploadedFile(file.name, file.read(), content_type='image/jpeg')

        url = reverse(
            'auto-salon-listing-add-photo-to-listing',
            kwargs={'pk': self.active_listing.id}
        )
        data = {'photo': photo_file}

        response = self.client.put(url, data, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.active_listing.refresh_from_db()
        photo_name = self.active_listing.photo.name
        self.assertTrue(photo_name.startswith(f'listings/{self.active_listing.id}/'))
        self.assertTrue(photo_name.endswith('.jpg'))

    def test_create_listing_with_bad_words_sets_inactive(self):
        self.client.force_authenticate(user=self.seller_user)

        Forbiddenwords.objects.create(word='badword1')
        Forbiddenwords.objects.create(word='badword2')

        url = reverse('auto-salon-listing-create')

        data = {
            'brand_id': self.brand.id,
            'car_model_id': self.car_model.id,
            'year': 2022,
            'country': 'Testcountry',
            'region': 'Testregion',
            'city': 'Testcity',
            'price': 15000,
            'currency': 'USD',
            "exchange_rate_used": "2024-01-01",
            'description': 'This listing contains badword1 and badword2',
            "auto_salon": self.auto_salon.id
        }

        response1 = self.client.post(url, data, format='json')
        self.assertEqual(response1.status_code, 400)

        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, 400)

        response3 = self.client.post(url, data, format='json')
        self.assertEqual(response3.status_code, 400)

        listing = AutoSalonListingModel.objects.latest('id')
        self.assertEqual(listing.description, data['description'])
        self.assertFalse(listing.is_active)
        self.assertEqual(listing.bad_word_attempts, 3)

    def test_admin_can_get_inactive_listings(self):
        url = reverse('auto-salon-listing-inactive')
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json().get('data', [])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.inactive_listing.id)

    def test_admin_can_delete_inactive_listing(self):
        url = reverse(
            'auto-salon-listing-delete-inactive',
            kwargs={'pk': self.inactive_listing.id}
        )
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(AutoSalonListingModel.objects.filter(pk=self.inactive_listing.id).exists())

    def test_non_admin_cannot_get_inactive_listings(self):
        url = reverse('auto-salon-listing-inactive')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_delete_inactive_listing(self):
        url = reverse(
            'auto-salon-listing-delete-inactive',
            kwargs={'pk': self.inactive_listing.id}
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



