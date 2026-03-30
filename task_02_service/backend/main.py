"""
FastAPI backend: CRUD для записей из data.csv.
Эндпоинты: GET /records, POST /records, DELETE /records/{id}
"""
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Task 2 Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent / "data.csv"


def load_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["timestep"] = pd.to_datetime(df["timestep"])
    return df


def save_df(df: pd.DataFrame) -> None:
    df = df.copy()
    df["timestep"] = df["timestep"].astype(str)
    df.to_csv(DATA_PATH, index=False)


class RecordCreate(BaseModel):
    timestep: str
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float


@app.get("/records")
def get_records():
    """Читать data.csv, добавить id = индекс строки, вернуть список словарей JSON."""
    try:
        df = load_df()
        df = df.reset_index(drop=True)
        df["id"] = df.index
        # для JSON даты в строки
        out = df.copy()
        out["timestep"] = out["timestep"].astype(str)
        return out.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/records")
def post_record(record: RecordCreate):
    """Добавить новую запись в конец, сохранить в CSV. timestep должен парситься как дата/время."""
    try:
        pd.to_datetime(record.timestep)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"timestep не является датой/временем: {e}")
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    """Удалить запись по id (индекс строки). После удаления reset_index и сохранить CSV."""
    try:
        df = load_df()
        if record_id < 0 or record_id >= len(df):
            raise HTTPException(status_code=404, detail="id не найден")
        df = df.drop(index=record_id).reset_index(drop=True)
        save_df(df)
        return {"message": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
