"""
FastAPI: CRUD для записей из data.csv.
Эндпоинты: GET /, GET /records, POST /records, DELETE /records/{id}
"""
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Task 2 Backend", version="1.0")

# разрешаем запросы с другого origin (нужно для Streamlit в браузере)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent / "data.csv"


def load_df() -> pd.DataFrame:
    """Читаем CSV и сразу приводим колонку timestep к датам."""
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Файл данных не найден: {DATA_PATH}",
        ) from exc
    except pd.errors.EmptyDataError as exc:
        raise HTTPException(
            status_code=500,
            detail="Файл data.csv пуст или повреждён",
        ) from exc
    except (OSError, pd.errors.ParserError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка чтения CSV: {exc}",
        ) from exc
    except Exception as exc:
        # остальные редкие сбои read_csv — тоже отдаём текстом, без «сырого» traceback в UI
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка чтения CSV: {exc}",
        ) from exc
    try:
        df["timestep"] = pd.to_datetime(df["timestep"])
    except (KeyError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Некорректный формат колонки timestep: {exc}",
        ) from exc
    return df


def save_df(df: pd.DataFrame) -> None:
    """Сохраняем таблицу в CSV; даты пишем строкой, чтобы файл был читаемым."""
    try:
        to_save = df.copy()
        to_save["timestep"] = to_save["timestep"].astype(str)
        to_save.to_csv(DATA_PATH, index=False)
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось сохранить data.csv: {exc}",
        ) from exc


class RecordCreate(BaseModel):
    timestep: str
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float


@app.get("/")
def root():
    """Проверка, что сервис запущен."""
    return {"status": "ok", "service": "task-03-docker-backend"}


@app.get("/records")
def get_records():
    """Отдаём все строки из CSV как JSON; id = номер строки (с нуля)."""
    try:
        df = load_df()
        df = df.reset_index(drop=True)
        df["id"] = df.index
        out = df.copy()
        out["timestep"] = out["timestep"].astype(str)
        return out.to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/records")
def post_record(record: RecordCreate):
    """Добавляем строку в конец файла; timestep должен быть валидной датой."""
    try:
        pd.to_datetime(record.timestep)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"timestep не является датой/временем: {exc}",
        ) from exc
    try:
        df = load_df()
        new_row = {
            "timestep": record.timestep,
            "consumption_eur": record.consumption_eur,
            "consumption_sib": record.consumption_sib,
            "price_eur": record.price_eur,
            "price_sib": record.price_sib,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df["timestep"] = pd.to_datetime(df["timestep"])
        save_df(df)
        return {"message": "ok", "id": len(df) - 1}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    """Удаляем строку по id (как в таблице), пересчитываем индексы и сохраняем."""
    try:
        df = load_df()
        if record_id < 0 or record_id >= len(df):
            raise HTTPException(status_code=404, detail="id не найден")
        df = df.drop(index=record_id).reset_index(drop=True)
        save_df(df)
        return {"message": "ok"}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
