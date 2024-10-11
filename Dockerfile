# Указываем базовый образ с Python 3.10
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем необходимые пакеты для Tkinter и X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libxft2 \
    libxext6 \
    libxrender1 \
    && apt-get clean

# Устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код в контейнер
COPY . .

# Команда запуска приложения
CMD ["python3", "main.py"]
