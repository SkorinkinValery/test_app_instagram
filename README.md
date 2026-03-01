# Instagram Sync & Comment Manager

Простое веб-приложение на Django + Django REST Framework, которое:

- синхронизирует посты из Instagram Business/Creator аккаунта в локальную PostgreSQL базу
- позволяет добавлять комментарии под постами через API
- возвращает список постов с пагинацией (cursor-based)

Проект создан в рамках тестового задания на позицию Junior Backend Developer.

## Стек технологий

- Python 3.10+
- Django 5.x / 6.x
- Django REST Framework
- PostgreSQL
- requests (для работы с Instagram Graph API)
- python-dotenv (переменные окружения)
- Docker + docker-compose (опционально)

## Основные возможности

- `POST /api/sync/` — полная синхронизация всех постов аккаунта (с пагинацией)
- `GET /api/posts/` — список всех постов из базы с курсорной пагинацией
- `POST /api/posts/<id>/comment/` — добавление комментария под постом (через Instagram API + сохранение в БД)

## Как запустить проект локально (без Docker)

1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-логин/Test-task-Junior-Backend.git
cd Test-task-Junior-Backend

Создайте и активируйте виртуальное окружение

Bashpython -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

Установите зависимости

Bashpip install -r requirements.txt

Создайте файл .env в корне проекта

envSECRET_KEY=ваш_секретный_ключ_из_settings
INSTAGRAM_ACCESS_TOKEN=IGAAhmq5x1EXlBZAGJjc3JRMUk... (ваш токен из Meta App Dashboard)

Выполните миграции и создайте суперпользователя

Bashpython manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Запустите сервер

Bashpython manage.py runserver
Приложение будет доступно по адресу: http://127.0.0.1:8000/
Доступные эндпоинты

POST /api/sync/ → синхронизировать посты
GET /api/posts/ → список постов (с пагинацией ?limit= и cursor)
POST /api/posts/<id>/comment/ → добавить комментарий
Body (x-www-form-urlencoded):
message=Ваш текст комментария

Как получить Instagram Access Token

Зайдите в https://developers.facebook.com/apps/
Создайте приложение типа Business
Добавьте продукт Instagram Graph API
В разделе Instagram → API setup подключите свой Business/Creator аккаунт
Сгенерируйте User Access Token (long-lived) прямо в дашборде
Скопируйте токен и вставьте в .env → INSTAGRAM_ACCESS_TOKEN=...

Важно: для создания комментариев нужен scope instagram_manage_comments (часто требуется App Review).
Запуск в Docker (рекомендуется)
Bashdocker-compose up --build
После запуска приложение доступно на http://localhost:8000/
