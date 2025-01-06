from fastapi import APIRouter, HTTPException
from gateway_app.schemas import EmailNotification, SMSNotification, TelegramNotification
from gateway_app.services import send_notification

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

@router.post("/send_telegram_msg/")
async def send_telegram_msg(notification: TelegramNotification):
    try:
        send_notification(notification)
        return {"message": "Telegram notification sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))