from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_join_request_email_task(email, name, role, auto_salon_name, location, created_at):
    EmailService.send_email(
        to=email,
        template_name='join_request_email.html',
        context={
            'name': name,
            'role': role,
            'auto_salon_name': auto_salon_name,
            'location': location,
            'created_at': created_at,
        },
        subject='Join Request To Auto Salon',
    )