FROM python:3.10.0-alpine

COPY ./requirements.txt /temp/requirements.txt

RUN apk update \
    && apk add postgresql-client build-base postgresql-dev musl-dev gcc python3-dev linux-headers \
    && pip install --no-cache-dir -r /temp/requirements.txt

COPY ../../movies /movies
WORKDIR /movies
EXPOSE 8000

RUN adduser --disabled-password movie-user
