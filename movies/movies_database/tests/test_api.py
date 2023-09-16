import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext

from movies_database.models import Movie, UserMovieRelation
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.movie_1 = Movie.objects.create(name='Avengers2', year=2013, country='LOL', owner=self.user)
        self.movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')
        self.movie_3 = Movie.objects.create(name='Mainstream', year=1235, country='Slovenia')

        UserMovieRelation.objects.create(user=self.user, movie=self.movie_1, like=True, rate=5)

    def test_get(self):
        url = reverse('movie-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))
        movies = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1)))
        ).order_by('id')
        serializer_data = MovieSerializer(movies, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], 5)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_get_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'search': 'LOL'})
        movies = Movie.objects.filter(id__in=[self.movie_1.id, self.movie_2.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1)))
        ).order_by('id')
        serializer_data = MovieSerializer(movies, many=True).data
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


class MovieRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.movie_1 = Movie.objects.create(name='Avengers2', year=2013, country='LOL', owner=self.user)
        self.movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')

    def test_like(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            'like': True,
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserMovieRelation.objects.get(user=self.user,
                                                 movie=self.movie_1)
        self.movie_1.refresh_from_db()
        self.assertTrue(relation.like)

    def test_bookmarks(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            'in_bookmarks': True,
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserMovieRelation.objects.get(user=self.user,
                                                 movie=self.movie_1)
        self.movie_1.refresh_from_db()
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            'rate': 8,
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserMovieRelation.objects.get(user=self.user,
                                                 movie=self.movie_1)
        self.movie_1.refresh_from_db()
        self.assertEqual(8, relation.rate)

    def test_rate_negative(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            'rate': -5,
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
