from rest_framework.serializers import ModelSerializer

from movies_database.models import Movie


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
