from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movies_database.models import Movie
from movies_database.serializers import MovieSerializer


class MovieApiTestCase(APITestCase):
    def test_get(self):
        movie_1 = Movie.objects.create(name='Avengers', year=2012, country='USA')
        movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')
        url = reverse('movie-list')
        response = self.client.get(url)
        serializer_data = MovieSerializer([movie_1, movie_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
