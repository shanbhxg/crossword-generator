<template>
  <div id="app">
    <div v-if="isMobile" class="mobile-message">
      <p>This site is not accessible on mobile devices. Please visit from a desktop.</p>
    </div>
    <div v-else>
      <h1>CROSSWRD</h1>
      <h3 v-if="!gen">Generate a unique crossword puzzle!</h3>
      <WhatsNew v-if="!gen"/>
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
        <div v-if="acrossClues.length > 0">
          <h4>Across</h4>
          <div v-for="clue in acrossClues" :key="clue.number" :class="getClueClass(clue)">
            <strong>{{ clue.number }}.</strong> {{ clue.text }} ({{ clue.length }})
          </div>
        </div>

        <div v-if="downClues.length > 0">
          <h4>Down</h4>
          <div v-for="clue in downClues" :key="clue.number" :class="getClueClass(clue)">
            <strong>{{ clue.number }}.</strong> {{ clue.text }} ({{ clue.length }})
          </div>
        </div>
      </div>

      <div v-if="errorMessage" class="error">
        <p>{{ errorMessage }}</p>
      </div>
      <div class="buttons-container">
        <button v-if='!gen' id='generate' @click="generateCrossword">Generate New Puzzle</button>
        <button v-if='gen' id='generate2' @click="generateCrossword">Generate Another Puzzle</button>
        <button v-if='gen' id='fill' @click="autofillGrid">Answers</button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue';
import WhatsNew from './components/WhatsNew.vue'; 

const getApiBaseUrl = () => {
  if (window.location.hostname === "crosswrd.vercel.app") {
    return "https://crosswrd.vercel.app/api"; 
  }
  return "http://127.0.0.1:5000"; 
};

export default {
  components: {
    WhatsNew, 
  },
  data() {
    return {
      gen: false,
      grid: [],
      userGrid: [],
      solutionGrid: [],
      clues: [],
      wordPositions: [],
      errorMessage: null,
      acrossClues: [],
      downClues: [],
      isMobile: false, 
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
        this.solutionGrid = JSON.parse(JSON.stringify(data.grid)); 
        this.wordPositions = data.word_positions;
        this.clues = data.clues;
        this.userGrid = this.createEmptyGrid(this.grid.length, this.grid[0].length);
        this.acrossClues = [];
        this.downClues = [];
        this.organizeClues();
        this.errorMessage = null;
        this.gen = true;
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
    autofillGrid() {
      this.userGrid = JSON.parse(JSON.stringify(this.solutionGrid)); 
    },
    getClueClass(clue) {
      if (!clue.text) return ''; 
      if (clue.text.includes("_")) {
        return "blue-clue";  
      } else if (clue.text.includes("means the same as")) {
        return "green-clue"; 
      } else {
        return "red-clue"; 
      }
    }
  },
};
</script>

<style src="./style.css"></style>
