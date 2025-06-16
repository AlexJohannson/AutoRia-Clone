from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.user.filter import UserFilter
from apps.user.models import ProfileModel

UserModel = get_user_model()

class UserFilterTestCase(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(email='userone@test.com', password='password')

        self.user1.profile = ProfileModel.objects.create(
            user=self.user1,
            name="Alex",
            surname="Johnson",
            age=30,
            house=5,
            street="First Street",
            city="Kyiv",
            region="Kyivska",
            country="Ukraine",
            gender="Male"
        )

        self.user2 = UserModel.objects.create_user(email='usertwo@test.com', password='password')

        self.user2.profile = ProfileModel.objects.create(
            user=self.user2,
            name="Bob",
            surname="Smith",
            age=45,
            house=10,
            street="Main Road",
            city="Lviv",
            region="Lvivska",
            country="Ukraine",
            gender="Female"
        )

    def test_lt_house_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'lt_house': 6}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_gt_house_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'gt_house': 6}, queryset=queryset).qs
        self.assertIn(self.user2, filtered)
        self.assertNotIn(self.user1, filtered)

    def test_age_filter(self):
        queryset = UserModel.objects.select_related("profile").all()
        filtered = UserFilter({'lt_age': 40, 'gt_age': 25}, queryset=queryset).qs
        filtered.values_list("profile__age", flat=True)
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_icontains_name_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'icontains_name': 'Alex'}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_icontains_surname_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'icontains_surname': 'Smith'}, queryset=queryset).qs
        self.assertIn(self.user2, filtered)
        self.assertNotIn(self.user1, filtered)

    def test_icontains_street_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'icontains_street': 'First'}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_icontains_city_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'icontains_city': 'Kyiv'}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_icontains_region_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'icontains_region': 'Kyivska'}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_icontains_country_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'icontains_country': 'Ukraine'}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertIn(self.user2, filtered)

    def test_gender_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'gender': 'Male'}, queryset=queryset).qs
        self.assertIn(self.user1, filtered)
        self.assertNotIn(self.user2, filtered)

    def test_ordering_filter(self):
        queryset = UserModel.objects.all()
        filtered = UserFilter({'order': 'profile__id'}, queryset=queryset).qs
        self.assertEqual(list(filtered), [self.user1, self.user2])







