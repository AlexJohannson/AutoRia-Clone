from configs.celery import app
from core.services.email_service import EmailService


@app.task
def send_premium_activate_email_task(email, name):
    EmailService.send_email(
        to=email,
        template_name='create_premium_account.html',
        context={'name': name},
        subject='Premium Activate'
    )