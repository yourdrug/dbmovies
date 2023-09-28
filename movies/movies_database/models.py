from django.contrib.auth.models import User
from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.URLField()


class Director(models.Model):
    name = models.CharField(max_length=100)
    photo = models.URLField()


class Producer(models.Model):
    name = models.CharField(max_length=100)
    photo = models.URLField()


class Screenwriter(models.Model):
    name = models.CharField(max_length=100)
    photo = models.URLField()


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255, default="")
    tagline = models.CharField(max_length=255, default="")
    year = models.SmallIntegerField()
    country = models.CharField(max_length=80)
    genres = models.ManyToManyField(Genre, related_name='film_genres')
    watch_time = models.CharField(max_length=40, default="")
    poster = models.URLField(default="")

    actors = models.ManyToManyField(Actor, related_name='film_actor')
    director = models.ManyToManyField(Director, related_name='film_director')
    producer = models.ManyToManyField(Producer, related_name='film_producer')
    screenwriter = models.ManyToManyField(Screenwriter, related_name='film_screenwriter')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_movies')
    watchers = models.ManyToManyField(User, through='UserMovieRelation', related_name='my_watched_movies')
    rating = models.FloatField(default=None, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.name} {self.year}'


class UserMovieRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(null=True)

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
