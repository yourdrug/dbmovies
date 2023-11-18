from django.contrib import admin
from django.contrib.admin import ModelAdmin

from movies_database.models import Movie, UserMovieRelation, Person, Profession, Genre


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    list_display = ("name", "en_name")
    search_fields = ("name__startswith", "en_name__startswith",)


@admin.register(Profession)
class ProfessionAdmin(ModelAdmin):
    list_display = ("name", "person", "movie")
    search_fields = ("name__startswith", "movie__name__startswith",)


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    search_fields = ("name__startswith",)
    list_filter = ("year",)


@admin.register(UserMovieRelation)
class UserMovieRelationAdmin(ModelAdmin):
    pass
