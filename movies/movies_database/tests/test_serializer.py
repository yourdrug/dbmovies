import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from account.models import Account
from movies_database.models import Movie, UserMovieRelation, Person, Genre, Profession
from movies_database.serializers import MovieSerializer


class MovieSerializerTestCase(TestCase):

    def setUp(self):
        # Создаем необходимые объекты для тестирования
        self.user = Account.objects.create_user(username='testuser', password='testpassword')
        self.genre = Genre.objects.create(name='Action')
        self.person = Person.objects.create(name='John Doe')
        self.movie = Movie.objects.create(
            name='Test Movie',
            description='This is a test movie',
            year=2022,
            country='USA',
            owner=self.user,
            rating=4.5,
        )
        self.movie.genres.add(self.genre)
        Profession.objects.create(person=self.person, movie=self.movie,
                                  name="режиссер", slug="director")
        self.user_movie_relation = UserMovieRelation.objects.create(
            user=self.user,
            movie=self.movie,
            like=True,
            rate=4,
            review='Great movie!',
        )

    def test_movie_model(self):
        # Проверяем, что модель Movie корректно создается
        self.assertEqual(self.movie.name, 'Test Movie')
        self.assertEqual(self.movie.genres.count(), 1)
        self.assertEqual(self.movie.crew.count(), 1)
        self.assertEqual(self.movie.owner, self.user)

    def test_movie_serializer(self):
        # Проверяем, что сериализатор MovieSerializer корректно представляет объект Movie
        serializer = MovieSerializer(instance=self.movie)
        data = serializer.data

        self.assertEqual(data['id'], self.movie.id)
        self.assertEqual(data['name'], 'Test Movie')
        self.assertEqual(data['genres'][0]['name'], 'Action')
        self.assertEqual(data['crew'][0]['person']['name'], 'John Doe')
        self.assertEqual(data['owner_name'], 'testuser')
        self.assertEqual(data['movies_reviews'][0]['review'], 'Great movie!')

