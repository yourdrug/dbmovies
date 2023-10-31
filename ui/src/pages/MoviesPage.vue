<template>
  <input v-model="idInput" placeholder="id фильма в кинопоиске" />
  <button @click="getMoviesFromKinopoisk">Получить фильм</button>
  <button @click="postMovies">Добавить Фильм в бд</button>
  <button @click="login">ВОЙТИ</button>
  <div class="movies">
    <div class="filters">
      <my-select v-model="selectedFilter" :options="genreOptions" />
      <my-select v-model="selectedFilter" :options="genreOptions" />
      <my-select v-model="selectedFilter" :options="genreOptions" />
    </div>
    <list-movies v-bind:short_movies="filterMovie" />
  </div>
</template>

<script>
import axios from "axios";
import ListMovies from "@/components/ListMovies.vue";

export default {
  components: {
    ListMovies,
  },

  data() {
    return {
      movies: [],
      moviesKP: {},
      user: {},
      idInput: "",
      selectedFilter: "",
      genreOptions: [
        { value: "криминал", name: "Криминал" },
        { value: "боевик", name: "Боевик" },
        { value: "драма", name: "Драма" },
        { value: "фэнтези", name: "Фэнтези" },
      ],
    };
  },

  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/movie");
        this.movies = response.data;
      } catch (error) {
        alert("erorr");
      }
    },

    async fetchShortMovies() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/movie_short");
        this.movies = response.data;
      } catch (error) {
        alert(error.message);
      }
    },

    async login() {
      let data = { username: "admin", password: "admin" };
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/auth/token/login",
          data
        );
        localStorage.setItem("token", response.data.auth_token);
        this.getAccountInfo();
        alert("Token " + localStorage.getItem("token"));
      } catch (error) {
        alert(error.message);
      }
    },

    async logout() {
      try {
        localStorage.setItem("token", "");
        this.user = {};
      } catch (error) {
        alert("ошибка в логауте");
      }
    },

    async getAccountInfo() {
      let config = {
        headers: {
          Authorization: "Token " + localStorage.getItem("token"),
        },
      };
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/auth/users/me/",
          config
        );
        this.user = response.data;
        alert(this.user.username);
      } catch (error) {
        alert("ошибка туть");
      }
    },

    async getMoviesFromKinopoisk() {
      let config = {
        headers: {
          "X-API-KEY": "3W0ZPKY-H5XM7X8-KRB88NB-QSF7VJ5",
        },
      };
      try {
        const response = await axios.get(
          "https://api.kinopoisk.dev/v1.3/movie/" + this.idInput,
          config
        );
        this.moviesKP = response.data;
        console.log(this.moviesKP);
        alert("Фильм получен");
      } catch (error) {
        alert("ошибка в парсе кп");
      }
    },

    async postMovies() {
      let data = {
        movies: this.moviesKP,
      };
      let config = {
        headers: {
          Authorization: "Token " + localStorage.getItem("token"),
        },
      };
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/movie/addAllGenres/",
          data,
          config
        );
        console.log(response.message);
        alert("Фильм загружен");
      } catch (error) {
        alert(error.message);
      }
    },
  },

  mounted() {
    this.fetchShortMovies();
  },

  computed: {
    filterMovie() {
      if (this.selectedFilter != "") {
        return this.movies.filter((movie) =>
          movie.genres.some((genre) => genre.name === this.selectedFilter)
        );
      } else {
        return this.movies;
      }
    },
  },
};
</script>

<style>
#app {
  font-family: "Gabarito", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.movies {
  width: 1300px;
  margin: 0 auto;
  background-color: #fff;
  display: flex;
}

.filters {
  background-color: white;
  margin: 15px;
}
</style>
