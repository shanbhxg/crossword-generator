# app.py

import random
from flask import Flask, render_template

app = Flask(__name__)

# Sample list of words for testing
word_list = ['apple', 'pear', 'roast', 'tree']
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


@app.route('/')
def crossword():
    word_list = ['apple', 'pear', 'roast', 'tree']
    ans = word_list
    crossword_grid = generate_crossword(word_list, grid_size)
    word_list = ans
    return render_template('crossword.html', grid=crossword_grid)

if __name__ == '__main__':
    app.run(debug=True)