from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie, UserMovieRelation


class MovieWatcherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class MovieSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    owner_name = serializers.CharField(read_only=True, source='owner.username', default="")
    watchers = MovieWatcherSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'country', 'annotated_likes', 'rating', 'owner_name', 'watchers')


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')
