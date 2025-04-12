FROM python:3.13.3-alpine3.21


RUN mkdir /app
COPY ./uv.lock /app
COPY ./pyproject.toml /app
WORKDIR /app

RUN pip install uv
RUN uv install

COPY  . /app/


CMD [ "uv", "run", 'main.py' ]
