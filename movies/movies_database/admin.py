from django.contrib import admin
from django.contrib.admin import ModelAdmin

from movies_database.models import Movie, UserMovieRelation, Actor, Director, Producer, Screenwriter, Genre


@admin.register(Actor)
class ActorAdmin(ModelAdmin):
    pass


@admin.register(Director)
class DirectorAdmin(ModelAdmin):
    pass


@admin.register(Producer)
class ProducerAdmin(ModelAdmin):
    pass


@admin.register(Screenwriter)
class ScreenwriterAdmin(ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    pass


@admin.register(UserMovieRelation)
class UserMovieRelationAdmin(ModelAdmin):
    pass
