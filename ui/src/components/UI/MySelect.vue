<template>
  <select :value="modelValue" @change="changeOption">
    <option disabled value="">Выберите значение</option>
    <option v-for="option in options" :key="option.value" :value="option.value">
      {{ option.name }}
    </option>
  </select>
</template>

<script>
export default {
  name: "my-select",

  props: {
    options: {
      type: Array,
      default: () => [],
    },
    modelValue: {
      type: String,
    },
  },

  methods: {
    changeOption(event) {
      this.$emit("update:modelValue", event.target.value);
      console.log(event);
    },
  },
};
</script>

<style></style>
