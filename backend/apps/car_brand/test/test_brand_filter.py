from django.test import TestCase

from apps.car_brand.filter import CarBrandFilter
from apps.car_brand.models import CarBrandModel


class CarBrandFilterTest(TestCase):
    def setUp(self):
        CarBrandModel.objects.create(brand="Toyota")
        CarBrandModel.objects.create(brand="Ford")
        CarBrandModel.objects.create(brand="Tesla")
        CarBrandModel.objects.create(brand="Toyota Supra")

    def test_filter_brand_icontains(self):
        data = {'brand': 'toyota'}
        qs = CarBrandModel.objects.all()
        filtered = CarBrandFilter(data=data, queryset=qs)
        self.assertEqual(filtered.qs.count(), 2)
        brands = set(b.brand for b in filtered.qs)
        self.assertIn("Toyota", brands)
        self.assertIn("Toyota Supra", brands)

    def test_ordering_by_brand_asc(self):
        data = {'order': 'brand'}
        qs = CarBrandModel.objects.all()
        filtered = CarBrandFilter(data=data, queryset=qs)
        brands_ordered = list(filtered.qs.values_list('brand', flat=True))
        self.assertEqual(brands_ordered, sorted(brands_ordered))

    def test_ordering_by_brand_desc(self):
        data = {'order': '-brand'}
        qs = CarBrandModel.objects.all()
        filtered = CarBrandFilter(data=data, queryset=qs)
        brands_ordered = list(filtered.qs.values_list('brand', flat=True))
        self.assertEqual(brands_ordered, sorted(brands_ordered, reverse=True))
