from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_listing_deleted_email_task(email, name, brand, car_model, price):
    EmailService.send_email(
        to=email,
        template_name='listing_deleted.html',
        context={
            'name': name,
            'brand': brand,
            'car_model': car_model,
            'price': price,
        },
        subject='Listing Deleted'
    )