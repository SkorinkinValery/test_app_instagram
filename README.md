Instagram Sync & Comment ManagerВеб-приложение на базе Django и Django REST Framework, предназначенное для автоматизации взаимодействия с постами Instagram Business/Creator аккаунтов. Проект реализует синхронизацию медиаконтента в локальную базу данных PostgreSQL и управление комментариями через Instagram Graph API.Разработано в рамках тестового задания на позицию Junior Backend Developer (февраль–март 2026).Технологический стекЯзык: Python 3.10+Фреймворк: Django 6.0.2 & Django REST FrameworkБаза данных: PostgreSQL (использование upsert для предотвращения дубликатов)Интеграции: Instagram Graph API (библиотека requests)Пагинация: CursorPagination (DRF) для эффективной работы с большими спискамиОкружение: python-dotenv, Docker & Docker ComposeОсновные возможностиСинхронизация (POST /api/sync/): Полная загрузка постов из Instagram в локальную БД. Поддерживает постраничную загрузку (next pagination) и обновление существующих записей по ig_id.Просмотр данных (GET /api/posts/): Список всех сохраненных постов с использованием курсорной пагинации (?limit=).Управление комментариями (POST /api/posts/<id>/comment/): Добавление комментария к посту через API с последующим сохранением в локальную базу.Примечание по БД: При расчетах в Postgres используется явное приведение типов для обеспечения floating point division. Для форматирования дат в API применяется функция to_char с обязательным использованием trim для удаления лишних пробелов.Как запустить проектВариант 1: Через Docker (рекомендуется)Убедитесь, что у вас установлен Docker и Docker Compose.Запустите сборку и контейнеры:Bashdocker-compose up --build
Приложение будет доступно по адресу: http://localhost:8000/Вариант 2: Локальный запуск (без Docker)1. Подготовка окруженияBashgit clone https://github.com/ваш-логин/Test-task-Junior-Backend.git
cd Test-task-Junior-Backend

python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
2. Конфигурация (.env)Создайте файл .env в корне проекта и заполните его:Фрагмент кодаSECRET_KEY=django-insecure-your-key-here
INSTAGRAM_ACCESS_TOKEN=IGAA...ваш_токен...
# Если используете локальную БД, укажите параметры подключения:
DB_NAME=instagram_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
3. Миграции и запускBashpython manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Спецификация APIМетодЭндпоинтОписаниеPOST/api/sync/Синхронизация всех постов аккаунта с БД.GET/api/posts/Получение списка постов (параметры: limit, cursor).POST/api/posts/<id>/comment/Добавление комментария (Body: message=текст).Настройка Instagram Graph APIДля работы приложения необходимо получить токен доступа:Зарегистрируйте приложение на Facebook Developers (тип: Business).Добавьте продукт Instagram Graph API.В разделе API Setup привяжите ваш Business или Creator аккаунт.Сгенерируйте User Access Token (long-lived) через Graph API Explorer.Убедитесь, что токен имеет разрешения instagram_basic и instagram_manage_comments.Важно: Функционал создания комментариев требует разрешения instagram_manage_comments, которое в режиме Production предоставляется только после прохождения App Review.
