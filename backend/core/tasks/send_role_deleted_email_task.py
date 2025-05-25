from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_role_deleted_email_task(email, name, auto_salon_name, role):
    EmailService.send_email(
        to=email,
        template_name='deleted_role.html',
        context={
            'name': name,
            'auto_salon_name': auto_salon_name,
            'role': role,
        },
        subject='Deleted Role From Auto Salon',
    )