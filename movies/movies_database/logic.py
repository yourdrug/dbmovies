from django.db.models import Avg

from movies_database.models import UserMovieRelation


def set_rating(movie):
    rating = UserMovieRelation.objects.filter(movie=movie).aggregate(rating=Avg('rate')).get('rating')
    movie.rating = rating
    movie.save()


