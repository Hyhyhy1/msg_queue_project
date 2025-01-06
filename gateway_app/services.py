import pika
import json
import logging
from pydantic import ValidationError
from gateway_app.schemas import EmailNotification, SMSNotification, TelegramNotification
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "notification_exchange")



def send_notification(notification):

    try:
        # Валидация сообщения
        if notification.type == "email":
            validated_notification = EmailNotification(**notification.dict())
            routing_key = 'email'
        elif notification.type == "sms":
            validated_notification = SMSNotification(**notification.dict())
            routing_key = 'sms'
        elif notification.type == "telegram":
            validated_notification = TelegramNotification(**notification.dict())
            routing_key = 'telegram'
        else:
            raise ValueError(f"Unknown notification type: {notification.type}")

        
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                virtual_host='/'
            )
        )
        channel = connection.channel()

        
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)
        channel.queue_declare(queue='email_queue', durable=True)
        channel.queue_declare(queue='sms_queue', durable=True)
        channel.queue_declare(queue='telegram_queue', durable=True)

        channel.queue_bind(exchange=EXCHANGE_NAME, queue='email_queue', routing_key='email')
        channel.queue_bind(exchange=EXCHANGE_NAME, queue='sms_queue', routing_key='sms')
        channel.queue_bind(exchange=EXCHANGE_NAME, queue='telegram_queue', routing_key='telegram')

        
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(validated_notification.model_dump()),
            properties=pika.BasicProperties(
                delivery_mode=2,  
            ),
        )
        logger.info(f" [x] Sent {notification.type} notification to {notification.recipient}")

        
        connection.close()
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise ValueError(str(e))
    except pika.exceptions.AMQPError as e:
        logger.error(f"RabbitMQ error: {e}")
        raise ValueError(f"Failed to send notification: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(str(e))