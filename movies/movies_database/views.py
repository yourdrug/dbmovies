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
    PersonsMoviesSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).select_related('owner').prefetch_related('watchers', 'actors', 'directors', 'producers',
                                               'screenwriters', 'composers', 'designers', 'editors',
                                               'operators', 'genres').order_by('id')
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
            match person.get("enProfession"):
                case "actor":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "actor"} not in some_person_professions:
                            if Profession.objects.filter(name="актёр").exists():
                                some_person.profession.add(Profession.objects.filter(name="актёр")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="актёр", en_name="actor"))
                        movie_temp.actors.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_actor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="актёр").exists():
                            temp_actor.profession.add(Profession.objects.filter(name="актёр")[0])
                        else:
                            temp_actor.profession.add(Profession.objects.create(name="актёр", en_name="actor"))
                        movie_temp.actors.add(temp_actor)

                case "director":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "director"} not in some_person_professions:
                            if Profession.objects.filter(name="режиссёр").exists():
                                some_person.profession.add(Profession.objects.filter(name="режиссёр")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="режиссёр", en_name="director"))
                        movie_temp.directors.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_director = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="режиссёр").exists():
                            temp_director.profession.add(Profession.objects.filter(name="режиссёр")[0])
                        else:
                            temp_director.profession.add(Profession.objects.create(name="режиссёр", en_name="director"))
                        movie_temp.directors.add(temp_director)

                case "producer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "producer"} not in some_person_professions:
                            if Profession.objects.filter(name="продюссер").exists():
                                some_person.profession.add(Profession.objects.filter(name="продюссер")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="продюссер", en_name="producer"))
                        movie_temp.producers.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_producer = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="продюссер").exists():
                            temp_producer.profession.add(Profession.objects.filter(name="продюссер")[0])
                        else:
                            temp_producer.profession.add(
                                Profession.objects.create(name="продюссер", en_name="producer"))
                        movie_temp.producers.add(temp_producer)

                case "writer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "writer"} not in some_person_professions:
                            if Profession.objects.filter(name="сценарист").exists():
                                some_person.profession.add(Profession.objects.filter(name="сценарист")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="сценарист", en_name="writer"))
                        movie_temp.screenwriters.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_writer = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="сценарист").exists():
                            temp_writer.profession.add(Profession.objects.filter(name="сценарист")[0])
                        else:
                            temp_writer.profession.add(Profession.objects.create(name="сценарист", en_name="writer"))
                        movie_temp.screenwriters.add(temp_writer)

                case "composer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "composer"} not in some_person_professions:
                            if Profession.objects.filter(name="композитор").exists():
                                some_person.profession.add(Profession.objects.filter(name="композитор")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="композитор", en_name="composer"))
                        movie_temp.composers.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_composer = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="композитор").exists():
                            temp_composer.profession.add(Profession.objects.filter(name="композитор")[0])
                        else:
                            temp_composer.profession.add(
                                Profession.objects.create(name="композитор", en_name="composer"))
                        movie_temp.composers.add(temp_composer)

                case "designer":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "designer"} not in some_person_professions:
                            if Profession.objects.filter(name="художник").exists():
                                some_person.profession.add(Profession.objects.filter(name="художник")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="художник", en_name="designer"))
                        movie_temp.designers.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_designer = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="художник").exists():
                            temp_designer.profession.add(Profession.objects.filter(name="художник")[0])
                        else:
                            temp_designer.profession.add(Profession.objects.create(name="художник", en_name="designer"))
                        movie_temp.designers.add(temp_designer)

                case "editor":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "editor"} not in some_person_professions:
                            if Profession.objects.filter(name="монтажёр").exists():
                                some_person.profession.add(Profession.objects.filter(name="монтажёр")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="монтажёр", en_name="editor"))
                        movie_temp.editors.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_editor = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="монтажёр").exists():
                            temp_editor.profession.add(Profession.objects.filter(name="монтажёр")[0])
                        else:
                            temp_editor.profession.add(Profession.objects.create(name="монтажёр", en_name="editor"))
                        movie_temp.editors.add(temp_editor)

                case "operator":
                    if Person.objects.filter(name=person.get("name")).exists():
                        some_person_professions = (
                            Person.objects.get(name=person.get("name")).profession.values("en_name"))
                        some_person = Person.objects.get(name=person.get("name"))
                        if {"en_name": "operator"} not in some_person_professions:
                            if Profession.objects.filter(name="оператор").exists():
                                some_person.profession.add(Profession.objects.filter(name="оператор")[0])
                            else:
                                some_person.profession.add(
                                    Profession.objects.create(name="оператор", en_name="operator"))
                        movie_temp.operators.add(Person.objects.get(name=person.get("name")))
                    else:
                        temp_operator = Person.objects.create(
                            name=person.get("name"),
                            photo=person.get("photo"),
                            en_name=person.get("enName")
                        )
                        if Profession.objects.filter(name="оператор").exists():
                            temp_operator.profession.add(Profession.objects.filter(name="оператор")[0])
                        else:
                            temp_operator.profession.add(Profession.objects.create(name="оператор", en_name="operator"))
                        movie_temp.operators.add(temp_operator)

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
    ).prefetch_related('actors', 'directors', 'genres').order_by('-world_premier')
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
