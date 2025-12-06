# 1. Берем легкую версию Python
FROM python:3.9-slim

# 2. Создаем папку внутри контейнера
WORKDIR /app

# 3. Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь твой код в контейнер
COPY . .

# 5. Открываем порт 5000
EXPOSE 5000

# 6. Запускаем приложение через Gunicorn (4 "работника" для скорости)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]