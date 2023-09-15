from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie, UserMovieRelation


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')
