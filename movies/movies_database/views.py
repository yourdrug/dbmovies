from django.db.models import Count, Case, When, Sum
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from cacheops import cached_view_as
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from movies_database.movie_db import MovieDb

from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession
from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer, ShortInfoMovieSerializer, \
    PersonsMoviesSerializer, ProfessionSerializer, MovieGenreSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).select_related('owner').prefetch_related('watchers', 'profession_set__person', 'genres').order_by('id')
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    filterset_fields = ['year', 'name', 'genres__name']
    search_fields = ['name', 'country', 'genres__name']

    # @method_decorator(cached_view_as(Movie))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        if not request.user.is_authenticated:
            total_likes = None
        else:
            likes_cache_name = 'likes_cache'
            likes_cache = cache.get(likes_cache_name)

            if likes_cache:
                total_likes = likes_cache
            else:
                total_likes = queryset.aggregate(total=Sum(Case(
                    When(usermovierelation__like=True, usermovierelation__user=request.user, then=1)))).get('total')
                cache.set(likes_cache_name, total_likes, 60)
        response_data = {'total_likes': total_likes, 'result': response.data}
        response.data = response_data

        return response

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    @action(detail=False, methods=['POST'])
    def addAllGenres(self, request):
        for genre in request.data.get("movies"):
            if Genre.objects.filter(name=genre.get("name")).exists():
                temp_genre = Genre.objects.get(name=genre.get("name"))
                temp_genre.slug = genre.get("slug")
                temp_genre.save()
            else:
                Genre.objects.create(name=genre.get("name"), slug=genre.get("slug"))
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def addMovies(self, request):
        # for i in range(30):
        movie_temp = Movie.objects.create(
            name=request.data.get("movies").get("name"),
            description=request.data.get("movies").get("description"),
            year=request.data.get("movies").get("year"),
            watch_time=request.data.get("movies").get("movieLength"),
            country=request.data.get("movies").get("countries")[0].get("name"),
            tagline=request.data.get("movies").get("slogan"),
            poster=request.data.get("movies").get("poster").get("url"),
            world_premier=request.data.get("movies").get("premiere").get("world").split("T")[0]
        )
        for genre in request.data.get("movies").get("genres"):
            if Genre.objects.filter(name=genre.get("name")).exists():
                movie_temp.genres.add(Genre.objects.get(name=genre.get("name")))
            else:
                temp_genre = Genre.objects.create(name=genre.get("name"), slug=genre.get("name"))
                movie_temp.genres.add(temp_genre)

        for person in request.data.get("movies").get("persons"):
            if Person.objects.filter(name=person.get("name")).exists():
                temp_person = Person.objects.get(name=person.get("name"))
            else:
                temp_person = Person.objects.create(
                    name=person.get("name"),
                    photo=person.get("photo"),
                    en_name=person.get("enName"),
                )
            Profession.objects.create(person=temp_person, movie=movie_temp,
                                      name=person.get("profession"), slug=person.get("enProfession"))

        return Response(status=status.HTTP_201_CREATED)


class UserMovieRelationViews(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = UserMovieRelation.objects.all()
    serializer_class = UserMovieRelationSerializer
    lookup_field = 'movie'

    def get_object(self):
        obj, _ = UserMovieRelation.objects.get_or_create(user=self.request.user,
                                                         movie_id=self.kwargs['movie'])
        return obj


class ShortInfoMovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).prefetch_related('profession_set__person', 'genres').order_by('-world_premier')
    serializer_class = ShortInfoMovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'name', 'genres__name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    @method_decorator(cached_view_as(Movie))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PersonInfoViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonsMoviesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)


class PersonViewSet(viewsets.ViewSet):
    def list(self, request):
        my_db = MovieDb()
        data = my_db.execute_query(
            """SELECT "movies_database_movie"."id",
            "movies_database_movie"."name",
            "movies_database_movie"."description",
            "movies_database_movie"."tagline",
            "movies_database_movie"."year",
            "movies_database_movie"."country",
            "movies_database_movie"."watch_time",
            "movies_database_movie"."poster",
            "movies_database_movie"."world_premier",
            "movies_database_movie"."rating",
            "movies_database_usermovierelation"."like",
            COUNT(CASE WHEN "movies_database_usermovierelation"."rate" IS NOT NULL THEN 1 ELSE NULL END)
            FROM "movies_database_movie"
            LEFT OUTER JOIN "movies_database_usermovierelation"
            ON ("movies_database_movie"."id" = "movies_database_usermovierelation"."movie_id")
            GROUP BY "movies_database_movie"."id", "movies_database_usermovierelation"."like"
            ORDER BY "movies_database_movie"."id" """
            )
        queryset = data
        return Response(queryset)


class ProfessionViewSet(ModelViewSet):
    queryset = Genre.objects.all().prefetch_related('film_genres')
    serializer_class = MovieGenreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
