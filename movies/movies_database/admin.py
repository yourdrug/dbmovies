from django.contrib import admin
from django.contrib.admin import ModelAdmin

from movies_database.models import Movie


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    pass
