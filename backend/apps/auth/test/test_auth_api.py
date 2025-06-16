from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.auth.views import ActivateUserView, RecoveryPasswordView, RecoveryRequestView, SocketTokenView, UserRoleView
from apps.user.models import ProfileModel, UserModel


class AuthIntegrationTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123',
            is_active=False
        )
        self.user_profile = ProfileModel.objects.create(
            user=self.user,
            name='Test',
            surname='User',
            age=25,
            house=10,
            street='Test Street',
            city='Test City',
            region='Test Region',
            country='Test Country',
            gender='Male'
        )

    @patch('apps.auth.views.JWTService.verify_token')
    def test_activate_user(self, mock_verify_token):
        mock_verify_token.return_value = self.user

        url = reverse('auth_activate', kwargs={'token': 'dummy-token'})
        request = self.factory.patch(url)
        response = ActivateUserView.as_view()(request, token='dummy-token')

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    @patch('apps.auth.views.EmailService.recovery')
    def test_recovery_request_view(self, mock_email_service):
        url = reverse('auth_recovery')
        request = self.factory.post(url, {'email': self.user.email})
        force_authenticate(request, user=self.user)

        response = RecoveryRequestView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Details'], 'Link send to email')
        mock_email_service.assert_called_once()

    @patch('apps.auth.views.JWTService.verify_token')
    def test_recovery_password_view(self, mock_verify_token):
        mock_verify_token.return_value = self.user

        url = reverse('auth_recovery_password', kwargs={'token': 'dummy-token'})
        request = self.factory.post(url, {'password': 'NewSecurePassword123'})
        force_authenticate(request, user=self.user)

        response = RecoveryPasswordView.as_view()(request, token='dummy-token')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecurePassword123'))

    @patch('apps.auth.views.JWTService.create_token')
    def test_socket_token_view(self, mock_create_token):
        mock_create_token.return_value = 'dummy-socket-token'

        url = reverse('socket_token')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = SocketTokenView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], 'dummy-socket-token')

    def test_user_role_view(self):
        url = reverse('user_site_role')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        response = UserRoleView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_staff', response.data)
        self.assertIn('is_user', response.data)
        self.assertIn('is_seller', response.data)
        self.assertIn('is_auto_salon_member', response.data)

        self.assertFalse(response.data['is_staff'])
        self.assertFalse(response.data['is_seller'])
        self.assertFalse(response.data['is_auto_salon_member'])
        self.assertFalse(response.data['is_user'])

