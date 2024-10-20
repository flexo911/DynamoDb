# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл requirements.txt і встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо файли додатку
COPY . .

# Вказуємо команду для запуску watcher, який буде відслідковувати зміни у Python файлах
CMD ["python", "watcher.py"]