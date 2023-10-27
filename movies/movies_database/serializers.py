from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie, UserMovieRelation, Actor, Director, Producer, Screenwriter, Genre


class MovieWatcherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class MovieActorsSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class ShortMovieActorsSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name',)


class MovieDirectorSerializer(ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class ShortMovieDirectorSerializer(ModelSerializer):
    class Meta:
        model = Director
        fields = ('name',)


class MovieProducerSerializer(ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'


class MovieScreenwriterSerializer(ModelSerializer):
    class Meta:
        model = Screenwriter
        fields = '__all__'


class MovieGenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_count_rate = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    watchers = MovieWatcherSerializer(many=True, read_only=True)
    actors = MovieActorsSerializer(many=True, read_only=True)
    director = MovieDirectorSerializer(many=True, read_only=True)
    producer = MovieProducerSerializer(many=True, read_only=True)
    screenwriter = MovieScreenwriterSerializer(many=True, read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'tagline', 'watch_time',
                  'year', 'country', 'poster', 'world_premier',
                  'annotated_likes', 'rating', 'owner_name',
                  'watchers', 'actors', 'director', 'producer',
                  'screenwriter', 'genres', 'annotated_count_rate')


class ShortInfoMovieSerializer(ModelSerializer):
    annotated_count_rate = serializers.IntegerField(read_only=True)
    actors = ShortMovieActorsSerializer(many=True, read_only=True)
    director = ShortMovieDirectorSerializer(many=True, read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'watch_time', 'world_premier',
                  'year', 'country', 'poster', 'rating', 'actors',
                  'director', 'genres', 'annotated_count_rate')


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')


class ActorSerializer(ModelSerializer):
    film_actor = ShortInfoMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        # fields = ('id', 'name', 'photo', 'birth_day', 'death_day', 'movies')
        fields = '__all__'
