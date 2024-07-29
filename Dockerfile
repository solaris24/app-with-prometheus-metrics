# Стадия 1: Сборка зависимостей
FROM python:3.9 AS builder

# Устанавливаем зависимости проекта
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Стадия 2: Создание итогового образа
FROM python:3.9-slim

# Копируем зависимости из стадии 1
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Копируем исходный код приложения
COPY . /app
WORKDIR /app

# Устанавливаем рабочую директорию и запускаем приложение
EXPOSE 5000
CMD ["python", "app.py"]