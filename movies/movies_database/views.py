import random

from django.core.cache import cache
from django.db.models import Count, Case, When
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.views.decorators.cache import never_cache, cache_page
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession
from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer, ShortInfoMovieSerializer, \
    PersonsSerializer, PersonProfessionSerializer


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

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        if not Movie.objects.filter(name=request.data.get("movies").get("name")).exists():
            max_desc = 1495
            max_tagline = 195
            desc = request.data.get("movies").get("description")
            tagline = request.data.get("movies").get("slogan")
            points = "..."
            short_tag = "-"
            short_desc = "-"
            if desc is not None:
                short_desc = desc[:max_desc] + (points if len(desc) > max_desc else "")
            if tagline is not None:
                short_tag = tagline[:max_tagline] + (points if len(tagline) > max_tagline else "")

            movie_temp = Movie.objects.create(
                name=request.data.get("movies").get("name"),
                description=short_desc,
                year=request.data.get("movies").get("year"),
                watch_time=request.data.get("movies").get("movieLength"),
                country=request.data.get("movies").get("countries")[0].get("name"),
                tagline=short_tag,
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

    @action(detail=False, methods=['GET'])
    @method_decorator(never_cache)
    def randomMovie(self, request):
        data = self.get_queryset()
        ids = data.values('id')
        random_id = random.choice(ids)
        random_movie = data.get(id=random_id.get("id"))
        serializer = self.get_serializer(random_movie)
        return Response(serializer.data)


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


class MoviesPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 200


class ShortInfoMovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).prefetch_related('profession_set__person', 'genres').order_by('id')
    serializer_class = ShortInfoMovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'name', 'genres__name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    pagination_class = MoviesPagination

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PersonInfoViewSet(ModelViewSet):
    queryset = Person.objects.all().prefetch_related('person_movies', 'person_movies__genres')
    serializer_class = PersonsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)


class ProfessionViewSet(ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = PersonProfessionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['person_id']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
