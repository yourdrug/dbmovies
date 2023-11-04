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


class ProfessionSerializer(ModelSerializer):
    # person = PersonsMoviesSerializer(read_only=True)

    class Meta:
        model = Profession
        fields = ('name', 'en_name')


class PersonsMoviesSerializer(ModelSerializer):
    professions = ProfessionSerializer(many=True, source='profession_set.all', read_only=True)

    class Meta:
        model = Person
        # fields = ('id', 'name', 'photo', 'birth_day', 'death_day', 'movies')
        fields = '__all__'


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_count_rate = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    watchers = MovieWatcherSerializer(many=True, read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)
    # crew = PersonsMoviesSerializer(many=True, read_only=True)
    actors = serializers.SerializerMethodField('get_actors')
    directors = serializers.SerializerMethodField('get_directors')
    producers = serializers.SerializerMethodField('get_producers')
    writers = serializers.SerializerMethodField('get_writers')
    composers = serializers.SerializerMethodField('get_composers')
    editors = serializers.SerializerMethodField('get_editors')
    designers = serializers.SerializerMethodField('get_designers')
    operators = serializers.SerializerMethodField('get_operators')

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'tagline', 'watch_time',
                  'year', 'country', 'poster', 'world_premier',
                  'annotated_likes', 'rating', 'owner_name',
                  'watchers', 'actors', 'directors', 'producers', 'writers', 'composers', 'editors',
                  'designers', 'operators', 'genres', 'annotated_count_rate')

    def get_actors(self, obj):
        # Извлеките информацию об актерах в фильме и верните ее в виде списка объектов
        actors = Profession.objects.filter(movie=obj, en_name='actor')
        actor_data = [{'id': actor.person.id, 'name': actor.person.name} for actor in actors]
        return actor_data

    def get_directors(self, obj):
        # Извлеките информацию о режиссерах в фильме и верните ее в виде списка объектов
        directors = Profession.objects.filter(movie=obj, en_name='director')
        director_data = [{'id': director.person.id, 'name': director.person.name} for director in directors]
        return director_data

    def get_producers(self, obj):
        producers = Profession.objects.filter(movie=obj, en_name='producer')
        producer_data = [{'id': producer.person.id, 'name': producer.person.name} for producer in producers]
        return producer_data

    def get_composers(self, obj):
        composers = Profession.objects.filter(movie=obj, en_name='composer')
        composer_data = [{'id': composer.person.id, 'name': composer.person.name} for composer in composers]
        return composer_data

    def get_writers(self, obj):
        writers = Profession.objects.filter(movie=obj, en_name='writer')
        writer_data = [{'id': writer.person.id, 'name': writer.person.name} for writer in writers]
        return writer_data

    def get_editors(self, obj):
        editors = Profession.objects.filter(movie=obj, en_name='editor')
        editor_data = [{'id': editor.person.id, 'name': editor.person.name} for editor in editors]
        return editor_data

    def get_designers(self, obj):
        designers = Profession.objects.filter(movie=obj, en_name='designer')
        designer_data = [{'id': designer.person.id, 'name': designer.person.name} for designer in designers]
        return designer_data

    def get_operators(self, obj):
        operators = Profession.objects.filter(movie=obj, en_name='operator')
        operator_data = [{'id': operator.person.id, 'name': operator.person.name} for operator in operators]
        return operator_data


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
        # Извлеките информацию об актерах в фильме и верните ее в виде списка объектов
        actors = Profession.objects.filter(movie=obj, en_name='actor')
        actor_data = [{'id': actor.person.id, 'name': actor.person.name} for actor in actors]
        return actor_data

    def get_directors(self, obj):
        # Извлеките информацию о режиссерах в фильме и верните ее в виде списка объектов
        directors = Profession.objects.filter(movie=obj, en_name='director')
        director_data = [{'id': director.person.id, 'name': director.person.name} for director in directors]
        return director_data


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')
