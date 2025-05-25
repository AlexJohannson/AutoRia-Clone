from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_join_request_approved_email_task(emai, name, auto_salon_name, location, updated_at):
    EmailService.send_email(
        to=emai,
        template_name='join_request_approved_email.html',
        context={
            'name': name,
            'auto_salon_name': auto_salon_name,
            'location': location,
            'updated_at': updated_at,
        },
        subject='Role Approved in Auto Salon',
    )