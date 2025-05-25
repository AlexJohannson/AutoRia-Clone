from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_delete_auto_salon_task(email, name, auto_salon_name, location):
    EmailService.send_email(
        to=email,
        template_name='delete_auto_salon.html',
        context={
            'name': name,
            'auto_salon_name': auto_salon_name,
            'location': location,
        },
        subject='Auto Salon Deleted'
    )