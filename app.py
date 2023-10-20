# app.py

import random
from flask import Flask, render_template
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

app = Flask(__name__)

def get_random_words(num_words):
    random_words = []
    word_synsets = list(wordnet.all_synsets())
    
    while len(random_words) < num_words:
        synset = random.choice(word_synsets)
        word = synset.name().split('.')[0]  # Get the word without the part of speech
        
        # Check if the word's length is between 3 and 8 characters
        if 3 <= len(word) <= 8:
            random_words.append(word) 
    return random_words
# Sample list of words for testing
# generating a list of random words using the wordnet corpus
num_words = 10  # Change the number of random words as needed
word_list = get_random_words(num_words)   
ans = word_list
grid_size = max(len(word) for word in word_list) + 1

def generate_crossword(word_list, grid_size):
    # Create an empty grid
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    # Function to check if a word fits at a given position
    def fits(word, x, y, direction):
        if direction == 'across':
            return all(grid[y][x + i] == ' ' or grid[y][x + i] == word[i] for i in range(len(word)))
        else:
            return all(grid[y + i][x] == ' ' or grid[y + i][x] == word[i] for i in range(len(word)))
    
    # Function to add a word to the grid
    def add_word(word, x, y, direction):
        if direction == 'across':
            for i in range(len(word)):
                grid[y][x + i] = word[i]
        else:
            for i in range(len(word)):
                grid[y + i][x] = word[i]
    
    # Shuffle the word list and sort by length
    random.shuffle(word_list)
    word_list.sort(key=lambda x: len(x), reverse=True)
    
    # Starting positions (x, y, direction)
    starting_cells = [(0, 0, 'across')]
    
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] == ' ':
                if x == 0 or grid[y][x - 1] == '#':
                    starting_cells.append((x, y, 'across'))
                if y == 0 or grid[y - 1][x] == '#':
                    starting_cells.append((x, y, 'down'))
    
    for start_x, start_y, direction in starting_cells:
        for word in word_list:
            if fits(word, start_x, start_y, direction):
                add_word(word, start_x, start_y, direction)
                word_list.remove(word)
    return grid

def generate_crossword_clues(words):
    clues = {}
    for word in words:
        # Find the first synset (sense) of the word in WordNet
        synsets = wordnet.synsets(word)
        if synsets:
            # Use the definition of the first synset as the clue
            clues[word] = synsets[0].definition()
        else:
            # If no definition is found, provide a default message
            clues[word] = "No definition found"
    return clues

@app.route('/')
def crossword():
    word_list = get_random_words(10)   
    ans = word_list
    grid_size = max(len(word) for word in word_list) + 1
    crossword_grid = generate_crossword(word_list, grid_size)
    word_list = ans
    # Generate clues
    clues = generate_crossword_clues(word_list)
    across_clues = {i: clues[word] for i, word in enumerate(word_list)}
    down_clues = {i: clues[word] for i, word in enumerate(word_list, len(word_list))}
    return render_template('crossword.html', grid=crossword_grid, across=across_clues, down=down_clues)

if __name__ == '__main__':
    app.run(debug=True)