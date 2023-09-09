from django.test import TestCase

from movies_database.models import Movie
from movies_database.serializers import MovieSerializer


class MovieSerializerTestCase(TestCase):
    def test_ok(self):
        movie_1 = Movie.objects.create(name='Avengers', year=2012, country='USA')
        movie_2 = Movie.objects.create(name='LOL', year=2001, country='Russia')
        serializer_data = MovieSerializer([movie_1, movie_2], many=True).data
        expected_data = [
            {
                'id': movie_1.id,
                'name': 'Avengers',
                'year': 2012,
                'country': 'USA'
            },
            {
                'id': movie_2.id,
                'name': 'LOL',
                'year': 2001,
                'country': 'Russia'
            }
        ]
        self.assertEqual(serializer_data, expected_data)
