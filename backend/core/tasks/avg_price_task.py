from django.db.models import Avg

from configs.celery import app

from apps.listings.models import ListingSellersModel


@app.task(name='core.tasks.avg_price_task')
def avg_price_task():
    listings = ListingSellersModel.objects.filter(is_active=True, seller__premium_account__isnull=False)

    for listing in listings:
        city_avg = ListingSellersModel.objects.filter(
            city=listing.city, is_active=True
        ).aggregate(Avg('price'))['price__avg']

        region_avg = ListingSellersModel.objects.filter(
            region=listing.region, is_active=True
        ).aggregate(Avg('price'))['price__avg']

        country_avg = ListingSellersModel.objects.filter(
            country=listing.country, is_active=True
        ).aggregate(Avg('price'))['price__avg']

        listing.avg_city_price = city_avg if city_avg else 0.0
        listing.avg_region_price = region_avg if region_avg else 0.0
        listing.avg_country_price = country_avg if country_avg else 0.0

        listing.save(update_fields=['avg_city_price', 'avg_region_price', 'avg_country_price'])



