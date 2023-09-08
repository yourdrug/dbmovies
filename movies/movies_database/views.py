from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from movies_database.models import Movie
from movies_database.serializers import MovieSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
