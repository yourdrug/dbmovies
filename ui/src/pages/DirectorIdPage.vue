<template>
  <div>
    <current-person :person="this.person"></current-person>
  </div>
</template>

<script>
import axios from "axios";
import CurrentPerson from "@/components/CurrentPerson.vue";

export default {
  components: {
    CurrentPerson,
  },

  data() {
    return {
      person: {},
    };
  },
  methods: {
    async fetchPerson() {
      let url =
        "http://127.0.0.1:8000/persons/director/" + this.$route.params.id;
      try {
        const response = await axios.get(url);
        this.person = response.data;
      } catch (error) {
        alert("erorr");
      }
    },
  },
  mounted() {
    this.fetchPerson();
  },
};
</script>

<style></style>
