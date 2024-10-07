import os

from celery import Celery
from dotenv import load_dotenv

from .sms_senders import twilio

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://rabbitmq:rabbitmq@localhost:5672//")

celery_app = Celery("notification_center", broker=CELERY_BROKER_URL)


@celery_app.task(bind=True, name="send_notification_task")
def send_notification_task(self, data):
    phone_numbers = data.get("phone_numbers", [])
    message = data.get("message", "")
    sender = data.get("sender", "twilio")

    if sender == "twilio":
        sender_func = twilio.send_sms
    else:
        raise ValueError(f"Unsupported sender: {sender}")

    successes = []
    failures = []

    for number in phone_numbers:
        try:
            sender_func(number, message)
            successes.append(number)
        except Exception as e:
            failures.append({"number": number, "error": str(e)})

    return {"successes": successes, "failures": failures}
