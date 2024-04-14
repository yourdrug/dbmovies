import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext

from account.models import Account
from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer

from django.test.client import RequestFactory


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        self.genre_1 = Genre.objects.create(name='Action', slug='action')
        self.genre_2 = Genre.objects.create(name='Drama',  slug='drama')
        self.person_1 = Person.objects.create(name='John Doe')
        self.person_2 = Person.objects.create(name='Johna Daa')

        self.movie_1 = Movie.objects.create(
            name='Test Movie',
            description='This is a test movie',
            year=2022,
            country='USA',
            owner=self.user,
        )
        self.movie_1.genres.add(self.genre_1)
        Profession.objects.create(person=self.person_1, movie=self.movie_1, name="режиссер", slug="director")
        self.user_movie_relation = UserMovieRelation.objects.create(
            user=self.user,
            movie=self.movie_1,
            like=True,
            rate=4,
            review='Great movie!',
        )

        self.movie_2 = Movie.objects.create(
            name='Test Movie 2',
            description='This is a test drama movie',
            year=2022,
            country='USA',
            owner=self.user,
        )
        self.movie_2.genres.add(self.genre_2)
        Profession.objects.create(person=self.person_2, movie=self.movie_2, name="актер", slug="actor")
        self.user_movie_relation_2 = UserMovieRelation.objects.create(
            user=self.user,
            movie=self.movie_2,
            like=False,
            rate=3,
            review='Decent drama film.',
        )

        self.movie_3 = Movie.objects.create(
            name='HAHA',
            description='not a film',
            year=2022,
            country='USA',
            owner=self.user,
        )
        self.movie_3.genres.add(self.genre_1, self.genre_2)
        Profession.objects.create(person=self.person_1, movie=self.movie_3, name="режиссер", slug="director")
        Profession.objects.create(person=self.person_2, movie=self.movie_3, name="актер", slug="actor")
        self.user_movie_relation_3 = UserMovieRelation.objects.create(
            user=self.user,
            movie=self.movie_3,
            like=True,
            rate=4,
            review='Enjoyable movie with both action and drama.',
        )
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_get(self):
        url = reverse('movie-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            movies = Movie.objects.all().annotate(
                annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
                annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
            ).order_by('id')
            serializer_data = MovieSerializer(movies, many=True, context={"request": self.request}).data
            self.assertEqual(status.HTTP_200_OK, response.status_code)

            for expected_movie, actual_movie in zip(serializer_data, response.data['results']):
                self.assertEqual(expected_movie['id'], actual_movie['id'])
                self.assertEqual(expected_movie['name'], actual_movie['name'])
                self.assertEqual(expected_movie['watch_time'], actual_movie['watch_time'])
                self.assertEqual(expected_movie['world_premier'], actual_movie['world_premier'])
                self.assertEqual(expected_movie['year'], actual_movie['year'])
                self.assertEqual(expected_movie['country'], actual_movie['country'])
                self.assertEqual(expected_movie['poster'], actual_movie['poster'])
                self.assertEqual(expected_movie['rating'], actual_movie['rating'])
                # Добавьте дополнительные поля, которые вам важны

            # Проверяем количество элементов
            self.assertEqual(len(serializer_data), response.data['count'])

    def test_create(self):
        self.assertEqual(3, Movie.objects.all().count())
        url = reverse('movie-list')

        data = {
            "name": "New Movie",
            "description": "This is a new movie",
            "tagline": "Exciting",
            "year": 2023,
            "country": "USA",
            "genres": [self.genre_1.id, self.genre_2.id],
            "watch_time": "2h 30min",
            "poster": "https://example.com/poster.jpg",
            "world_premier": "2023-01-01",
            "crew": [{"slug": "actor", "person": {"id": 3, "name": "Анн Ле Ни", "en_name": "Anne Le Ny"},
                      "image": None}]
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(4, Movie.objects.all().count())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_delete(self):
        url = reverse('movie-detail', args=[self.movie_2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Movie.objects.filter(id=self.movie_2.id).exists())

    def test_update(self):
        url = reverse('movie-detail', args=(self.movie_1.id,))
        updated_data = {
            "year": 2024,
        }
        json_data = json.dumps(updated_data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual(2024, self.movie_1.year)
        self.assertEqual("Test Movie", self.movie_1.name)

    def test_update_not_owner(self):
        self.user2 = Account.objects.create_user(username='test_username2', password='asdasdadas')
        self.token = Token.objects.create(user=self.user2)
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            "year": 2000,
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual(2022, self.movie_1.year)

    def test_update_not_owner_but_staff(self):
        self.user2 = Account.objects.create_user(username='test_username2', password='sadasdsada', is_staff=True)
        self.token = Token.objects.create(user=self.user2)
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            "year": 2000
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual(2000, self.movie_1.year)


class MovieRelationTestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='test_username', password='asasdasd')
        self.token = Token.objects.create(user=self.user)
        self.user2 = Account.objects.create_user(username='test_username2', password='asdasdasd')
        self.token2 = Token.objects.create(user=self.user2)
        self.movie_1 = Movie.objects.create(name='Avengers2', year=2013, country='LOL', owner=self.user)
        self.movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')

    def test_like(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            'like': True,
        }

        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
