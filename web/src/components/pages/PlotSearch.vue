<template>
  <el-card class="box-card">
    <el-row>
      <el-form :inline="true" :model="formSearch">
        <el-select
          v-model="formSearch.movie_name"
          filterable
          remote
          reserve-keyword
          :remote-method="remoteSearchMethod"
          :loading="search_loading"
          placeholder="请选择">
          <el-option
            v-for="item in movie_candidates"
            :key="item.id"
            :label="item.title"
            :value="item.tag_line">
            <div>
              <span style="float: left">{{ item.title }}</span>
              <span style="float: right; color: #8492a6; font-size: 12px">{{ item.tag_line }}</span>
            </div>
          </el-option>
        </el-select>
        <el-form-item>
          <el-button type="primary" @click="onSearch">Search</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-row :gutter="20" :span="24">
      <el-col :span="4" v-for="movie in movies" :key="movie.id" style="margin-bottom: 20px;">
        <el-card :body-style="{ padding: '0px' }">
          <img
            style="width: 100%; height: 100%;"
            :src="'https://image.tmdb.org/t/p/w200' + movie.poster"
            class="image"
            :fit="fit">
          <div style="height: 80px">
            <span>{{movie.title}}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
  import axios from 'axios';
  import {debounce} from 'vue-debounce'

  export default {
    name: 'PlotSearch',
    data() {
      return {
        formSearch: {
          movie_name: ""
        },
        movies: [],
        movie_candidates: [],
        search_loading: false
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      remoteSearchMethod(query) {
        this.searchByName(query)
      },
      searchByName(query) {
        this.loading = true;
        const url = 'http://127.0.0.1:6006/movies?movie_name=' + query
        axios
          .get(url)
          .then(response => (
              this.movie_candidates = response.data
            )
          )
      },
      onSearch() {
        this.$watch('query', debounce((newQuery) => {
          this.$emit('query', newQuery)
        }, 200))
        const url = 'http://127.0.0.1:6006/movies?movie_name=' + this.formSearch.movie_name
        axios
          .get(url)
          .then(response => (
              this.movie_candidates = response.data
            )
          )
      }
    }
  }
</script>

<style>
  .el-row {
    margin-bottom: 20px;

  &
  :last-child {
    margin-bottom: 0;
  }

  }
  .el-col {
    border-radius: 4px;
  }

  .bg-purple-dark {
    background: #99a9bf;
  }

  .bg-purple {
    background: #d3dce6;
  }

  .bg-purple-light {
    background: #e5e9f2;
  }

  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }

  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
