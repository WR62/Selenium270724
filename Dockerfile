# Установка базового образа
FROM python:3.12.7-alpine

# Установка рабочего директория внутри контейнера
# Директорий будет создан если его не было
WORKDIR /knst

# Копирование зависимостей
# Для того чтобы не пересобирать их каждый раз при сборке образа
COPY requirements.txt .

# Установка зависимостей
RUN pip install -U pip
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта
COPY ./tests/*.py ./tests/
COPY ./pages/*.py ./pages/

# Запуск тестов
CMD ["pytest"]