"""
Streamlit frontend: только API (GET/POST/DELETE /records). Таблица, 2 графика Plotly, форма добавления, удаление по id.
"""
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Task 2 — CRUD", layout="wide")
st.title("Task 2: FastAPI + Streamlit (CRUD)")

# Получаем данные только через API
def fetch_records():
    try:
        r = requests.get(f"{BACKEND_URL}/records", timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as e:
        return None, str(e)

rows, err = fetch_records()
if err:
    st.error(f"Не удалось подключиться к бэкенду: {err}. Запусти: cd backend && python -m uvicorn main:app --reload")
    st.stop()

data = pd.DataFrame(rows)
if not data.empty:
    data["timestep"] = pd.to_datetime(data["timestep"])

st.subheader("Таблица данных")
if data.empty:
    st.info("Нет записей.")
else:
    st.dataframe(data, use_container_width=True)

if not data.empty:
    st.subheader("График: timestep vs consumption_eur и consumption_sib")
    fig1 = px.line(
        data,
        x="timestep",
        y=["consumption_eur", "consumption_sib"],
        title="Consumption EUR / SIB",
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("График: timestep vs price_eur и price_sib")
    fig2 = px.line(
        data,
        x="timestep",
        y=["price_eur", "price_sib"],
        title="Price EUR / SIB",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Добавить запись")
with st.form("add_record"):
    timestep = st.text_input("timestep (например 2006-09-01 12:00)", value="2006-09-01 12:00")
    consumption_eur = st.number_input("consumption_eur", value=70000.0, step=1000.0)
    consumption_sib = st.number_input("consumption_sib", value=19000.0, step=100.0)
    price_eur = st.number_input("price_eur", value=450.0, step=10.0)
    price_sib = st.number_input("price_sib", value=0.0, step=10.0)
    submitted = st.form_submit_button("Отправить")
    if submitted:
        try:
            r = requests.post(
                f"{BACKEND_URL}/records",
                json={
                    "timestep": timestep,
                    "consumption_eur": consumption_eur,
                    "consumption_sib": consumption_sib,
                    "price_eur": price_eur,
                    "price_sib": price_sib,
                },
                timeout=5,
            )
            if r.status_code == 200:
                st.success("Запись добавлена.")
                st.rerun()
            else:
                st.error(r.json().get("detail", r.text))
        except requests.RequestException as e:
            st.error(str(e))

st.subheader("Удалить запись по id")
del_id = st.number_input("id для удаления", min_value=0, value=0, step=1)
if st.button("Удалить"):
    try:
        r = requests.delete(f"{BACKEND_URL}/records/{int(del_id)}", timeout=5)
        if r.status_code == 200:
            st.success("Запись удалена.")
            st.rerun()
        else:
            st.error(r.json().get("detail", r.text))
    except requests.RequestException as e:
        st.error(str(e))
