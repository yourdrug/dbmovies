from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession


class MovieWatcherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class MovieGenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PersonsMoviesSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ProfessionSerializer(ModelSerializer):
    person = PersonsMoviesSerializer(read_only=True)

    class Meta:
        model = Profession
        fields = ('name', 'slug', 'person')


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_count_rate = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    watchers = MovieWatcherSerializer(many=True, read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)
    crew = ProfessionSerializer(many=True, read_only=True, source='profession_set')

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'tagline', 'watch_time',
                  'year', 'country', 'poster', 'world_premier',
                  'annotated_likes', 'rating', 'owner_name', 'crew',
                  'watchers', 'genres', 'annotated_count_rate')

    def get_crew(self, obj):
        persons = Profession.objects.filter(movie=obj)
        persons_data = [{'id': person.person.id, 'name': person.person.name, 'profession': person.slug} for person in
                        persons]
        return persons_data


class ShortInfoMovieSerializer(ModelSerializer):
    annotated_count_rate = serializers.IntegerField(read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)
    actors = serializers.SerializerMethodField('get_actors')
    directors = serializers.SerializerMethodField('get_directors')

    class Meta:
        model = Movie
        fields = ('id', 'name', 'watch_time', 'world_premier',
                  'year', 'country', 'poster', 'rating', 'actors', 'directors',
                  'genres', 'annotated_count_rate')

    def get_actors(self, obj):
        actors = Profession.objects.filter(movie=obj, slug='actor')
        actor_data = [{'id': actor.person.id, 'name': actor.person.name} for actor in actors]
        return actor_data

    def get_directors(self, obj):
        directors = Profession.objects.filter(movie=obj, slug='director')
        director_data = [{'id': director.person.id, 'name': director.person.name} for director in directors]
        return director_data


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')
