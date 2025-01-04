<template>
  <div id="app">
    <h1>Crossword Generator</h1>

    <button @click="generateCrossword">Generate Crossword</button>
    <div v-if="grid.length > 0" class="crossword-container">
      <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="crossword-row">
        <div
          v-for="(cell, cellIndex) in row"
          :key="cellIndex"
          class="crossword-cell"
          :class="{'empty': cell === ' ', 'filled': cell !== ' '}"
        >
          <div v-if="isStartOfWord(rowIndex, cellIndex)" class="word-number">
            {{ getWordNumber(rowIndex, cellIndex) }}
          </div>

          <input
            v-if="cell !== ' '"
            v-model="userGrid[rowIndex][cellIndex]"
            :placeholder="cell !== ' ' ? '' : ' '"
            maxlength="1"
            class="crossword-input"
            @input="checkAnswer(rowIndex, cellIndex)"
            :disabled="userGrid[rowIndex][cellIndex] !== '' && !canEdit(rowIndex, cellIndex)"
          />
        </div>
      </div>
    </div>

    <div v-if="clues && clues.length > 0" class="clues-container">
      <h3>Clues:</h3>
      <div v-for="(clue, index) in clues" :key="index">
        <strong>{{ index + 1 }}.</strong> {{ clue }}
      </div>
    </div>

    <div v-if="errorMessage" class="error">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      grid: [],
      userGrid: [],
      clues: [],
      wordPositions: [], 
      errorMessage: null,
    };
  },
  methods: {
    async generateCrossword() {
      try {
        const response = await fetch("http://localhost:5000/generate");
        if (!response.ok) {
          throw new Error("Failed to fetch crossword data");
        }
        const data = await response.json();

        this.grid = data.grid;
        this.wordPositions = data.word_positions;
        this.clues = Object.values(data.clues);
        this.userGrid = this.createEmptyGrid(this.grid.length, this.grid[0].length);
        this.errorMessage = null;
      } catch (error) {
        this.errorMessage = error.message;
        console.error("Error generating crossword:", error);
      }
    },

    createEmptyGrid(rows, cols) {
      return Array.from({ length: rows }, () => Array(cols).fill(''));
    },

    checkAnswer(rowIndex, cellIndex) {
      const answer = this.grid[rowIndex][cellIndex];
      if (this.userGrid[rowIndex][cellIndex].toUpperCase() === answer.toUpperCase()) {
        this.$set(this.userGrid[rowIndex], cellIndex, this.userGrid[rowIndex][cellIndex].toUpperCase());
      }
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
      return word ? this.wordPositions.indexOf(word) + 1 : null;
    },

    canEdit(rowIndex, cellIndex) {
      return this.userGrid[rowIndex][cellIndex] !== '';
    },
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
}

.crossword-container {
  margin-top: 20px;
}

.crossword-row {
  display: flex;
  justify-content: center;
}

.crossword-cell {
  width: 30px;
  height: 30px;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty {
  background-color: #f4f4f4;
}

.filled {
  background-color: #e0e0e0;
}

.crossword-input {
  text-align: center;
  font-size: 18px;
  border: none;
  outline: none;
  width: 20px;
  height: 20px;
}

.word-number {
  font-size: 14px;
  color: #007bff;
  font-weight: bold;
}

.clues-container {
  margin-top: 20px;
  text-align: left;
  max-width: 600px;
  margin: 0 auto;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 20px;
}
</style>
