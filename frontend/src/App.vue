<template>
  <div id="app">
    <table border="1">
      <tr v-for="(row, rowIndex) in grid" :key="rowIndex">
        <td v-for="(cell, colIndex) in row" :key="colIndex" :class="{'empty': cell === ' '}" class="cell">
          {{ cell !== ' ' ? cell : '' }}
        </td>
      </tr>
    </table>
    <h2>Clues</h2>
    <ol>
      <li v-for="(clue, word) in clues" :key="word">{{ clue }}</li>
    </ol>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      grid: [],
      clues: {},
    };
  },
  mounted() {
    this.fetchCrosswordData();
  },
  methods: {
    async fetchCrosswordData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/crossword');
        const data = response.data;
        this.grid = data.grid;
        this.clues = data.clues;
      } catch (error) {
        console.error('Error fetching crossword data:', error);
      }
    },
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

table {
  border-collapse: collapse;
  margin: 20px auto;
}

td {
  width: 50px;
  height: 50px;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  border: 1px solid #ccc;
}

td.empty {
  background-color: #000;
}

h1, h2 {
  color: #333;
}

ol {
  text-align: left;
  padding-left: 30px;
}
</style>
