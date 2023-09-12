from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from movies_database.models import Movie
from movies_database.serializers import MovieSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['year', 'name']
    search_fields = ['name', 'country']
