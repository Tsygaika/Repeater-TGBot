FROM python:3.9-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Selenium
RUN pip install selenium

# Копирование вашего скрипта
COPY  .  /app
# Установка рабочей директории
WORKDIR /app
RUN  pip  install  -r  requirements.txt
# Запуск скрипта
CMD ["python", "main.py"]
