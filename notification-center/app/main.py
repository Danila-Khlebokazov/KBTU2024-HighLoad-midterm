from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from .tasks import send_notification_task

app = FastAPI(title="Notification Center API")


class NotificationRequest(BaseModel):
    phone_numbers: List[str] = Field(..., example=["+1234567890", "+0987654321"])
    message: str = Field(..., example="Your verification code is 123456")
    sender: str = Field(..., example="twilio")  # e.g., twilio, nexmo

    @field_validator("phone_numbers")
    def validate_phone_numbers(cls, v):
        if not v:
            raise ValueError("At least one phone number must be provided")
        for number in v:
            if not number.startswith("+") or not number[1:].isdigit():
                raise ValueError(f"Invalid phone number format: {number}")
        return v


@app.post("/send-notification", summary="Send SMS Notifications")
async def send_notification(notification: NotificationRequest):
    try:
        task = send_notification_task.delay(notification.dict())
        return {"task_id": task.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
