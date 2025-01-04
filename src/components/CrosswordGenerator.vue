<template>
    <div v-if="crossword">
      <div class="grid">
        <div v-for="(row, y) in crossword.grid" :key="y" class="row">
          <div
            v-for="(cell, x) in row"
            :key="x"
            :class="{'black': cell === '#', 'letter': cell !== '#'}"
            class="cell"
          >
            {{ cell !== '#' ? cell : '' }}
          </div>
        </div>
      </div>
      <div class="clues">
        <div v-for="(clue, word) in crossword.clues" :key="word">
          <b>{{ word }}:</b> {{ clue }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      crossword: Object,
    },
  };
  </script>
  
  <style scoped>
  .grid {
    display: grid;
    grid-template-columns: repeat(15, 30px);
    grid-template-rows: repeat(15, 30px);
    gap: 2px;
  }
  
  .row {
    display: flex;
  }
  
  .cell {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    background-color: white;
    border: 1px solid #ddd;
  }
  
  .cell.black {
    background-color: black;
  }
  
  .letter {
    color: black;
  }
  
  .clues {
    margin-top: 20px;
  }
  
  .clues b {
    margin-right: 10px;
  }
  </style>
  