# Один образ для FastAPI и Streamlit: Python + зависимости из requirements.txt
FROM python:3.11-slim

WORKDIR /app

# не писать .pyc и сразу выводить логи в консоль
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# 8888 — API, 8889 — Streamlit (порты пробрасывает docker-compose)
EXPOSE 8888
EXPOSE 8889
