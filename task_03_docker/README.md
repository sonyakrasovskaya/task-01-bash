# Task 03 — Docker (FastAPI + Streamlit)

Коротко: API читает и меняет `data.csv`, Streamlit показывает таблицу, графики и формы.

## Структура папки

- `backend/` — `main.py` и `data.csv`
- `frontend/` — `app.py` (Streamlit)
- `requirements.txt` — библиотеки Python
- `Dockerfile` — один образ на оба сервиса
- `docker-compose.yml` — два контейнера: API и интерфейс

## Запуск без Docker

**Терминал 1** — бэкенд (порт 8000):

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Терминал 2** — фронт (по умолчанию ходит на `http://127.0.0.1:8000`):

```bash
cd frontend
streamlit run app.py
```

## Запуск с Docker

Из папки `task_03_docker`:

```bash
docker compose up --build
```

Если у вас старая команда:

```bash
docker-compose up --build
```

## Адреса в браузере

| Что открыть | Адрес |
|-------------|--------|
| API | http://localhost:8888 |
| Проверка «жив ли сервис» | http://localhost:8888/ |
| Список записей (JSON) | http://localhost:8888/records |
| Интерфейс (таблица и графики) | http://localhost:8889 |

В Docker Streamlit подключается к API по внутреннему адресу `http://fastapi:8888` (это задано в `docker-compose.yml`).

## Как пользоваться интерфейсом

1. Откройте http://localhost:8889 (или адрес, который покажет Streamlit без Docker).
2. Увидите **таблицу** и два **графика** по данным из CSV.
3. **Добавить запись** — заполните поля формы и нажмите «Отправить».
4. **Удалить** — введите `id` строки (как в таблице) и нажмите «Удалить».

Если бэкенд не запущен, на странице будет понятное сообщение об ошибке.

## Линтеры (перед сдачей)

Удобно завести виртуальное окружение в этой папке, чтобы не ставить пакеты в системный Python:

```bash
cd task_03_docker
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install flake8 pylint
flake8 backend/main.py frontend/app.py --max-line-length=120
pylint backend/main.py frontend/app.py --max-line-length=120 --disable="C0103,C0114,C0115"
```

Проверка `Dockerfile` (нужен запущенный Docker):

```bash
cat Dockerfile | docker run --rm -i hadolint/hadolint
```

У hadolint может быть предупреждение про версию `pip` в образе — для учебного проекта это обычно допустимо.

## Перед сдачей

1. Запустить `docker compose up --build` из этой папки.
2. Открыть http://localhost:8888/ и http://localhost:8889 — данные должны загружаться.
3. При проблемах посмотреть логи: `docker compose logs`.
4. По желанию — команды из раздела «Линтеры» выше.
