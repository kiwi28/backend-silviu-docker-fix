FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100

COPY requirements.txt /var/task/
WORKDIR /var/task

RUN pip install -r requirements.txt


