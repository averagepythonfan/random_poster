FROM python:3.10-slim

RUN pip install "poetry==1.3.2"

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --only poster --no-root

COPY /poster .