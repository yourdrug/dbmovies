<template>
  <div class="container">
    <div class="wrapper">
      <div class="wrapper-col-1">
        <img :src="this.person.photo" :alt="this.person.name" />
      </div>
      <!-- /.wrapper-col-1 -->
      <div class="wrapper-col-2">
        <h1 class="title">{{ this.person.name }}</h1>
        <p class="description">
          {{ this.person.birth_day }}
        </p>
      </div>
    </div>
    <!-- /.wrapper -->
  </div>
  <!-- /.container -->
</template>

<script>
export default {
  props: {
    person: {
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

.description {
  margin-bottom: 30px;
  text-align: justify;
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
