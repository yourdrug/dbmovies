from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession


class MovieWatcherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class MovieGenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class PersonsMoviesSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'en_name')


class ProfessionSerializer(ModelSerializer):
    person = PersonsMoviesSerializer(read_only=True)

    class Meta:
        model = Profession
        fields = ('slug', 'person')


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_count_rate = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    genres = MovieGenreSerializer(many=True, read_only=True)
    crew = ProfessionSerializer(many=True, read_only=True, source='profession_set')

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'tagline', 'watch_time',
                  'year', 'country', 'poster', 'world_premier',
                  'annotated_likes', 'rating', 'owner_name', 'crew',
                  'genres', 'annotated_count_rate')


class ShortInfoMovieSerializer(ModelSerializer):
    annotated_count_rate = serializers.IntegerField(read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)
    crew = ProfessionSerializer(many=True, read_only=True, source='profession_set')
    user_rating = serializers.SerializerMethodField()

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_rating = obj.usermovierelation_set.filter(user=user).values('rate').first()

            if user_rating:
                return user_rating['rate']

        return None

    class Meta:
        model = Movie
        fields = ('id', 'name', 'watch_time', 'world_premier',
                  'year', 'country', 'poster', 'rating', 'crew',
                  'genres', 'user_rating', 'annotated_count_rate')


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate', 'is_watched', 'review')


class ProfessionPersonSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = ('slug',)


class MoviePersonsSerializer(ModelSerializer):
    genres = MovieGenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'watch_time', 'year', 'poster',
                  'rating', 'genres')


class PersonsSerializer(ModelSerializer):
    person_movies = MoviePersonsSerializer(many=True, read_only=True)
    professions = ProfessionPersonSerializer(many=True, read_only=True, source='profession_set')

    class Meta:
        model = Person
        fields = ('id', 'name', 'en_name', 'photo', 'birth_day',
                  'death_day', 'person_movies', 'professions')


class PersonProfessionSerializer(ModelSerializer):
    person = PersonsMoviesSerializer(read_only=True)
    movie = MoviePersonsSerializer(read_only=True)

    class Meta:
        model = Profession
        fields = ('slug', 'person', 'movie')
