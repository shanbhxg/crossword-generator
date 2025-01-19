<template>
  <div class="whats-new">
    <h3>What's New?</h3>
    <ul>
      <li v-for="(update, index) in updates" :key="index">
        <strong>{{ update.title }}</strong> - {{ update.date }}
        <p>{{ update.description }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'WhatsNew',
  data() {
    return {
      updates: [
        {
          title: "New types of clues: Synonyms and Fill-in-the-Blank",
          date: "January 2025",
          description: "The crossword generator now randomly selects between definitions, synonyms, and fill-in-the-blank clues; so that if one type of clue is not available, another type will be used instead. For now, the clues are also color-coded according to their type (definitions are blue, synonyms are green, and fill-in-the-blank are red)."
        },
      ]
    };
  }
};
</script>

<style scoped>
.whats-new {
  background-color: #f9f9f9;
  padding: 1rem;
  margin: 20px 0;
  border-radius: 8px;
  width: 50%;
  margin: 0 auto;
  text-align: left;
  box-shadow: 0 2px 4px #4caf4f7d;
  margin-top: 40px;
  margin-bottom: 40px;
}

.whats-new h3 {
  color: #4CAF50;
  font-size: 20px;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
}

.whats-new ul {
  list-style-type: none;
  padding-left: 0;
}

.whats-new li {
  padding: 10px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(150, 150, 150, 0.1);
  border-radius: 4px;
  margin-bottom: 10px;
}

.whats-new li p {
  color: #555;
  font-size: 14px;
}
</style>
