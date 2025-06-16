from django.test import TestCase

from apps.auto_salon.models import AutoSalonModel
from apps.user.models import UserModel


class AutoSalonModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(email='testuser@example.com', is_active=True)
        self.user.set_password('testpassword')
        self.user.save()

        self.auto_salon = AutoSalonModel.objects.create(
            name='Fast Cars',
            location='Kyiv',
            user=self.user
        )

    def test_auto_salon_creation(self):
        self.assertEqual(self.auto_salon.name, 'Fast Cars')
        self.assertEqual(self.auto_salon.location, 'Kyiv')
        self.assertEqual(self.auto_salon.user, self.user)

    def test_auto_salon_str_method(self):
        self.assertEqual(str(self.auto_salon), 'Fast Cars (Kyiv)')

    def test_user_auto_salon_relationship(self):
        self.assertEqual(self.user.auto_salon, self.auto_salon)
