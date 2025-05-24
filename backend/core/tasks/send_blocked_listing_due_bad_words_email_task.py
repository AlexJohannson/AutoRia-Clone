from configs.celery import app
from core.services.email_service import EmailService

from apps.listings.models import ListingSellersModel
from apps.user.models import UserModel


@app.task
def send_blocked_listing_due_bad_words_email_task(listings_id):
    try:
        listing = ListingSellersModel.objects.get(id=listings_id)
    except ListingSellersModel.DoesNotExist:
        return

    admins = UserModel.objects.filter(is_staff=True).exclude(email=None)

    for admin in admins:
        if not admin.email:
            continue

        EmailService.send_email.delay(
            to=admin.email,
            template_name='blocket_listing.html',
            context={
                'listing_id': listing.id,
                'seller_name': listing.seller.user.profile.name,
                'description': listing.description,
            },
            subject='Blocked Listing due to obscene language',
        )


