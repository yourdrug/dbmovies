from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from movies_database.models import Movie, UserMovieRelation, Actor, Director, Producer, Screenwriter, Genre
from movies_database.serializers import MovieSerializer


class MovieSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='test_username3', first_name='Ivan', last_name='Digorov')

        self.actor = Actor.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.director = Director.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.producer = Producer.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.screenwriter = Screenwriter.objects.create(name='test_actor', photo='http://127.0.0.1:8000/')
        self.genre = Genre.objects.create(name='test_genre')

        movie_1 = Movie.objects.create(name='Avengers', year=2012, country='USA', description='asas',
                                       tagline='assa', watch_time='asdasd',
                                       poster='http://127.0.0.1:8000/', owner=user1)

        movie_1.genres.add(self.genre)
        movie_1.actors.add(self.actor)
        movie_1.director.add(self.director)
        movie_1.producer.add(self.producer)
        movie_1.screenwriter.add(self.screenwriter)
        # movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')

        UserMovieRelation.objects.create(user=user1, movie=movie_1, like=True, rate=8)
        UserMovieRelation.objects.create(user=user2, movie=movie_1, like=True, rate=8)
        user_movie_3 = UserMovieRelation.objects.create(user=user3, movie=movie_1, like=True)
        user_movie_3.rate = 8
        user_movie_3.save()

        # UserMovieRelation.objects.create(user=user1, movie=movie_2, like=True, rate=5)
        # UserMovieRelation.objects.create(user=user2, movie=movie_2, like=False, rate=10)
        # UserMovieRelation.objects.create(user=user3, movie=movie_2, like=True)

        movies = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1)))
        ).order_by('id')
        serializer_data = MovieSerializer(movies, many=True).data
        expected_data = [{
            'actors': [{'id': self.actor.id, 'name': 'test_actor', 'photo': 'http://127.0.0.1:8000/'}],
            'annotated_likes': 3,
            'country': 'USA',
            'description': 'asas',
            'director': [{'id': self.director.id, 'name': 'test_actor', 'photo': 'http://127.0.0.1:8000/'}],
            'genres': [{'id': self.genre.id, 'name': 'test_genre'}],
            'id': movie_1.id,
            'owner': user1.id,
            'name': 'Avengers',
            'owner_name': 'test_username1',
            'poster': 'http://127.0.0.1:8000/',
            'producer': [{'id': self.producer.id, 'name': 'test_actor', 'photo': 'http://127.0.0.1:8000/'}],
            'rating': 8,
            'screenwriter': [{'id': self.screenwriter.id, 'name': 'test_actor', 'photo': 'http://127.0.0.1:8000/'}],
            'tagline': 'assa',
            'watch_time': 'asdasd',
            'watchers': [{'first_name': 'Ivan', 'last_name': 'Petrov'},
                         {'first_name': 'Ivan', 'last_name': 'Sidorov'},
                         {'first_name': 'Ivan', 'last_name': 'Digorov'}],
            'year': 2012},

        ]

        print(serializer_data)
        self.assertEqual(serializer_data, expected_data)
