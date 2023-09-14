import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movies_database.models import Movie
from movies_database.serializers import MovieSerializer


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.movie_1 = Movie.objects.create(name='Avengers2', year=2013, country='LOL', owner=self.user)
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

    def test_create(self):
        self.assertEqual(3, Movie.objects.all().count())
        url = reverse('movie-list')
        data = {
            'name': 'Beauty and Beast',
            'year': 2017,
            'country': 'UK'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Movie.objects.all().count())

    def test_delete(self):
        url = reverse('movie-detail', args=(self.movie_1.id,))
        self.assertEqual(3, Movie.objects.all().count())
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Movie.objects.all().count())

    def test_update(self):
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            'name': self.movie_1.name,
            'year': 2000,
            'country': self.movie_1.country
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual(2000, self.movie_1.year)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            'name': self.movie_1.name,
            'year': 2000,
            'country': self.movie_1.country
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual(2013, self.movie_1.year)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            'name': self.movie_1.name,
            'year': 2000,
            'country': self.movie_1.country
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual(2000, self.movie_1.year)
