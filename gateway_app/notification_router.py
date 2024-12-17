from fastapi import APIRouter, HTTPException
from schemas import EmailNotification, SMSNotification, PushNotification
from services import send_notification

router = APIRouter()

@router.post("/send_email/")
async def send_email(notification: EmailNotification):
    try:
        send_notification(notification)
        return {"message": "Email notification sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/send_sms/")
async def send_sms(notification: SMSNotification):
    try:
        send_notification(notification)
        return {"message": "SMS notification sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/send_push/")
async def send_push(notification: PushNotification):
    try:
        send_notification(notification)
        return {"message": "Push notification sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))