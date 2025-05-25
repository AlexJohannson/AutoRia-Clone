from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_deleted_auto_salon_listing_email_task(email, name, brand, car_model, price):
    EmailService.send_email(
        to=email,
        template_name='auto_salon_listing_deleted.html',
        context={
            'name': name,
            'brand': brand,
            'car_model': car_model,
            'price': price,
        },
        subject='Auto Salon Listing Deleted',
    )