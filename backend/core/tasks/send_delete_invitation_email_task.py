from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_delete_invitation_email_task(email, name, auto_salon_name,):
    EmailService.send_email(
        to=email,
        template_name='delete_invitation.html',
        context={
            'name': name,
            'auto_salon_name': auto_salon_name,
        },
        subject='Delete Invitation',
    )