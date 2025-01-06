import pika
import json
import logging
import asyncio
import threading
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

# Функция для отправки Telegram-уведомления
async def send_telegram_message(chat_id, message):
    try:
        await application.bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Сообщение отправлено в Telegram: {message}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

# Функция для обработки сообщений из очереди RabbitMQ
def consume_messages():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(
                username=RABBITMQ_USER,
                password=RABBITMQ_PASSWORD
            )
        ))
        channel = connection.channel()

        channel.queue_declare(queue='telegram_queue', durable=True)

        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                chat_id = message['recipient']
                telegram_message = message['message']

                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(send_telegram_message(chat_id, telegram_message))
                loop.close()

                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Ошибка обработки сообщения: {e}")

        channel.basic_consume(queue='telegram_queue', on_message_callback=callback)

        logger.info(' [*] Ожидание Telegram сообщений. Для выхода нажмите CTRL+C')
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Ошибка при подключении к RabbitMQ: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Ваш Chat ID: {chat_id}")

# Инициализация бота
application = Application.builder().token(BOT_TOKEN).build()

# Регистрация обработчика команды /start
application.add_handler(CommandHandler('start', start))

# Запуск RabbitMQ потребителя в отдельном потоке
def start_rabbitmq_consumer():
    consume_messages()

if __name__ == '__main__':
    if not BOT_TOKEN:
        logger.error("Токен бота не указан. Установите переменную окружения TELEGRAM_BOT_TOKEN.")
        exit(1)

    # Запуск RabbitMQ потребителя в отдельном потоке
    rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer)
    rabbitmq_thread.start()

    # Запуск бота в основном потоке
    application.run_polling()