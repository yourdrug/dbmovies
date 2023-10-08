import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext

from movies_database.models import Movie, UserMovieRelation, Actor, Director, Producer, Screenwriter, Genre
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.actor = Actor.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.director = Director.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.producer = Producer.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.screenwriter = Screenwriter.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.genre = Genre.objects.create(name='test_genre')

        self.movie_1 = Movie.objects.create(name='Avengers2', year=2013, country='LOL',
                                            description='asas', tagline='assa', watch_time='asdasd',
                                            poster='http://127.0.0.1:8000/',
                                            owner=self.user)

        self.movie_1.genres.add(self.genre)
        self.movie_1.actors.add(self.actor)
        self.movie_1.director.add(self.director)
        self.movie_1.producer.add(self.producer)
        self.movie_1.screenwriter.add(self.screenwriter)

        self.movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')

        self.movie_2.genres.add(self.genre)
        self.movie_2.actors.add(self.actor)
        self.movie_2.director.add(self.director)
        self.movie_2.producer.add(self.producer)
        self.movie_2.screenwriter.add(self.screenwriter)

        self.movie_3 = Movie.objects.create(name='Mainstream', year=1235, country='Slovenia')

        self.movie_3.genres.add(self.genre)
        self.movie_3.actors.add(self.actor)
        self.movie_3.director.add(self.director)
        self.movie_3.producer.add(self.producer)
        self.movie_3.screenwriter.add(self.screenwriter)

        UserMovieRelation.objects.create(user=self.user, movie=self.movie_1, like=True, rate=5)

    def test_get(self):
        url = reverse('movie-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(17, len(queries))
        movies = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
        ).order_by('id')
        serializer_data = MovieSerializer(movies, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], 5)
        self.assertEqual(serializer_data[0]['annotated_count_rate'], 1)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_get_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'search': 'LOL'})
        movies = Movie.objects.filter(id__in=[self.movie_1.id, self.movie_2.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
        ).order_by('id')
        serializer_data = MovieSerializer(movies, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Movie.objects.all().count())
        url = reverse('movie-list')
        data = {
            "actors": [{"id": 2, "name": "Крис Хемсворт","photo": "https://st.kp.yandex.net/images/actor_iphone/iphone360_1300401.jpg"}],
            "name": "Barbie",
            "description": "Самая обыкновенная стереотипная Барби живёт в великолепном розовом Барбиленде",
            "tagline": "-",
            "year": 2023,
            "country": "USA",
            "watch_time": "114 мин. / 01:54",
            "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/4774061/f0ae94af-050a-433b-a2a9-d6c96d644fd8/orig",
            "owner": 1,
            "genres": [{"id": 2, "name": "Крис Хемсворт","photo": "https://st.kp.yandex.net/images/actor_iphone/iphone360_1300401.jpg"}],
            "director": [{"id": 2, "name": "Крис Хемсворт","photo": "https://st.kp.yandex.net/images/actor_iphone/iphone360_1300401.jpg"}],
            "producer": [{"id": 2, "name": "Крис Хемсворт","photo": "https://st.kp.yandex.net/images/actor_iphone/iphone360_1300401.jpg"}],
            "screenwriter": [{"id": 2, "name": "Крис Хемсворт","photo": "https://st.kp.yandex.net/images/actor_iphone/iphone360_1300401.jpg"}]
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(4, Movie.objects.all().count())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

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
            "name": self.movie_1.name,
            "description": self.movie_1.description,
            "tagline": self.movie_1.tagline,
            "year": 2000,
            "country": self.movie_1.country,
            "watch_time": self.movie_1.watch_time,
            "poster": self.movie_1.poster,
            "owner": self.user.id,
            "actors": [self.actor.id],
            "genres": [self.genre.id],
            "director": [self.director.id],
            "producer": [self.producer.id],
            "screenwriter": [self.screenwriter.id]
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
            "name": self.movie_1.name,
            "description": self.movie_1.description,
            "tagline": self.movie_1.tagline,
            "year": 2000,
            "country": self.movie_1.country,
            "watch_time": self.movie_1.watch_time,
            "poster": self.movie_1.poster,
            "owner": self.user.id,
            "actors": [self.actor.id],
            "genres": [self.genre.id],
            "director": [self.director.id],
            "producer": [self.producer.id],
            "screenwriter": [self.screenwriter.id]
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
            "name": self.movie_1.name,
            "description": self.movie_1.description,
            "tagline": self.movie_1.tagline,
            "year": 2000,
            "country": self.movie_1.country,
            "watch_time": self.movie_1.watch_time,
            "poster": self.movie_1.poster,
            "owner": self.user.id,
            "actors": [self.actor.id],
            "genres": [self.genre.id],
            "director": [self.director.id],
            "producer": [self.producer.id],
            "screenwriter": [self.screenwriter.id]
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
