from django.test import TestCase

from apps.auto_salon.models import AutoSalonModel
from apps.invitation_to_auto_salon.models import JoinRequestModel
from apps.user.models import UserModel


class JoinRequestModelTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(email="test@example.com", password="testpassword")

        self.auto_salon = AutoSalonModel.objects.create(
            name="Test Salon",
            location="Test Location",
            user=self.user
        )

    def test_create_join_request_seller(self):
        join_request = JoinRequestModel.objects.create(
            user=self.user,
            auto_salon=self.auto_salon,
            role='seller',
            status='pending'
        )

        self.assertEqual(join_request.user, self.user)
        self.assertEqual(join_request.auto_salon, self.auto_salon)
        self.assertEqual(join_request.role, 'seller')
        self.assertEqual(join_request.status, 'pending')


    def test_invalid_status_choice_seller(self):
        with self.assertRaises(Exception):
            JoinRequestModel.objects.create(
                user=self.user,
                auto_salon=self.auto_salon,
                role='seller',
                status='invalid_status'
            )

    def test_create_join_request_admin(self):
        join_request = JoinRequestModel.objects.create(
            user=self.user,
            auto_salon=self.auto_salon,
            role='admin',
            status='pending'
        )

        self.assertEqual(join_request.user, self.user)
        self.assertEqual(join_request.auto_salon, self.auto_salon)
        self.assertEqual(join_request.role, 'admin')
        self.assertEqual(join_request.status, 'pending')


    def test_invalid_status_choice_admin(self):
        with self.assertRaises(Exception):
            JoinRequestModel.objects.create(
                user=self.user,
                auto_salon=self.auto_salon,
                role='admin',
                status='invalid_status'
            )
    def test_create_join_request_mechanic(self):
        join_request = JoinRequestModel.objects.create(
            user=self.user,
            auto_salon=self.auto_salon,
            role='mechanic',
            status='pending'
        )

        self.assertEqual(join_request.user, self.user)
        self.assertEqual(join_request.auto_salon, self.auto_salon)
        self.assertEqual(join_request.role, 'mechanic')
        self.assertEqual(join_request.status, 'pending')


    def test_invalid_status_choice_mechanic(self):
        with self.assertRaises(Exception):
            JoinRequestModel.objects.create(
                user=self.user,
                auto_salon=self.auto_salon,
                role='mechanic',
                status='invalid_status'
            )


    def test_invalid_role_choice(self):
        with self.assertRaises(Exception):
            JoinRequestModel.objects.create(
                user=self.user,
                auto_salon=self.auto_salon,
                role='invalid_role',
                status='pending'
            )
