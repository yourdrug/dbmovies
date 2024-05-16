from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.db import models

User = settings.AUTH_USER_MODEL


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    en_name = models.CharField(max_length=100, unique=True, null=True)
    photo = models.URLField()
    birth_day = models.DateField(default=date.today, null=True)
    death_day = models.DateField(default=None, null=True, blank=True)

    # profession = models.ManyToManyField(Profession)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=1500, default="")
    tagline = models.CharField(max_length=200, default="-", null=True)
    year = models.PositiveIntegerField()
    country = models.CharField(max_length=80)
    genres = models.ManyToManyField(Genre, related_name='film_genres')
    watch_time = models.CharField(max_length=40, default="")
    poster = models.URLField(default="")
    world_premier = models.DateField(default=date.today)
    movie_video = models.FileField(
        blank=True,
        null=True,
        upload_to=f"video/{name}/",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )

    crew = models.ManyToManyField(Person, through='Profession', related_name='person_movies')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_movies')
    watchers = models.ManyToManyField(User, through='UserMovieRelation', related_name='my_watched_movies')
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)

    def __str__(self):
        return f'Id {self.id}: {self.name} {self.year}'


def get_upload_path(instance, filename):
    movie_name = instance.movie.name.replace(" ", "_")
    person_name = instance.person.name.replace(" ", "_")
    return f'actors/{movie_name}/{person_name}/{filename}'


class Profession(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=None, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class UserMovieRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    is_watched = models.BooleanField(default=False)
    will_watch = models.BooleanField(default=False)

    rate = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(10)])
    review = models.TextField(blank=True, null=True, default=None)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user.username}: {self.movie.name}, Rating: {self.rate}'

    def save(self, *args, **kwargs):
        from movies_database.logic import set_rating
        creating = not self.pk
        old_rating = self.rate

        if self.review is None:
            self.review = None

        super().save(*args, **kwargs)

        new_rating = self.rate

        if old_rating == new_rating or creating:
            set_rating(self.movie)
