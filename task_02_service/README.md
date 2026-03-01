# Task 2: FastAPI + Streamlit (CRUD)

Проект реализует CRUD-приложение:
- Backend на FastAPI (работа с CSV)
- Frontend на Streamlit (таблица + графики + формы)

Данные: временной ряд по потреблению и ценам электроэнергии.

---

## Структура проекта

task_02_service/
- backend/main.py — FastAPI API
- backend/data.csv — исходные данные
- frontend/app.py — Streamlit интерфейс
- requirements.txt — зависимости

---

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Запуск (2 терминала)

- **Терминал 1 — backend:** `cd backend && python -m uvicorn main:app --reload`
- **Терминал 2 — frontend:** `cd frontend && python -m streamlit run app.py`

Команды выполнять из корня `task_02_service` (после активации venv).
