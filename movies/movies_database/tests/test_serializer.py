from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from movies_database.models import Movie, UserMovieRelation
from movies_database.serializers import MovieSerializer


class MovieSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='test_username3', first_name='Ivan', last_name='Digorov')
        movie_1 = Movie.objects.create(name='Avengers', year=2012, country='USA', owner=user1)
        movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')

        UserMovieRelation.objects.create(user=user1, movie=movie_1, like=True, rate=10)
        UserMovieRelation.objects.create(user=user2, movie=movie_1, like=True, rate=10)
        UserMovieRelation.objects.create(user=user3, movie=movie_1, like=True, rate=10)

        UserMovieRelation.objects.create(user=user1, movie=movie_2, like=True, rate=5)
        UserMovieRelation.objects.create(user=user2, movie=movie_2, like=False, rate=10)
        UserMovieRelation.objects.create(user=user3, movie=movie_2, like=True)

        movies = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MovieSerializer(movies, many=True).data
        expected_data = [
            {
                'id': movie_1.id,
                'name': 'Avengers',
                'year': 2012,
                'country': 'USA',
                'annotated_likes': 3,
                'rating': 10,
                'owner_name': 'test_username1',
                'watchers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Digorov'
                    },
                ]
            },
            {
                'id': movie_2.id,
                'name': 'LOL',
                'year': 2001,
                'country': 'Russia',
                'annotated_likes': 2,
                'rating': 7.5,
                'owner_name': '',
                'watchers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Digorov'
                    },
                ]
            }
        ]
        self.assertEqual(serializer_data, expected_data)
