<template>
  <div class="navbar">
    <a @click="$router.push('/')" class="appName">Название</a>
    <a @click="$router.push('/movies')" class="refs">Фильмы</a>
    <a class="refs">Сериалы</a>
    <a class="logbtn">Войти</a>
  </div>
</template>

<script>
export default {};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

.navbar {
  margin: 0;
  padding: 0;
  background-color: black;
  height: 70px;
  box-shadow: 2px 2px 4px gray;
  display: flex;
  gap: 40px;
  padding-left: 330px;
  padding-right: 365px;
}

.navbar .appName {
  font-size: 35px;
  background-color: inherit;
  color: lightgrey;
  display: flex;
  font-weight: bold;
  vertical-align: middle;
  align-items: center;
  padding-right: 30px;
}

.navbar .refs {
  background-color: inherit;
  color: lightgrey;
  font-size: 20px;
  font-weight: bold;
  align-items: center;
  vertical-align: middle;
  display: flex;
  justify-content: space-between;
  padding-top: 4px;
}

.navbar .logbtn {
  background-color: inherit;
  color: lightgrey;
  margin-left: auto;
  font-size: 16px;
  font-weight: bold;
  align-items: center;
  vertical-align: middle;
  display: flex;
}
</style>
