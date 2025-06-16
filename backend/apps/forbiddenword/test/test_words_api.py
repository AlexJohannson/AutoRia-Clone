from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.forbiddenword.models import Forbiddenwords
from apps.user.models import UserModel

UserModel = get_user_model()

class ForbiddenWordsAPITest(APITestCase):
    def setUp(self):
        self.admin_user = UserModel.objects.create_user(
            email='admin@test.test',
            password='adminpass',
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        self.word = Forbiddenwords.objects.create(word='testword')

        self.list_url = reverse('forbidden_word-create')
        self.detail_url = reverse('forbidden_word-retrieve', kwargs={'pk': self.word.pk})

    def test_get_forbidden_words_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('data', [])
        self.assertTrue(any(w['word'] == 'testword' for w in data))

    def test_create_forbidden_word(self):
        data = {'word': 'newbadword'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['word'], 'newbadword')
        self.assertEqual(Forbiddenwords.objects.count(), 2)

    def test_get_forbidden_word_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'testword')

    def test_update_forbidden_word_put(self):
        data = {'word': 'updatedword'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'updatedword')
        self.word.refresh_from_db()
        self.assertEqual(self.word.word, 'updatedword')

    def test_partial_update_forbidden_word_patch(self):
        data = {'word': 'patchedword'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'patchedword')
        self.word.refresh_from_db()
        self.assertEqual(self.word.word, 'patchedword')

    def test_delete_forbidden_word(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Forbiddenwords.objects.filter(pk=self.word.pk).exists())


    def test_permission_denied_for_non_admin(self):
        user = UserModel.objects.create_user(email='user@test.user', password='userpass')
        client = APIClient()


        response = client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


        client.force_authenticate(user=user)

        response = client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.post(self.list_url, {'word': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.put(self.detail_url, {'word': 'x'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
