<template>
  <div id="app">
    <PartTable />
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import PartTable from "@/components/PartTable.vue";

export default {
  name: 'App',
  components: {
    PartTable
  }
}
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
</style>
