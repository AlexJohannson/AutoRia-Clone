from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_user_blocked_email_task(email, name):
    EmailService.send_email(
        to=email,
        template_name='user_blocked.html',
        context={'name': name},
        subject='Account Blocked',
    )