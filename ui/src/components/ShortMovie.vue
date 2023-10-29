<template>
  <div class="movie-card" @click="$router.push('/movies/' + this.movie.id)">
    <div class="number">{{ index + 1 }}</div>
    <div class="poster">
      <img :src="movie.poster" />
    </div>
    <div class="movie-info">
      <div class="movie-name">{{ movie.name }}</div>
      <div class="movie-desc">
        {{ movie.year }}, {{ movie.watch_time.split("/")[0] }}
      </div>
      <div class="movie-more-desc">
        {{ movie.country.split(",")[0] }} | {{ movie.genres[0].name }}
        &nbsp;Режиссёр:
        {{ movie.directors[0].name }} <br />
        <br />
        В ролях: {{ movie.actors[0].name }}, {{ movie.actors[1].name }}
      </div>
    </div>
    <div class="additional-info">
      <div class="movie-rate" v-if="movie.rating >= 7.5" style="color: green">
        {{ movie.rating }}
      </div>
      <div class="movie-rate" v-if="movie.rating <= 5.5" style="color: red">
        {{ movie.rating }}
      </div>
      <div
        class="movie-rate"
        v-if="movie.rating < 7.5 && movie.rating > 5.5"
        style="color: grey"
      >
        {{ movie.rating }}
      </div>
      <div class="count-rates">{{ movie.annotated_count_rate }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    movie: {
      type: Object,
      required: true,
    },

    index: {
      type: Number,
      required: false,
    },
  },

  methods: {},
};
</script>

<style>
.number {
  margin-top: 50px;
  margin-left: 5px;
  font-size: 20px;
  font-weight: bold;
}

.movie-card {
  /*background-color: rgb(214, 213, 213);*/
  width: 800px;
  height: 215px;
  text-align: center;
  border-bottom: 1px solid black;
  margin-top: 5px;
  cursor: pointer;
  display: grid;
  grid-template-columns: 40px 150px 350px 260px;
}

.poster {
  width: 150px;
  height: 180px;
  margin-top: 15px;
}

.poster img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.movie-info {
  text-align: left;
  margin-top: 20px;
  margin-left: 15px;
}

.movie-rate {
  margin-top: 15px;
  font-size: 20px;
  font-weight: bold;
  width: 40px;
  display: inline-block;
}

.count-rates {
  display: inline-block;
  text-align: left;
  margin-left: 10px;
  margin-top: 17px;
  width: 50px;
  font-size: 12px;
  font-weight: 100;
}

.additional-info {
  overflow: hidden;
  white-space: nowrap;
}

.movie-name {
  font-size: 24px;
  color: black;
  font-weight: bold;
}

.movie-desc {
  font-size: 14px;
  margin-top: 10px;
  color: black;
}

.movie-more-desc {
  font-size: 14px;
  margin-top: 16px;
  color: grey;
}
</style>
