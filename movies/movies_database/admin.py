from django.contrib import admin
from django.contrib.admin import ModelAdmin

from movies_database.models import Movie, UserMovieRelation


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    pass


@admin.register(UserMovieRelation)
class UserMovieRelationAdmin(ModelAdmin):
    pass
