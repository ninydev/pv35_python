# Используем минималистичный образ Python
FROM python:3.14-slim

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости (создадим requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код и страницу
COPY main.py .
COPY chat_client.html .

# Открываем порт
EXPOSE 5555

# Запускаем
CMD ["python", "main.py"]