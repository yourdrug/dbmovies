from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession


class MovieWatcherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class MoviePersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PersonProfessionSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = ('name', 'en_name')


class ShortMoviePersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('name',)


class MovieGenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_count_rate = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    watchers = MovieWatcherSerializer(many=True, read_only=True)
    actors = MoviePersonSerializer(many=True, read_only=True)
    directors = MoviePersonSerializer(many=True, read_only=True)
    producers = MoviePersonSerializer(many=True, read_only=True)
    screenwriters = MoviePersonSerializer(many=True, read_only=True)
    composers = MoviePersonSerializer(many=True, read_only=True)
    designers = MoviePersonSerializer(many=True, read_only=True)
    editors = MoviePersonSerializer(many=True, read_only=True)
    operators = MoviePersonSerializer(many=True, read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'tagline', 'watch_time',
                  'year', 'country', 'poster', 'world_premier',
                  'annotated_likes', 'rating', 'owner_name',
                  'watchers', 'actors', 'directors', 'producers',
                  'screenwriters', 'composers', 'designers', 'editors',
                  'operators', 'genres', 'annotated_count_rate')


class ShortInfoMovieSerializer(ModelSerializer):
    annotated_count_rate = serializers.IntegerField(read_only=True)
    actors = ShortMoviePersonSerializer(many=True, read_only=True)
    directors = ShortMoviePersonSerializer(many=True, read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'watch_time', 'world_premier',
                  'year', 'country', 'poster', 'rating', 'actors',
                  'directors', 'genres', 'annotated_count_rate')


class ShortMovieForPersonSerializer(ModelSerializer):
    annotated_count_rate = serializers.IntegerField(read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'genres',
                  'poster', 'rating', 'annotated_count_rate')


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')


class PersonsMoviesSerializer(ModelSerializer):
    film_actor = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_director = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_producer = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_screenwriter = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_composer = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_designer = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_editor = ShortMovieForPersonSerializer(many=True, read_only=True)
    film_operator = ShortMovieForPersonSerializer(many=True, read_only=True)
    profession = PersonProfessionSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        # fields = ('id', 'name', 'photo', 'birth_day', 'death_day', 'movies')
        fields = '__all__'
