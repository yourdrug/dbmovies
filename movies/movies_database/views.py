from django.db.models import Count, Case, When, Avg
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
    PersonsMoviesSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).select_related('owner').prefetch_related('watchers', 'actors', 'director', 'producer', 'screenwriter',
                                               'genres').order_by('id')
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
            if Genre.objects.get(name=genre.get("name")).exists():
                movie_temp.genres.add(Genre.objects.get(name=genre.get("name")))
            else:
                temp_genre = Genre.objects.create(name=genre.get("name"), en_name=genre.get("name"))
                movie_temp.genres.add(temp_genre)

        for person in request.data.get("movies").get("persons"):
            match person.get("enProfession"):
                case "actor":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="актёр", en_name="actor"))
                        movie_temp.actors.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="актёр", en_name="actor"))
                        movie_temp.actors.add(temp_actor)

                case "director":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="режиссёр", en_name="director"))
                        movie_temp.directors.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="режиссёр", en_name="director"))
                        movie_temp.directors.add(temp_actor)

                case "producer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="продюссер", en_name="producer"))
                        movie_temp.producers.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="продюссер", en_name="producer"))
                        movie_temp.producers.add(temp_actor)

                case "writer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="сценарист", en_name="writer"))
                        movie_temp.screenwriters.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="сценарист", en_name="writer"))
                        movie_temp.screenwriters.add(temp_actor)

                case "composer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="композитор", en_name="composer"))
                        movie_temp.composers.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="композитор", en_name="composer"))
                        movie_temp.composers.add(temp_actor)

                case "designer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="художник", en_name="designer"))
                        movie_temp.designers.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="художник", en_name="designer"))
                        movie_temp.designers.add(temp_actor)

                case "editor":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="монтажёр", en_name="editor"))
                        movie_temp.editors.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="монтажёр", en_name="editor"))
                        movie_temp.editors.add(temp_actor)

                case "operator":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = Person.objects.get(name=person.get("name")).profession.all()
                        some_person = Person.objects.get(name=person.get("name"))
                        if "actor" not in some_person_professions.en_name:
                            some_person.profession.add(Profession.objects.get_or_create(name="оператор", en_name="operator"))
                        movie_temp.operators.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo")
                        )
                        temp_actor.profession.add(Profession.objects.get_or_create(name="оператор", en_name="operator"))
                        movie_temp.operators.add(temp_actor)

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
    ).prefetch_related('actors', 'director', 'genres').order_by('-world_premier')
    serializer_class = ShortInfoMovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'name', 'genres__en_name', 'actors__name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)


class PersonInfoViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonsMoviesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)

