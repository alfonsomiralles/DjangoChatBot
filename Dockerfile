FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements-docker.txt /app/
RUN pip install -r requirements-docker.txt

COPY . /app/

# Copia el script wait_for_db.py en el contenedor
COPY wait_for_db.py /app/