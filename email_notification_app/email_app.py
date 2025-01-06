import pika
import json
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, recipient, msg.as_string())
        server.quit()
        logger.info(f"Email sent to {recipient}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        recipient = message['recipient']
        subject = "Notification"
        body = message['message']

        send_email(recipient, subject, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing message: {e}")


def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT")),
            credentials=pika.PlainCredentials(
                username=os.getenv("RABBITMQ_USER"),
                password=os.getenv("RABBITMQ_PASSWORD")
            )
        ))
        channel = connection.channel()


        channel.queue_declare(queue='email_queue', durable=True)


        channel.basic_consume(queue='email_queue', on_message_callback=callback)

        logger.info(' [*] Ожидание email сообщений. Для выхода нажмите CTRL+C')
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Ошибка при подключении к RabbitMQ: {e}")

if __name__ == '__main__':
    start_consumer()