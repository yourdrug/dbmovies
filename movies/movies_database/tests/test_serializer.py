import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from account.models import Account
from movies_database.models import Movie, UserMovieRelation, Person, Genre, Profession
from movies_database.serializers import MovieSerializer


class MovieSerializerTestCase(TestCase):

    def test_ok(self):
        user1 = Account.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        user2 = Account.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        user3 = Account.objects.create(username='test_username3', first_name='Ivan', last_name='Digorov')

        # self.person = Person.objects.create(name='test_actor', photo='http://127.0.0.1:8000/', birth_day=datetime.date(2020, 2, 2))
        # self.genre = Genre.objects.create(name='test_genre', slug='test_slug')

        self.movie_1 = Movie.objects.create(
            name='s', description='a', year=2012, watch_time='asdasd', country='USA',
            tagline='a',  poster='http://127.0.0.1:8000/',
            world_premier=datetime.date(2020, 2, 2))

        # self.movie_1.genres.add(self.genre)
        # Profession.objects.create(person=self.person, movie=self.movie_1, name='актер', slug='actor')

        UserMovieRelation.objects.create(user=user1, movie=self.movie_1, like=True, rate=8)
        UserMovieRelation.objects.create(user=user2, movie=self.movie_1, like=True, rate=8)
        user_movie_3 = UserMovieRelation.objects.create(user=user3, movie=self.movie_1, like=True)
        user_movie_3.rate = 8
        user_movie_3.save()

        movies = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
        ).order_by('id')
        # expected_data = {
        #     'id': self.movie_1.id,
        #     'name': 's',
        #     'description': 'a',
        #     'tagline': 'a',
        #     'watch_time': 'asdasd',
        #     'year': 2012,
        #     'country': 'USA',
        #     'poster': 'http://127.0.0.1:8000/',
        #     'world-premier': '2020-02-02',
        #     'annotated_likes': 3,
        #     'rating': 8,
        #     'owner_name': 'test_username1',
        #     'crew': [{'slug': 'actor',
        #               'person': {'id': self.person.id, 'name': 'test_actor', 'en_name': None,
        #                          'photo': 'http://127.0.0.1:8000/', 'birth_day': '2020-02-02', 'death_day': None}}],
        #     'genres': [{'id': self.genre.id, 'name': 'test_genre', 'slug': 'test_slug'}],
        #     'annotated_count_rate': 3,
        # }
        serializer = MovieSerializer(data=movies)
        self.assertTrue(serializer.is_valid())
