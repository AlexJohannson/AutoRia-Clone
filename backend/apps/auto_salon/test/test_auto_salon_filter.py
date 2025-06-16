from django.test import TestCase

from apps.auto_salon.filter import AutoSalonFilter
from apps.auto_salon.models import AutoSalonModel
from apps.user.models import UserModel


class AutoSalonFilterTest(TestCase):
    def setUp(self):
        self.salon_data = [
            {'name': 'Fast Cars', 'location': 'Kyiv'},
            {'name': 'Luxury Wheels', 'location': 'Lviv'},
            {'name': 'Budget Autos', 'location': 'Kyiv'},
            {'name': 'Elite Motors', 'location': 'Odesa'},
        ]

        for i, data in enumerate(self.salon_data):
            user = UserModel.objects.create(email=f'user{i}@test.com', is_active=True)
            user.set_password('testpass')
            user.save()
            AutoSalonModel.objects.create(user=user, **data)

    def apply_filter(self, data):
        queryset = AutoSalonModel.objects.all()
        return AutoSalonFilter(data=data, queryset=queryset).qs

    def test_icontains_name_filter(self):
        filtered = self.apply_filter({'icontains_name': 'luxury'})
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().name, 'Luxury Wheels')

    def test_icontains_location_filter(self):
        filtered = self.apply_filter({'icontains_location': 'kyiv'})
        self.assertEqual(filtered.count(), 2)
        names = list(filtered.values_list('name', flat=True))
        self.assertIn('Fast Cars', names)
        self.assertIn('Budget Autos', names)

    def test_ordering_by_name(self):
        filtered = self.apply_filter({'order': 'name'})
        names = list(filtered.values_list('name', flat=True))
        self.assertEqual(names, sorted(names))

    def test_ordering_by_location_desc(self):
        filtered = self.apply_filter({'order': '-location'})
        locations = list(filtered.values_list('location', flat=True))
        self.assertEqual(locations, sorted(locations, reverse=True))

