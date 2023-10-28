from django.contrib import admin
from django.contrib.admin import ModelAdmin

from movies_database.models import Movie, UserMovieRelation, Person, Profession, Genre


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    pass


@admin.register(Profession)
class ProfessionAdmin(ModelAdmin):
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
