# Task 03 — Docker (FastAPI + Streamlit)

## Project description

Мини-сервис дашборда по данным потребления/цен из `data.csv`: REST API на **FastAPI** (CRUD по записям) и веб-интерфейс на **Streamlit** с таблицей, графиками Plotly и формами добавления/удаления записей.

## Project structure

- `backend/` — FastAPI (`main.py`), файл данных `data.csv`
- `frontend/` — Streamlit (`app.py`)
- `requirements.txt` — зависимости Python
- `Dockerfile` — сборка общего образа для обоих сервисов
- `docker-compose.yml` — два контейнера: API и Streamlit
- `.dockerignore` — исключения для контекста сборки

## How to run locally (without Docker)

Терминал 1 — backend (порт **8000**, как в исходном задании):

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Терминал 2 — frontend (переменная `API_URL` не обязательна, по умолчанию `http://127.0.0.1:8000`):

```bash
cd frontend
streamlit run app.py
```

## How to run with Docker

Из **корня** папки `task_03_docker`:

```bash
docker compose up --build
```

Если установлена старая версия Compose:

```bash
docker-compose up --build
```

Проверка контейнеров:

```bash
docker compose ps
```

## Available services

| Сервис    | URL                         |
|-----------|-----------------------------|
| FastAPI   | <http://localhost:8888>     |
| Streamlit | <http://localhost:8889>     |

- Корневой эндпоинт API: `GET http://localhost:8888/` → `{"status":"ok",...}`
- Данные: `GET http://localhost:8888/records`

Внутри Docker Streamlit обращается к API по имени сервиса `fastapi` и порту **8888** (переменная `API_URL` задаётся в `docker-compose.yml`).

## How to use the application

1. Откройте в браузере **Streamlit**: <http://localhost:8889> (или локальный порт Streamlit без Docker).
2. На странице отображается **таблица** всех записей из `data.csv` (через API).
3. Ниже — **два линейных графика**: потребление (EUR/SIB) и цены (EUR/SIB) по времени `timestep`.
4. Форма **«Добавить запись»**: заполните `timestep` (дата/время), числовые поля и нажмите **Отправить** — запись добавится в CSV через `POST /records`.
5. Блок **«Удалить запись по id»**: укажите `id` строки (как в таблице) и нажмите **Удалить** — вызовется `DELETE /records/{id}`.

При недоступном бэкенде интерфейс покажет сообщение об ошибке, а не «сыплющуюся» трассировку.

## Error handling

- **Backend**: отсутствие/битый `data.csv`, ошибки парсинга дат и сохранения файла возвращаются как `HTTPException` с понятным `detail`.
- **Frontend**: сетевые ошибки и не-200 ответы обрабатываются через `st.error` / разбор `detail` из JSON.

## Linting (optional)

Установка инструментов (один раз):

```bash
python3 -m pip install flake8 pylint
```

Проверка Python:

```bash
cd task_03_docker
flake8 backend/main.py frontend/app.py --max-line-length=120
pylint backend/main.py frontend/app.py --max-line-length=120 --disable="C0103,C0114,C0115"
```

Проверка Dockerfile (нужен запущенный Docker):

```bash
cat Dockerfile | docker run --rm -i hadolint/hadolint
```

## Pre-submission checklist

1. Запустить **Docker Desktop**, затем `docker compose up --build` из этой папки.
2. Открыть <http://localhost:8888/> и <http://localhost:8889>, убедиться, что UI грузит данные.
3. При необходимости: `docker compose logs` — без бесконечных traceback.
4. Прогнать команды из раздела **Linting** выше.
5. В корне репозитория: `git add task_03_docker/`, коммит в ветке `task_03`, `git push -u origin task_03`, на GitHub — **Pull Request** `task_03` → `main`.
