from configs import settings
from configs.celery import app
from core.services.email_service import EmailService

from apps.listings.models import ListingSellersModel


@app.task
def send_blocked_listing_due_bad_words_email_task(listings_id):

    try:
        listings = ListingSellersModel.objects.get(id=listings_id)
    except ListingSellersModel.DoesNotExist:
        return

    admin_email = settings.ADMIN_EMAIL


    EmailService.send_email.delay(
        to=admin_email,
        template_name='blocket_listing.html',
        context={
        'listing_id': listings.id,
        'seller_name': listings.seller.user.profile.name,
        'description': listings.description,
    },
        subject='Blocket Listing due to obscene language',
    )
