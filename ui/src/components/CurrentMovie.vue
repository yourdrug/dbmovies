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
                v-for="director in movie.directors"
                :key="director.id"
              >
                <div
                  v-if="director != movie.directors[movie.directors.length - 1]"
                >
                  <a @click="$router.push('/persons/' + director.id)">
                    {{ director.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + director.id)">
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
                v-for="producer in movie.producers"
                :key="producer.id"
              >
                <div
                  v-if="producer != movie.producers[movie.producers.length - 1]"
                >
                  <a @click="$router.push('/persons/' + producer.id)">
                    {{ producer.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + producer.id)">
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
                v-for="screenwriter in movie.screenwriters"
                :key="screenwriter.id"
              >
                <div
                  v-if="
                    screenwriter !=
                    movie.screenwriters[movie.screenwriters.length - 1]
                  "
                >
                  <a @click="$router.push('/persons/' + screenwriter.id)">
                    {{ screenwriter.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + screenwriter.id)">
                    {{ screenwriter.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Композитор</span>
            <span>
              <div
                class="director"
                v-for="composer in movie.composers"
                :key="composer.id"
              >
                <div
                  v-if="composer != movie.composers[movie.composers.length - 1]"
                >
                  <a @click="$router.push('/persons/' + composer.id)">
                    {{ composer.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + composer.id)">
                    {{ composer.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Оператор</span>
            <span>
              <div
                class="director"
                v-for="operator in movie.operators"
                :key="operator.id"
              >
                <div
                  v-if="operator != movie.operators[movie.operators.length - 1]"
                >
                  <a @click="$router.push('/persons/' + operator.id)">
                    {{ operator.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + operator.id)">
                    {{ operator.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Художник</span>
            <span>
              <div
                class="director"
                v-for="designer in movie.designers"
                :key="designer.id"
              >
                <div
                  v-if="designer != movie.designers[movie.designers.length - 1]"
                >
                  <a @click="$router.push('/persons/' + designer.id)">
                    {{ designer.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + designer.id)">
                    {{ designer.name }}</a
                  >
                </div>
              </div>
            </span>
          </li>
          <li>
            <span class="text-muted">Монтажёр</span>
            <span>
              <div
                class="director"
                v-for="editor in movie.editors"
                :key="editor.id"
              >
                <div v-if="editor != movie.editors[movie.editors.length - 1]">
                  <a @click="$router.push('/persons/' + editor.id)">
                    {{ editor.name }},&nbsp;</a
                  >
                </div>
                <div v-else>
                  <a @click="$router.push('/persons/' + editor.id)">
                    {{ editor.name }}</a
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
  background-color: lightgray;
}

.wrapper-col-1 {
  background-color: white;
}

.wrapper-col-2 {
  background-color: white;
}

.wrapper-col-3 {
  background-color: white;
}

img {
  width: 100%;
  border-radius: 10px;
  background-color: white;
}

span {
  background-color: white;
}

a {
  color: black;
  text-decoration: none;
  cursor: pointer;
  background-color: white;
}

a:hover {
  color: #ff5c00;
  cursor: pointer;
  background-color: white;
}

h2 {
  margin-bottom: 20px;
  font-weight: 900;
  font-size: 22px;
  background-color: white;
}

.container {
  width: 1230px;
  max-width: 100%;
  margin: 0 auto;
  background-color: white;
}

.genre {
  display: inline-block;
  background-color: white;
}

.director {
  display: inline-block;
  text-align: justify;
  background-color: white;
}

.wrapper {
  display: grid;
  grid-template-columns: 350px 600px 160px;
  grid-gap: 40px;
  padding-top: 80px;
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 80px;
  background-color: white;
}

.title {
  font-size: 36px;
  font-weight: 900;
  margin-bottom: 10px;
  padding-top: 20px;
  line-height: 42px;
  background-color: white;
}

.subtitle {
  margin-bottom: 10px;
  opacity: 0.4;
  line-height: 19px;
  font-size: 16px;
  font-weight: 400;
  background-color: white;
}

.description {
  margin-bottom: 30px;
  text-align: justify;
  background-color: white;
}

.mb-40 {
  margin-bottom: 40px;
  background-color: white;
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
  background-color: white;
}

.params li {
  margin-bottom: 15px;
  display: grid;
  grid-template-columns: 130px 1fr;
  grid-gap: 30px;
  width: 100%;
  font-size: 14px;
  text-align: justify;
  background-color: white;
}

.tag {
  font-size: 12px;
  font-weight: 400;
  padding: 3px 5px;
  border-radius: 6px;
  border: 1px solid #ffffff;
  display: inline-block;
  margin-top: -3px;
  background-color: white;
}

.text-muted {
  opacity: 0.4;
  background-color: white;
}

.rathing-main {
  display: block;
  margin-bottom: 10px;
  font-weight: 900;
  font-size: 36px;
  line-height: 42px;
  background-color: white;
}

.rathing-counts {
  display: block;
  margin-bottom: 10px;
  line-height: 19px;
  opacity: 0.4;
  background-color: white;
}

.rathing-details {
  display: inline-block;
  background-color: white;
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
