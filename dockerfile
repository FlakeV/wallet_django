FROM python:3

# Устанавливаем переменную окружения PYTHONUNBUFFERED в 1, чтобы вывод был направлен прямо в терминал без буферизации
ENV PYTHONUNBUFFERED 1

# Создаем и переходим в рабочую директорию /app
RUN mkdir /app
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app/