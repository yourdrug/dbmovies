<template>
  <div>
    <list-movies :short_movies="movies" />
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
      let url =
        "http://127.0.0.1:8000/movie_short/?genres__en_name=" +
        this.$route.params.genre;
      try {
        const response = await axios.get(url);
        this.movies = response.data;
      } catch (error) {
        alert("erorr");
      }
    },
  },
  mounted() {
    this.fetchMovies();
  },
};
</script>

<style></style>
