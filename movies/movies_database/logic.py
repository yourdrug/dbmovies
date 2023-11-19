from django.db.models import Avg
from django_pandas.io import read_frame
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from movies_database.models import UserMovieRelation


def set_rating(movie):
    rating = UserMovieRelation.objects.filter(movie=movie).aggregate(rating=Avg('rate')).get('rating')
    movie.rating = rating
    movie.save()


def prep_data():
    db_data = UserMovieRelation.objects.values('movie__id', 'user__id', 'rate')
    data = read_frame(db_data)
    df = pd.DataFrame(data=data)
    user_item_matrix = df.pivot(index='movie__id', columns='user__id', values='rate')
    user_item_matrix.fillna(0, inplace=True)

    # сгруппируем пользователей, возьмем только столбец rate
    # и посчитаем, сколько было оценок у каждого пользователя
    users_votes = df.groupby('user__id')['rate'].agg('count')
    # так же для фильмов
    movies_votes = df.groupby('movie__id')['rate'].agg('count')

    user_mask = users_votes[users_votes > 1].index  # делаем маски чтобы у пользователя было 50 голосов
    movie_mask = movies_votes[movies_votes > 0].index  # а для фильмов больше 10

    # применим фильтры и отберем фильмы с достаточным количеством оценок
    user_item_matrix = user_item_matrix.loc[movie_mask, :]
    # а также активных пользователей
    user_item_matrix = user_item_matrix.loc[:, user_mask]
    user_item_matrix = user_item_matrix.rename_axis(None, axis=1).reset_index()
    user_item_matrix = user_item_matrix.astype(float)
    return user_item_matrix


def get_csr_data(user_item_matrix):
    # user_item_matrix = prep_data()
    csr_data = csr_matrix(user_item_matrix.values)
    return csr_data


def train_model(csr_data):
    # csr_data = get_csr_data()
    knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    # обучим модель
    knn_model.fit(csr_data)

    import pickle
    pickle.dump(knn_model, open("movie_ml_model.sav", "wb"))
