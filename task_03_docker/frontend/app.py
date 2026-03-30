"""
Streamlit: таблица, графики и формы для работы с API (GET/POST/DELETE /records).

Локально API по умолчанию: http://127.0.0.1:8000
В Docker задайте API_URL (см. docker-compose.yml).
"""
import json
import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Task 2 — CRUD", layout="wide")
st.title("Task 2: FastAPI + Streamlit (CRUD)")
st.caption(f"Backend: `{API_URL}`")


def error_detail_from_response(http_response: requests.Response) -> str:
    """Текст ошибки из JSON (поле detail) или сырой ответ, если это не JSON."""
    try:
        body = http_response.json()
        if isinstance(body, dict) and "detail" in body:
            return str(body["detail"])
    except json.JSONDecodeError:
        pass
    text = (http_response.text or "").strip()
    if text:
        return text
    return f"Ошибка сервера (код {http_response.status_code})"


def fetch_records():
    """Загружаем список записей с бэкенда; при сбое возвращаем сообщение."""
    try:
        get_response = requests.get(f"{API_URL}/records", timeout=10)
        get_response.raise_for_status()
        return get_response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


records, fetch_error = fetch_records()
if fetch_error:
    st.error(
        f"Не удалось подключиться к бэкенду: {fetch_error}. "
        "Локально: `cd backend && uvicorn main:app --reload --port 8000`. "
        "Docker: `docker compose up --build` из папки task_03_docker."
    )
    st.stop()

# ответ API превращаем в таблицу pandas
try:
    data = pd.DataFrame(records)
except (TypeError, ValueError) as exc:
    st.error(f"Не удалось разобрать ответ API: {exc}")
    st.stop()

if not data.empty:
    try:
        data["timestep"] = pd.to_datetime(data["timestep"])
    except (ValueError, TypeError, KeyError) as exc:
        st.warning(f"Не удалось привести timestep к датам: {exc}")

st.subheader("Таблица данных")
if data.empty:
    st.info("Нет записей.")
else:
    st.dataframe(data, use_container_width=True)

if not data.empty:
    st.subheader("График: timestep vs consumption_eur и consumption_sib")
    try:
        fig_consumption = px.line(
            data,
            x="timestep",
            y=["consumption_eur", "consumption_sib"],
            title="Consumption EUR / SIB",
        )
        st.plotly_chart(fig_consumption, use_container_width=True)
    except (ValueError, KeyError) as exc:
        st.error(f"Не удалось построить график consumption: {exc}")

    st.subheader("График: timestep vs price_eur и price_sib")
    try:
        fig_price = px.line(
            data,
            x="timestep",
            y=["price_eur", "price_sib"],
            title="Price EUR / SIB",
        )
        st.plotly_chart(fig_price, use_container_width=True)
    except (ValueError, KeyError) as exc:
        st.error(f"Не удалось построить график price: {exc}")

st.subheader("Добавить запись")
with st.form("add_record"):
    timestep = st.text_input(
        "timestep (например 2006-09-01 12:00)",
        value="2006-09-01 12:00",
    )
    consumption_eur = st.number_input(
        "consumption_eur", value=70000.0, step=1000.0
    )
    consumption_sib = st.number_input(
        "consumption_sib", value=19000.0, step=100.0
    )
    price_eur = st.number_input("price_eur", value=450.0, step=10.0)
    price_sib = st.number_input("price_sib", value=0.0, step=10.0)
    submitted = st.form_submit_button("Отправить")
    if submitted:
        try:
            post_response = requests.post(
                f"{API_URL}/records",
                json={
                    "timestep": timestep,
                    "consumption_eur": consumption_eur,
                    "consumption_sib": consumption_sib,
                    "price_eur": price_eur,
                    "price_sib": price_sib,
                },
                timeout=10,
            )
            if post_response.status_code == 200:
                st.success("Запись добавлена.")
                st.rerun()
            else:
                st.error(error_detail_from_response(post_response))
        except requests.RequestException as exc:
            st.error(f"Ошибка запроса к бэкенду: {exc}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            st.error(f"Неожиданная ошибка при добавлении: {exc}")

st.subheader("Удалить запись по id")
delete_id = st.number_input("id для удаления", min_value=0, value=0, step=1)
if st.button("Удалить"):
    try:
        delete_response = requests.delete(
            f"{API_URL}/records/{int(delete_id)}",
            timeout=10,
        )
        if delete_response.status_code == 200:
            st.success("Запись удалена.")
            st.rerun()
        else:
            st.error(error_detail_from_response(delete_response))
    except requests.RequestException as exc:
        st.error(f"Ошибка запроса к бэкенду: {exc}")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        st.error(f"Неожиданная ошибка при удалении: {exc}")
