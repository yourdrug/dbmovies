<template>
  <div class="app">
    <list-movies v-bind:short_movies="movies"> </list-movies>
    <button @click="logout">ВЫЙТИ</button>
    <button @click="login">ВОЙТИ</button>
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
      user: {},
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
      let config = {
        headers: {
          Authorization: "Token " + localStorage.getItem("token"),
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      };
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/auth/token/logout",
          config
        );
        alert(response.data);
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
  },

  mounted() {
    this.fetchShortMovies();
  },
};
</script>

<style>
#app {
  font-family: "Gabarito", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.photo {
  width: 250px;
}
</style>
