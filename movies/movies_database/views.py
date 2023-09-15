from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from movies_database.models import Movie, UserMovieRelation
from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from movies_database.serializers import MovieSerializer, UserMovieRelationSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['year', 'name']
    search_fields = ['name', 'country']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserMovieRelationViews(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserMovieRelation.objects.all()
    serializer_class = UserMovieRelationSerializer
    lookup_field = 'movie'

    def get_object(self):
        obj, _ = UserMovieRelation.objects.get_or_create(user=self.request.user,
                                                         movie_id=self.kwargs['movie'])
        return obj


def auth(request):
    return render(request, 'index.html')
