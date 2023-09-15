from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=80)
    year = models.SmallIntegerField()
    country = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_movies')
    watchers = models.ManyToManyField(User, through='UserMovieRelation', related_name='my_watched_movies')

    def __str__(self):
        return f'Id {self.id}: {self.name} {self.year}'


class UserMovieRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.user.username}: {self.movie.name}, Rating: {self.rate}'
