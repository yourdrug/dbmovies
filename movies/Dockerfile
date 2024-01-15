FROM python:3.10-slim-bullseye

WORKDIR /dbmovies/movies

COPY requirements.txt /dbmovies/movies/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /dbmovies/movies

EXPOSE 8000

RUN adduser --disabled-password movie-user
