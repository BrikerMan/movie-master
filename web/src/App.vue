<template>
  <div id="app">
    <el-container>
      <el-header>
        <NavBar></NavBar>
      </el-header>
      <el-main>
        <PlotSearch></PlotSearch>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import NavBar from './components/NavBar.vue'
  import PlotSearch from './components/pages/PlotSearch.vue'

  export default {
    name: 'App',
    components: {
      NavBar,
      PlotSearch
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
  }
</style>
