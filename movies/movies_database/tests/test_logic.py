from django.contrib.auth.models import User
from django.test import TestCase

from movies_database.logic import set_rating
from movies_database.models import Movie, UserMovieRelation


class SetRatingTestcase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='test_username1', first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='test_username2', first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='test_username3', first_name='Ivan', last_name='Digorov')

        self.movie_1 = Movie.objects.create(name='Avengers', year=2012, country='USA', owner=user1)

        UserMovieRelation.objects.create(user=user1, movie=self.movie_1, like=True, rate=10.2)
        UserMovieRelation.objects.create(user=user2, movie=self.movie_1, like=True, rate=10.2)
        UserMovieRelation.objects.create(user=user3, movie=self.movie_1, like=True, rate=10.2)

    def test_ok(self):
        set_rating(self.movie_1)
        self.movie_1.refresh_from_db()
        self.assertEqual(10.2, self.movie_1.rating)
