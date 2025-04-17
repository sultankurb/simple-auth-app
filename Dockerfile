FROM python:3.13.3-alpine3.21

EXPOSE 80

RUN mkdir /app
COPY ./uv.lock /app
COPY ./pyproject.toml /app
WORKDIR /app

RUN pip install uv
RUN uv sync

COPY  . /app/


CMD uv run uvicorn src.main:app --reload --port 80 --host 0.0.0.0
