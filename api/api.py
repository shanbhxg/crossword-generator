import random
import requests
from flask import Flask, jsonify
from flask_cors import CORS  
app = Flask(__name__)
CORS(app)
# Define the URL for the Free Dictionary API
API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# Load words from 'english.txt'
def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()
    return [word.strip() for word in words]

# Fetch word definition (clue) from the Free Dictionary API
def fetch_definition(word):
    url = f"{API_URL}{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        definitions = data[0]['meanings'][0]['definitions']
        return definitions[0]['definition']  # We use the first definition as the clue
    except requests.exceptions.RequestException:
        return "No clue available."

# Function to generate the crossword grid
def generate_crossword(words):
    grid_size = 15  # Define the size of the grid (e.g., 15x15)
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]  # Empty grid

    word_positions = []  # List to store words and their positions (x, y, direction)

    # Attempt to place words into the grid
    def place_word(word):
        word_len = len(word)
        placed = False

        for _ in range(100):  # Try 100 times to place the word
            direction = random.choice(['across', 'down'])
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)

            if direction == 'across' and x + word_len <= grid_size:
                # Check if the word fits and doesn't overlap incorrectly
                if all(grid[y][x + i] == ' ' or grid[y][x + i] == word[i] for i in range(word_len)):
                    # Place the word
                    for i in range(word_len):
                        grid[y][x + i] = word[i]
                    word_positions.append({'word': word, 'x': x, 'y': y, 'direction': 'across'})
                    placed = True
                    break

            elif direction == 'down' and y + word_len <= grid_size:
                # Check if the word fits and doesn't overlap incorrectly
                if all(grid[y + i][x] == ' ' or grid[y + i][x] == word[i] for i in range(word_len)):
                    # Place the word
                    for i in range(word_len):
                        grid[y + i][x] = word[i]
                    word_positions.append({'word': word, 'x': x, 'y': y, 'direction': 'down'})
                    placed = True
                    break

        return placed

    # Try placing all words on the grid
    for word in sorted(words, key=lambda w: -len(w)):  # Sort by word length (longest first)
        if not place_word(word):
            print(f"Failed to place word: {word}")
    
    return grid, word_positions

# Endpoint to generate the crossword
@app.route('/generate', methods=['GET'])
def generate_crossword_api():
    words = random.sample(load_words('api\words\english.txt'), 10)  # Select 10 random words
    crossword_grid, word_positions = generate_crossword(words)
    
    # Get clues for each word
    clues = {word: fetch_definition(word) for word in words}

    # Prepare response data
    crossword = {
        "grid": crossword_grid,
        "word_positions": word_positions,
        "clues": clues
    }

    return jsonify(crossword)

if __name__ == '__main__':
    app.run(debug=True)
