<template>
  <my-navbar />
  <div class="myapp">
    <router-view></router-view>
  </div>
</template>

<script>
import MyNavbar from "@/components/MyNavbar.vue";
export default {
  components: {
    MyNavbar,
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.myapp {
  width: 1300px;
  height: 873px;
  margin: 0 auto;
  background-color: #fff;
}
</style>
