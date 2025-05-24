from datetime import timedelta

from django.utils.timezone import now

from core.services.exchange_servise import get_exchange_rates

from apps.listings.models import ListingSellersModel


def calculate_prices(price, currency):

    rates = get_exchange_rates()

    if currency == 'USD':
        return price, round(price * rates['USD_EUR'], 2), round(price * rates['USD_UAH'], 2)
    elif currency == 'EUR':
        return round(price * rates['EUR_USD'], 2), price, round(price * rates['EUR_UAH'], 2)
    elif currency == 'UAH':
        return round(price / rates['USD_UAH'], 2), round(price / rates['EUR_UAH'], 2), price

    return 0, 0, 0

def check_seller_listing_limit(seller):

    if hasattr(seller, 'base_account'):
        listing_count = ListingSellersModel.objects.filter(seller=seller).count()
        if listing_count >= 1:
            return False, "Base account can only create one listing!"
    return True, None


def update_listing_views(listing):
    today = now()

    if hasattr(listing, 'seller') and hasattr(listing.seller, 'premium_account') or hasattr(listing, 'auto_salon'):
        listing.views += 1


        if listing.last_view_date and listing.last_view_date.date() == today.date():
            listing.daily_views += 1
        else:
            listing.daily_views = 1

        if listing.last_view_date and listing.last_view_date >= today - timedelta(days=7):
            listing.weekly_views += 1
        else:
            listing.weekly_views = 1

        if listing.last_view_date and listing.last_view_date >= today - timedelta(days=30):
            listing.monthly_views += 1
        else:
            listing.monthly_views = 1

        listing.last_view_date = today
        listing.save(update_fields=['views', 'daily_views', 'weekly_views', 'monthly_views', 'last_view_date'])


