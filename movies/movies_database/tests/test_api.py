from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movies_database.models import Movie
from movies_database.serializers import MovieSerializer


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.movie_1 = Movie.objects.create(name='Avengers2', year=2013, country='LOL')
        self.movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')
        self.movie_3 = Movie.objects.create(name='Mainstream', year=1235, country='Slovenia')

    def test_get(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        serializer_data = MovieSerializer([self.movie_1, self.movie_2, self.movie_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'search': 'LOL'})
        serializer_data = MovieSerializer([self.movie_1, self.movie_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
