# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем необходимые пакеты Python
RUN pip install pillow

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы в контейнер
COPY . /app

# Запускаем скрипт
CMD ["python", "main.py"]
