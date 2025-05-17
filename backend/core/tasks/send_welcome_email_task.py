from configs.celery import app
from core.services.email_service import EmailService

from apps.user.models import UserModel


@app.task
def send_welcome_email_task(user_id):
    try:
        user = UserModel.objects.select_related('profile').get(id=user_id)
    except UserModel.DoesNotExist:
        return

    EmailService.send_email(
        to=user.email,
        template_name='welcome.html',
        context={'name': user.profile.name},
        subject='Welcome'
    )
