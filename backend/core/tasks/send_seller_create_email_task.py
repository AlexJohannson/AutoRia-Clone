from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_seller_create_email_task(email, name):
    EmailService.send_email(
        to=email,
        template_name='seller_create.html',
        context={'name': name},
        subject='Seller Create'
    )