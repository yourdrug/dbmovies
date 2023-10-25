from django.db.models import Count, Case, When, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from movies_database.models import Movie, UserMovieRelation
from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer, ShortInfoMovieSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().annotate(
        annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
        annotated_count_rate=Count(Case(When(usermovierelation__rate__isnull=False, then=1)))
    ).select_related('owner').prefetch_related('watchers', 'actors', 'director', 'producer', 'screenwriter', 'genres').order_by('id')
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    filterset_fields = ['year', 'name', 'genres__name']
    search_fields = ['name', 'country', 'genres__name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


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
    filterset_fields = ['year', 'name', 'genres__en_name']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
