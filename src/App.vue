<template>
  <div id="app">
    <h1>Crossword Generator</h1>
    <div v-if="grid.length > 0" class="crossword-container">
      <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="crossword-row">
        <div v-for="(cell, cellIndex) in row" :key="cellIndex" class="crossword-cell" :class="{'empty': cell === ' ', 'filled': cell !== ' '}">
          <div v-if="isStartOfWord(rowIndex, cellIndex)" class="word-number">
            {{ getWordNumber(rowIndex, cellIndex) }}
          </div>
          <input
            v-if="cell !== ' '"
            v-model="userGrid[rowIndex][cellIndex]"
            :maxlength="1"
            class="crossword-input"
            :class="getInputClass(rowIndex, cellIndex)"
            
          />
        </div>
      </div>
    </div>

    <div v-if="clues.length > 0" class="clues-container">
      <h3>Clues:</h3>

      <!-- ACROSS -->
      <div v-if="acrossClues.length > 0">
        <h4>Across</h4>
        <div v-for="clue in acrossClues" :key="clue.number">
          <strong>{{ clue.number }}.</strong> {{ clue.text }} ({{ clue.length }})
        </div>
      </div>

      <!-- DOWN -->
      <div v-if="downClues.length > 0">
        <h4>Down</h4>
        <div v-for="clue in downClues" :key="clue.number">
          <strong>{{ clue.number }}.</strong> {{ clue.text }} ({{ clue.length }})
        </div>
      </div>
    </div>

    <div v-if="errorMessage" class="error">
      <p>{{ errorMessage }}</p>
    </div>
    
    <button id='generate' @click="generateCrossword">Generate Crossword</button>
  </div>
</template>

<script>
import { reactive } from 'vue';
const getApiBaseUrl = () => {
  if (window.location.hostname === "crosswrd.vercel.app") {
    return "https://crosswrd.vercel.app/api"; // PROD
  }
  return "http://127.0.0.1:5000"; // LOCAL
};

export default {
  data() {
    return {
      grid: [],
      userGrid: [],
      clues: [],
      wordPositions: [],
      errorMessage: null,
      acrossClues: [],
      downClues: [],
    };
  },
  methods: {
    async generateCrossword() {
      try {
        const baseUrl = getApiBaseUrl();
        const response = await fetch(`${baseUrl}/generate`);        
        if (!response.ok) {
          throw new Error("Failed to fetch crossword data");
        }
        const data = await response.json();
        this.grid = data.grid;
        this.wordPositions = data.word_positions;
        this.clues = data.clues;
        this.userGrid = this.createEmptyGrid(this.grid.length, this.grid[0].length);
        this.errorMessage = null;
        this.organizeClues();
      } catch (error) {
        this.errorMessage = error.message;
        console.error("Error generating crossword:", error);
      }
    },
    createEmptyGrid(rows, cols) {
      return Array.from({ length: rows }, () => Array(cols).fill(''));
    },
    organizeClues() {
      this.acrossClues = this.clues.filter(clue => {
        const word = this.wordPositions.find(w => w.number === clue.number);
        return word && word.direction === 'across';
      }).sort((a, b) => a.number - b.number);

      this.downClues = this.clues.filter(clue => {
        const word = this.wordPositions.find(w => w.number === clue.number);
        return word && word.direction === 'down';
      }).sort((a, b) => a.number - b.number);
    },
    isStartOfWord(rowIndex, cellIndex) {
      return this.wordPositions.some(
        (word) =>
          (word.direction === 'across' && word.y === rowIndex && word.x === cellIndex) ||
          (word.direction === 'down' && word.x === cellIndex && word.y === rowIndex)
      );
    },
    getWordNumber(rowIndex, cellIndex) {
      const word = this.wordPositions.find(
        (word) =>
          (word.direction === 'across' && word.y === rowIndex && word.x === cellIndex) ||
          (word.direction === 'down' && word.x === cellIndex && word.y === rowIndex)
      );
      return word ? word.number : null;
    },
    getInputClass(rowIndex, cellIndex) {
      return '';
    },
  },
};
</script>

<style src="./style.css"></style>
