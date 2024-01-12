from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.serializers import CurrentUserInfoSerializer
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
        fields = ('slug', 'person', 'image')


class LittleMovieCardSerializer(ModelSerializer):
    annotated_count_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'country', 'poster', 'rating', 'annotated_count_rate')

    def get_annotated_count_rate(self, obj):
        queryset = Movie.objects.filter(id=obj.id)

        # Аннотируем count_rate
        from django.db.models import Count
        from django.db.models import Case
        from django.db.models import When

        annotated_queryset = queryset.annotate(
            annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
        )

        # Возвращаем значение для текущего объекта
        return annotated_queryset.first().annotated_count_rate if annotated_queryset.exists() else 0


class ReviewsSerializer(serializers.ModelSerializer):
    user = CurrentUserInfoSerializer(read_only=True)

    class Meta:
        model = UserMovieRelation
        fields = ('review', 'user')


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_count_rate = serializers.IntegerField(read_only=True)
    annotated_count_review = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    genres = MovieGenreSerializer(many=True, read_only=True)
    crew = ProfessionSerializer(many=True, read_only=True, source='profession_set')

    movies_reviews = ReviewsSerializer(many=True, read_only=True, source='usermovierelation_set')

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'tagline', 'watch_time',
                  'year', 'country', 'poster', 'world_premier',
                  'annotated_likes', 'rating', 'owner_name', 'crew',
                  'genres', 'annotated_count_rate', 'annotated_count_review', 'movies_reviews')


class ShortInfoMovieSerializer(ModelSerializer):
    annotated_count_rate = serializers.IntegerField(read_only=True)
    genres = MovieGenreSerializer(many=True, read_only=True)
    crew = ProfessionSerializer(many=True, read_only=True, source='profession_set')
    user_rating = serializers.SerializerMethodField()
    user_like = serializers.SerializerMethodField()
    user_is_watched = serializers.SerializerMethodField()
    user_is_in_bookmark = serializers.SerializerMethodField()
    user_will_watch = serializers.SerializerMethodField()

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_rating = obj.usermovierelation_set.filter(user=user).values('rate').first()

            if user_rating:
                return user_rating['rate']

        return None

    def get_user_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_like = obj.usermovierelation_set.filter(user=user).values('like').first()

            if user_like:
                return user_like['like']

        return None

    def get_user_is_watched(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_is_watched = obj.usermovierelation_set.filter(user=user).values('is_watched').first()

            if user_is_watched:
                return user_is_watched['is_watched']

        return None

    def get_user_is_in_bookmark(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_is_in_bookmark = obj.usermovierelation_set.filter(user=user).values('in_bookmarks').first()

            if user_is_in_bookmark:
                return user_is_in_bookmark['in_bookmarks']

        return None

    def get_user_will_watch(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            user_is_in_bookmark = obj.usermovierelation_set.filter(user=user).values('will_watch').first()

            if user_is_in_bookmark:
                return user_is_in_bookmark['will_watch']

        return None

    class Meta:
        model = Movie
        fields = ('id', 'name', 'watch_time', 'world_premier',
                  'year', 'country', 'poster', 'rating', 'crew',
                  'genres', 'user_rating', 'user_is_watched', 'user_like',
                  'user_is_in_bookmark', 'user_will_watch', 'annotated_count_rate')


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate', 'is_watched', 'will_watch', 'review')


class UserMovieRelationForUserSerializer(ModelSerializer):
    movie = LittleMovieCardSerializer(read_only=True)

    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate', 'is_watched', 'will_watch', 'review')


class ProfessionPersonSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = ('slug',)


class PersonProfessionSerializer(ModelSerializer):
    # person = PersonsMoviesSerializer(read_only=True)
    movie = LittleMovieCardSerializer(read_only=True)

    class Meta:
        model = Profession
        fields = ('slug', 'movie')


class PersonsSerializer(ModelSerializer):
    # person_movies = MoviePersonsSerializer(many=True, read_only=True)
    professions = PersonProfessionSerializer(many=True, read_only=True, source='profession_set')

    class Meta:
        model = Person
        fields = ('id', 'name', 'en_name', 'photo', 'birth_day',
                  'death_day', 'professions')
