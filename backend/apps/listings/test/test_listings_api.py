from io import BytesIO

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework.test import APITestCase

from PIL import Image

from apps.car_brand.models import CarBrandModel
from apps.car_model.models import CarModelModel
from apps.forbiddenword.models import Forbiddenwords
from apps.listings.models import ListingSellersModel
from apps.sellers.models import SellersModel
from apps.user.models import ProfileModel, UserModel


class ListingApiTestCase(APITestCase):
    def setUp(self):
        ListingSellersModel.objects.all().delete()
        cache.clear()


        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='password123'
        )

        self.other_user = UserModel.objects.create_user(
            email='other@example.com',
            password='password456'
        )

        self.admin = UserModel.objects.create_user(
            email='admin@test.com',
            password='password',
            is_staff=True,
            is_superuser=True
        )


        self.profile = ProfileModel.objects.create(
            name='Test',
            surname='User',
            age=30,
            house=1,
            street='Main Street',
            city='TestCity',
            region='TestRegion',
            country='TestCountry',
            gender='male',
            user=self.user
        )

        self.other_profile = ProfileModel.objects.create(
            name='Other',
            surname='User',
            age=35,
            house=2,
            street='Other Street',
            city='OtherCity',
            region='OtherRegion',
            country='OtherCountry',
            gender='female',
            user=self.other_user
        )


        self.seller = SellersModel.objects.create(user=self.user)
        self.other_seller = SellersModel.objects.create(user=self.other_user)


        self.brand = CarBrandModel.objects.create(brand='TestBrand')
        self.car_model = CarModelModel.objects.create(
            car_model='TestModel',
            car_brand=self.brand
        )


        self.active_listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2020,
            country='TestCountry',
            region='TestRegion',
            city='TestCity',
            price=10000,
            currency='USD',
            description='Active listing',
            seller=self.seller,
            is_active=True,
        )


        self.inactive_listing = ListingSellersModel.objects.create(
            brand=self.brand,
            car_model=self.car_model,
            year=2019,
            country='TestCountry',
            region='TestRegion',
            city='TestCity',
            price=9000,
            currency='USD',
            description='Inactive listing',
            seller=self.seller,
            is_active=False,
        )

    def test_get_listings_returns_only_active(self):
        url = reverse('listing_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        results = data.get('data', [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.active_listing.id)

    def test_get_active_listing_detail_success(self):
        url = reverse('listing_detail', kwargs={'pk': self.active_listing.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.active_listing.id)

    def test_create_listing_success_by_seller(self):
        self.client.force_authenticate(user=self.seller.user)
        url = reverse('listing_list')

        data = {
            'brand_id': self.brand.id,
            'car_model_id': self.car_model.id,
            'year': 2021,
            'country': 'Testcountry',
            'region': 'Testregion',
            'city': 'Testcity',
            'price': 12000,
            'currency': 'USD',
            'description': 'Test listing without bad words',
            'seller': self.seller.id
        }

        response = self.client.post(url, data, format='json')


        self.assertEqual(response.status_code, 201)
        self.assertEqual(ListingSellersModel.objects.count(), 3)
        new_listing = ListingSellersModel.objects.latest('id')
        self.assertEqual(new_listing.seller, self.seller)
        self.assertTrue(new_listing.is_active)



    def test_get_inactive_listing_detail_not_found(self):
        url = reverse('listing_detail', kwargs={'pk': self.inactive_listing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_put_listing_by_owner_success(self):
        url = reverse('listing_detail', kwargs={'pk': self.active_listing.id})
        self.client.force_authenticate(user=self.user)

        data = {
            'description': 'Updated description',
            'brand_id': self.brand.id,
            'car_model_id': self.car_model.id,
            'year': 2020,
            'country': 'Testcountry',
            'region': 'Testregion',
            'city': 'Testcity',
            'price': 10000,
            'currency': 'USD',
            'seller': self.seller.id
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Updated description')

    def test_put_listing_by_other_user_forbidden(self):
        url = reverse('listing_detail', kwargs={'pk': self.active_listing.id})
        self.client.force_authenticate(user=self.other_user)

        data = {
            'description': 'Hacked!',
            'brand': self.brand.id,
            'car_model': self.car_model.id,
            'year': 2020,
            'country': 'Testcountry',
            'region': 'Testregion',
            'city': 'Testcity',
            'price': 10000,
            'currency': 'USD',
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_delete_listing_by_owner_success(self):
        url = reverse('listing_detail', kwargs={'pk': self.active_listing.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


    def test_delete_listing_by_other_user_forbidden(self):
        url = reverse('listing_detail', kwargs={'pk': self.active_listing.id})
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_add_photo_to_listing_success(self):
        self.client.force_authenticate(user=self.user)


        file = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'JPEG')
        file.name = 'test_photo.jpg'
        file.seek(0)
        photo_file = SimpleUploadedFile(file.name, file.read(), content_type='image/jpeg')

        url = reverse('add_photo', kwargs={'pk': self.active_listing.id})
        data = {'photo': photo_file}

        response = self.client.put(url, data, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.active_listing.refresh_from_db()
        photo_name = self.active_listing.photo.name
        self.assertTrue(photo_name.startswith(f'listings/{self.active_listing.id}/'))
        self.assertTrue(photo_name.endswith('.jpg'))

    def test_admin_can_get_inactive_listings(self):
        url = reverse('listing_inactive')
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json().get('data', [])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.inactive_listing.id)

    def test_admin_can_delete_inactive_listing(self):
        url = reverse('listing_inactive_delete',
                      kwargs={'pk': self.inactive_listing.id})
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(ListingSellersModel.objects.filter(pk=self.inactive_listing.id).exists())

    def test_non_admin_cannot_get_inactive_listings(self):
        url = reverse('listing_inactive')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_non_admin_cannot_delete_inactive_listing(self):
        url = reverse('listing_inactive_delete', kwargs={'pk': self.inactive_listing.id})
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)


    def test_create_listing_with_bad_words_sets_inactive(self):
        self.client.force_authenticate(user=self.seller.user)


        Forbiddenwords.objects.create(word='badword1')
        Forbiddenwords.objects.create(word='badword2')

        url = reverse('listing_list')

        data = {
            'brand_id': self.brand.id,
            'car_model_id': self.car_model.id,
            'year': 2022,
            'country': 'Testcountry',
            'region': 'Testregion',
            'city': 'Testcity',
            'price': 15000,
            'currency': 'USD',
            'description': 'This listing contains badword1 and badword2',
            'seller': self.seller.id
        }


        response1 = self.client.post(url, data, format='json')
        self.assertEqual(response1.status_code, 400)


        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, 400)


        response3 = self.client.post(url, data, format='json')
        self.assertEqual(response3.status_code, 400)

        listing = ListingSellersModel.objects.latest('id')
        self.assertEqual(listing.description, data['description'])
        self.assertFalse(listing.is_active)
        self.assertEqual(listing.bad_word_attempts, 3)








