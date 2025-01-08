# Итоговый проект по курсу "Проектирование микросервисов"

Перед запускам создать файл .env со следующий содержанием:

SMTP_SERVER=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
FROM_EMAIL=

RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASSWORD=

TELEGRAM_BOT_TOKEN=

Для сборки запустить docker-compose up --build

Реализованы сервисы отправки сообщений на электронную почту и в telegram, бесплатных сервисов для отправки SmS сообщений я найти не смог.