import pika
import json
from pydantic import ValidationError
from schemas import EmailNotification, SMSNotification, PushNotification

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Объявление exchange
channel.exchange_declare(exchange='notification_exchange', exchange_type='direct')

# Объявление очередей и binding
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='push_queue')

channel.queue_bind(exchange='notification_exchange', queue='email_queue', routing_key='email')
channel.queue_bind(exchange='notification_exchange', queue='sms_queue', routing_key='sms')
channel.queue_bind(exchange='notification_exchange', queue='push_queue', routing_key='push')

def send_notification(notification):
    try:
        # Валидация сообщения
        if notification.type == "email":
            validated_notification = EmailNotification(**notification.dict())
            routing_key = 'email'
        elif notification.type == "sms":
            validated_notification = SMSNotification(**notification.dict())
            routing_key = 'sms'
        elif notification.type == "push":
            validated_notification = PushNotification(**notification.dict())
            routing_key = 'push'
        else:
            raise ValueError(f"Unknown notification type: {notification.type}")

        # Отправка сообщения
        channel.basic_publish(
            exchange='notification_exchange',
            routing_key=routing_key,
            body=json.dumps(validated_notification.model_dump())
        )
        print(f" [x] Sent {notification.type} notification to {notification.recipient}")
    except ValidationError as e:
        raise ValueError(str(e))
    except ValueError as e:
        raise ValueError(str(e))