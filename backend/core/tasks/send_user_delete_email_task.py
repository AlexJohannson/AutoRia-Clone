from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_user_delete_email_task(email, name):
    EmailService.send_email(
        to=email,
        template_name='delete_email.html',
        context={'name': name},
        subject='Account deleted',
    )
