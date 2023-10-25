FROM python:3.10.0-alpine

COPY ../requirements.txt /temp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

COPY ../../movies /movies
WORKDIR /movies
EXPOSE 8000

RUN adduser --disabled-password movie-user

USER movie-user