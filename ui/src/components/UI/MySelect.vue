<template>
  <div class="select-wrapper">
    <select class="select" :value="modelValue" @change="changeOption">
      <option disabled value="">Выберите значение</option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.name }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "my-select",

  data() {
    return {
      cliked: true,
    };
  },

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
    },
  },
};
</script>

<style>
.select {
  padding: 10px 35px 10px 15px;
  appearance: none;
  cursor: pointer;
  border: 1px solid;
  border-radius: 6px;
  width: 100%;
}

.select:focus {
  outline: none;
  box-shadow: 0 0 0 1px black, 0px 0px 10px black;
}

.select-wrapper {
  position: relative;
  width: 185px;
}

.select-wrapper:focus {
  position: relative;
  width: 185px;
}

.select-wrapper::before {
  content: "";
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);

  display: block;

  width: 0px;
  height: 0px;
  border-style: solid;
  border-width: 8px 5px 0 5px;
  border-color: black transparent transparent transparent;
}

.select-wrapper:focus {
  content: "";
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);

  display: block;

  width: 0px;
  height: 0px;
  border-style: solid;
  border-width: 0 5px 8px 5px;
  border-color: transparent transparent #000000 transparent;
}
</style>
