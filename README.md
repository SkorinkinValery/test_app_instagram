# Instagram Sync & Comment Manager

Простое веб-приложение на Django + Django REST Framework, которое:

- Синхронизирует посты из Instagram Business/Creator аккаунта в локальную PostgreSQL базу (с логикой upsert).
- Позволяет добавлять комментарии под постами через Instagram Graph API.
- Возвращает список постов с производительной курсорной пагинацией (cursor-based).

Проект создан в рамках тестового задания на позицию Junior Backend Developer (февраль–март 2026).

---

## Стек технологий

- Python 3.10+
- Django 5.x / 6.x
- Django REST Framework
- PostgreSQL
- requests (для работы с Instagram Graph API)
- python-dotenv (переменные окружения)
- Docker + docker-compose (опционально)

---

## Основные возможности

- POST /api/sync/ — полная синхронизация всех постов аккаунта (с автоматической обработкой пагинации API).
- GET /api/posts/ — список всех постов из базы с курсорной пагинацией (?limit=).
- POST /api/posts/<id>/comment/ — добавление комментария под постом (через Instagram API + сохранение в локальную БД).

Примечание по БД: При расчетах используется явное приведение типов для обеспечения floating point division. Для форматирования дат и времени в API применяется функция to_char с обязательным trim для удаления лишних пробелов.

---

## Как запустить проект локально (без Docker)

### 1. Клонируйте репозиторий
git clone https://github.com/onesimpleone/Test-task-Junior-Backend.git
cd Test-task-Junior-Backend

### 2. Создайте и активируйте виртуальное окружение
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

### 3. Установите зависимости
pip install -r requirements.txt

### 4. Создайте файл .env в корне проекта
SECRET_KEY=ваш_секретный_ключ
INSTAGRAM_ACCESS_TOKEN=IGAA... (ваш токен из Meta App Dashboard)
# Настройки БД (если не используете Docker)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

### 5. Выполните миграции и создайте суперпользователя
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

### 6. Запустите сервер
python manage.py runserver

Приложение будет доступно по адресу: http://127.0.0.1:8000/

---

## Запуск через Docker (рекомендуется)

docker-compose up --build

После запуска приложение доступно на http://localhost:8000/.

---

## Как получить Instagram Access Token

1. Зайдите в Facebook Developers Console (https://developers.facebook.com/apps/).
2. Создайте приложение типа Business.
3. Добавьте продукт Instagram Graph API.
4. В разделе Instagram -> API setup подключите свой Business/Creator аккаунт.
5. Сгенерируйте User Access Token (long-lived) прямо в дашборде.
6. Скопируйте токен и вставьте в .env параметр INSTAGRAM_ACCESS_TOKEN.

Важно: Для создания комментариев необходим scope instagram_manage_comments (обычно требует прохождения App Review для Advanced Access).
