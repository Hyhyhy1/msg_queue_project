# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Указываем порт, который будет использовать приложение
EXPOSE 8000

# Запускаем FastAPI 
CMD ["uvicorn", "gateway_app.gateway:app", "--host", "0.0.0.0", "--port", "8000"]