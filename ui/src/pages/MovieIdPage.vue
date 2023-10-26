<template>
  <div>
    <current-movie :movie="this.movie"></current-movie>
  </div>
</template>

<script>
import axios from "axios";
import CurrentMovie from "@/components/CurrentMovie.vue";

export default {
  components: {
    CurrentMovie,
  },

  data() {
    return {
      movie: {},
    };
  },
  methods: {
    async fetchMovies() {
      let url = "http://127.0.0.1:8000/movie/" + this.$route.params.id;
      try {
        const response = await axios.get(url);
        this.movie = response.data;
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
