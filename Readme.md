# Курсовая работа №6 по блоку "Django".

Проект представляет собой сервис email рассылок.

## Установка

1. Клонируйте репозиторий:
   ```bash
    git clone https://github.com/SerjMonstrX/course_work_django.git
   
2. Установите зависимости, используя Poetry:

       poetry install

3. Настройте PostgreSQL:
Создайте базу данных PostgreSQL с именем cw_django.

4. Примените миграции:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
   
5. Наполните БД:
   ```bash
   python manage.py fill_db

## Структура

Приложение mailing содержит модели для рассылок, сообщений и клиентов.

Приложение users содержит реализацию модели юзера.

Приложение blog реализует блог

## Запуск рассылок

Для ОС Windows запуск периодических задач рассылок реализован с помощью Celery.
Для начала рассылок запустите Worker и Celery beat.
   ```bash
   celery -A config worker -P eventlet -l info
   celery -A config.celery beat -l info

