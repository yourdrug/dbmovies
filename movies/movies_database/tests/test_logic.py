import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from account.models import Account
from movies_database.logic import set_rating
from movies_database.models import Movie, UserMovieRelation


class SetRatingTestcase(TestCase):
    def setUp(self):
        user1 = Account.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        user2 = Account.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        user3 = Account.objects.create(username='test_username3', first_name='Ivan', last_name='Digorov')

        self.movie_1 = Movie.objects.create(
            name='s', description='a', year=2012, watch_time='asdasd', country='USA',
            tagline='a', poster='http://127.0.0.1:8000/',
            world_premier=datetime.date(2020, 2, 2))

        UserMovieRelation.objects.create(user=user1, movie=self.movie_1, like=True, rate=12)
        UserMovieRelation.objects.create(user=user2, movie=self.movie_1, like=True, rate=12)
        UserMovieRelation.objects.create(user=user3, movie=self.movie_1, like=True, rate=12)

    def test_ok(self):
        set_rating(self.movie_1)
        self.movie_1.refresh_from_db()
        self.assertEqual(12, self.movie_1.rating)
