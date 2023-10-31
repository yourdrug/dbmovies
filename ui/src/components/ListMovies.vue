<template>
  <div class="movielist">
    <short-movie
      v-for="movie in short_movies"
      :key="movie.id"
      :movie="movie"
      :index="short_movies.indexOf(movie)"
    />
  </div>
</template>

<script>
import ShortMovie from "@/components/ShortMovie.vue";

export default {
  components: {
    ShortMovie,
  },
  props: {
    short_movies: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style>
.movielist {
  background-color: white;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  margin-top: 15px;
}
</style>
