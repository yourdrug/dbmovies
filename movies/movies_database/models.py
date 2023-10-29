import datetime
from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=50, unique=True)
    en_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    en_name = models.CharField(max_length=100, unique=True, null=True)
    photo = models.URLField()
    birth_day = models.DateField(default=date.today, null=True)
    death_day = models.DateField(default=None, null=True, blank=True)
    profession = models.ManyToManyField(Profession)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    en_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=1000, default="")
    tagline = models.CharField(max_length=200, default="-", null=True)
    year = models.SmallIntegerField()
    country = models.CharField(max_length=80)
    genres = models.ManyToManyField(Genre, related_name='film_genres')
    watch_time = models.CharField(max_length=40, default="")
    poster = models.URLField(default="")
    world_premier = models.DateField(default=date.today)

    actors = models.ManyToManyField(Person, related_name='film_actor')
    directors = models.ManyToManyField(Person, related_name='film_director')
    producers = models.ManyToManyField(Person, related_name='film_producer')
    screenwriters = models.ManyToManyField(Person, related_name='film_screenwriter')
    composers = models.ManyToManyField(Person, related_name='film_composer')
    designers = models.ManyToManyField(Person, related_name='film_designer')
    editors = models.ManyToManyField(Person, related_name='film_editor')
    operators = models.ManyToManyField(Person, related_name='film_operator')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_movies')
    watchers = models.ManyToManyField(User, through='UserMovieRelation', related_name='my_watched_movies')
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)

    def __str__(self):
        return f'Id {self.id}: {self.name} {self.year}'


class UserMovieRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(10)])

    def __str__(self):
        return f'{self.user.username}: {self.movie.name}, Rating: {self.rate}'

    def save(self, *args, **kwargs):
        from movies_database.logic import set_rating
        creating = not self.pk
        old_rating = self.rate

        super().save(*args, **kwargs)

        new_rating = self.rate

        if old_rating == new_rating or creating:
            set_rating(self.movie)
