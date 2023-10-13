<template>
  <div class="app">
    <list-movies v-bind:short_movies="movies"> </list-movies>
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
    };
  },

  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/movie/");
        this.movies = response.data;
      } catch (error) {
        alert("erorr");
      }
    },

    async fetchShortMovies() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/movie_short/");
        this.movies = response.data;
      } catch (error) {
        alert("erorr");
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
