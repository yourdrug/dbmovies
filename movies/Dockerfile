FROM python:3.10.0-alpine

WORKDIR /dbmovies/movies

COPY requirements.txt /dbmovies/movies/

RUN apk update \
    && apk add postgresql-client build-base postgresql-dev musl-dev gcc python3-dev linux-headers \
    && pip install --no-cache-dir -r requirements.txt

COPY . /dbmovies/movies

EXPOSE 8000

RUN adduser --disabled-password movie-user
