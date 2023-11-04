from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from movies_database.models import Movie, UserMovieRelation, Genre, Person, Profession
from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer, ShortInfoMovieSerializer, \
    PersonsMoviesSerializer, ProfessionSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).select_related('owner').prefetch_related('watchers', 'crew', 'genres').order_by('id')
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    filterset_fields = ['year', 'name', 'genres__name']
    search_fields = ['name', 'country', 'genres__name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    @action(detail=False, methods=['POST'])
    def addAllGenres(self, request):
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
                temp_genre = Genre.objects.create(name=genre.get("name"), en_name=genre.get("name"))
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
                                      name=person.get("profession"), en_name=person.get("enProfession"))

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
    ).prefetch_related('crew', 'genres').order_by('-world_premier')
    serializer_class = ShortInfoMovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'name', 'genres__en_name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)


class PersonInfoViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonsMoviesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)


class ProfessionViewSet(ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
