<template>
  <div class="container">
    <div class="wrapper">
      <div class="wrapper-col-1">
        <img :src="this.movie.poster" :alt="this.movie.name" />
      </div>
      <!-- /.wrapper-col-1 -->

      <div class="wrapper-col-2">
        <h1 class="title">{{ this.movie.name }}</h1>
        <p class="description">
          {{ this.movie.description }}
        </p>

        <h2>О фильме</h2>

        <ul class="params">
          <li>
            <span class="text-muted">Год производства</span>
            {{ this.movie.year }}
          </li>
          <li>
            <span class="text-muted">Страна</span> {{ this.movie.country }}
          </li>
          <li>
            <span class="text-muted">Жанр</span>
            <span>
              <div class="genre" v-for="genre in movie.genres" :key="genre.id">
                <div v-if="genre != movie.genres[movie.genres.length - 1]">
                  <a @click="$router.push('/movies/by-genre/' + genre.en_name)">
                    {{ genre.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/movies/by-genre/' + genre.en_name)">
                    {{ genre.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Слоган</span>
            <span class="text-muted">{{ this.movie.tagline }}</span>
          </li>
          <li>
            <span class="text-muted">Режиссёр</span>
            <span>
              <div
                class="director"
                v-for="director in movie.director"
                :key="director.id"
              >
                <div
                  v-if="director != movie.director[movie.director.length - 1]"
                >
                  <a @click="$router.push('/persons/director/' + director.id)">
                    {{ director.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/director/' + director.id)">
                    {{ director.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Продюссер</span>
            <span>
              <div
                class="director"
                v-for="producer in movie.producer"
                :key="producer.id"
              >
                <div
                  v-if="producer != movie.producer[movie.producer.length - 1]"
                >
                  <a @click="$router.push('/persons/producer/' + producer.id)">
                    {{ producer.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/producer/' + producer.id)">
                    {{ producer.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Сценарий</span>
            <span>
              <div
                class="director"
                v-for="screenwriter in movie.screenwriter"
                :key="screenwriter.id"
              >
                <div
                  v-if="
                    screenwriter !=
                    movie.screenwriter[movie.screenwriter.length - 1]
                  "
                >
                  <a
                    @click="
                      $router.push('/persons/screenwriter/' + screenwriter.id)
                    "
                  >
                    {{ screenwriter.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a
                    @click="
                      $router.push('/persons/screenwriter/' + screenwriter.id)
                    "
                  >
                    {{ screenwriter.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Время</span>
            <time class="text-muted">
              {{ this.movie.watch_time }}
            </time>
          </li>
          <li>
            <span class="text-muted">Премьера в мире</span>
            <time class="text-muted">
              {{ this.movie.world_premier }}
            </time>
          </li>
        </ul>
      </div>
      <!-- /.wrapper-col-2 -->

      <div class="wrapper-col-3">
        <span
          class="rathing-main"
          v-if="movie.rating >= 7.5"
          style="color: green"
        >
          {{ movie.rating }}
        </span>
        <span
          class="rathing-main"
          v-if="movie.rating <= 5.5"
          style="color: red"
        >
          {{ movie.rating }}
        </span>
        <span
          class="rathing-main"
          v-if="movie.rating < 7.5 && movie.rating > 5.5"
          style="color: grey"
        >
          {{ movie.rating }}
        </span>
        <span class="rathing-counts">{{
          this.movie.annotated_count_rate
        }}</span>
        <a href="#" class="rathing-details">459 рецензий</a>
      </div>
      <!-- /.wrapper-col-3 -->
    </div>
    <!-- /.wrapper -->
  </div>
  <!-- /.container -->
</template>

<script>
export default {
  props: {
    movie: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

img {
  width: 100%;
  border-radius: 10px;
}

a {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

a:hover {
  color: #ff5c00;
  cursor: pointer;
}

h2 {
  margin-bottom: 20px;
  font-weight: 900;
  font-size: 22px;
}

.container {
  width: 1100px;
  max-width: 100%;
  margin: 0 auto;
}

.genre {
  display: inline-block;
}

.director {
  display: inline-block;
}

.wrapper {
  display: grid;
  grid-template-columns: 340px 530px 150px;
  grid-gap: 40px;
  padding-top: 80px;
  padding-bottom: 80px;
}

.title {
  font-size: 36px;
  font-weight: 900;
  margin-bottom: 10px;
  padding-top: 20px;
  line-height: 42px;
}

.subtitle {
  margin-bottom: 10px;
  opacity: 0.4;
  line-height: 19px;
  font-size: 16px;
  font-weight: 400;
}

.description {
  margin-bottom: 30px;
  text-align: justify;
}

.mb-40 {
  margin-bottom: 40px;
}

.btn {
  background-color: #ff5c00;
  padding: 10px 30px;
  display: inline-block;
  font-weight: 500;
  font-size: 18px;
  line-height: 21px;
  border-radius: 100px;
  color: #fff !important;
  transition: all 200ms ease-in-out;
}

.params {
  list-style-type: none;
}

.params li {
  margin-bottom: 15px;
  display: grid;
  grid-template-columns: 130px 1fr;
  grid-gap: 30px;
  width: 100%;
  font-size: 14px;
}

.tag {
  font-size: 12px;
  font-weight: 400;
  padding: 3px 5px;
  border-radius: 6px;
  border: 1px solid #ffffff;
  display: inline-block;
  margin-top: -3px;
}

.text-muted {
  opacity: 0.4;
}

.rathing-main {
  display: block;
  margin-bottom: 10px;
  font-weight: 900;
  font-size: 36px;
  line-height: 42px;
}

.rathing-counts {
  display: block;
  margin-bottom: 10px;
  line-height: 19px;
  opacity: 0.4;
}

.rathing-details {
  display: inline-block;
}

@media (max-width: 1024px) {
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }

  .wrapper {
    grid-template-columns: 250px 1fr 150px;
    grid-gap: 30px;
  }
}

@media (max-width: 768px) {
  .wrapper {
    grid-template-columns: 1fr 150px;
    max-width: 520px;
    margin-left: auto;
    margin-right: auto;
  }

  .wrapper-col-3 {
    grid-row: 1 / 3;
    grid-column: 2;
  }
}

@media (max-width: 425px) {
  .wrapper {
    grid-template-columns: 1fr;
    max-width: 100%;
  }

  .wrapper-col-3 {
    grid-row: unset;
    grid-column: 1;
  }
}
</style>
