<template>
  <div>
    <div v-for="movie in movies" :key="movie.id">
      <div>Title {{ movie.name }}</div>
      <img v-bind:src="movie.poster" class="photo" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      movies: [],
    };
  },

  created() {
    fetch("http://127.0.0.1:8000/movie/", {
      method: "GET",
      "Access-Control-Allow-Origin": "*",
    })
      .then((res) => res.json())
      .then((data) => {
        this.movies = data;
      });
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.photo {
  width: 50px;
}
</style>
