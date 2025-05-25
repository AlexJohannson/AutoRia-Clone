from configs.celery import app
from core.services.email_service import EmailService

from apps.auto_salon_listings.models import AutoSalonListingModel
from apps.user.models import UserModel


@app.task
def send_blocked_auto_salon_listing_email_task(auto_salon_id):
    try:
        listing = AutoSalonListingModel.objects.get(id=auto_salon_id)
    except AutoSalonListingModel.DoesNotExist:
        return 

    admins = UserModel.objects.filter(is_staff=True).exclude(email=None)

    for admin in admins:
        if not admin.email:
            continue

        EmailService.send_email(
            to=admin.email,
            template_name='blocked_auto_salon_listing.html',
            context={
                'listing_id': listing.id,
                'auto_salon_name': listing.auto_salon.name,
                'description': listing.description,
            },
            subject='Blocked Auto Salon Listing due obscene language',

        )
    