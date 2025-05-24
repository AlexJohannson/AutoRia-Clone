from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_auto_salon_create_email_task(email, name, auto_salon_name, location):
    EmailService.send_email(
        to=email,
        template_name='create_auto_salon.html',
        context={
            'name': name,
            'name_auto_salon': auto_salon_name,
            'location': location,
        },
        subject='Create Auto Salon',
    )