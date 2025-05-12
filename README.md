# TaskGPT

Веб‑задачник с AI и Telegram‑ботом.

## Быстрый старт

1. Создайте Google Sheet с листами `Tasks` и `Achievements`.
2. Получите JSON сервисного аккаунта Google и занесите в `.env`.
3. Создайте бота через BotFather, узнавайте chat_id.
4. Заполните `.env` (см. `.env.example`).
5. Локально:
    ```bash
    cd backend
    pip install -r requirements.txt
    python app.py
    ```
6. Frontend:
    ```bash
    cd frontend
    npm install
    npm run build
    ```
7. Деплой на Render: создайте Web Service, добавьте переменные окружения, команда запуска:
    `gunicorn backend.app:app`.
