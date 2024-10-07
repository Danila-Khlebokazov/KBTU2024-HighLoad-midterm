from config.celery import app as celery_app
from apps.authentication.models import User


def send_sms_to_user(user: User, message: str):
    celery_app.signature(
        "send_notification_task",
        kwargs={
            "data": {
                "phone_numbers": [user.phone_number],
                "message": message,
            }
        },
        queue="notification-center"
    ).delay()
