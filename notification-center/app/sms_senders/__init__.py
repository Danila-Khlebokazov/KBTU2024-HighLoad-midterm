from .twilio import send_sms as send_sms_twilio

SMS_SENDERS = {
    "twilio": send_sms_twilio,
}
