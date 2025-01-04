import random
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()
    return [word.strip() for word in words if len(word.strip()) >= 4] 

def fetch_definition(word):
    url = f"{API_URL}{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        definitions = data[0]['meanings'][0]['definitions']
        return definitions[0]['definition']  
    except requests.exceptions.RequestException:
        return "No clue available."

def generate_crossword(words):
    grid_size = 15  
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)] 
    word_positions = [] 
    word_numbers = {}

    def place_word(word):
        word_len = len(word)
        placed = False
        for _ in range(100):  
            direction = random.choice(['across', 'down'])
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)

            if direction == 'across' and x + word_len <= grid_size:
                valid = True
                # no touching words
                for i in range(word_len):
                    if grid[y][x + i] != ' ' and grid[y][x + i] != word[i]:
                        valid = False
                        break
                    if x + i > 0 and grid[y][x + i - 1] != ' ':  
                        valid = False
                        break
                    if x + i < grid_size - 1 and grid[y][x + i + 1] != ' ':  
                        valid = False
                        break
                    if y > 0 and grid[y - 1][x + i] != ' ':  
                        valid = False
                        break
                    if y < grid_size - 1 and grid[y + 1][x + i] != ' ': 
                        valid = False
                        break

                if valid:
                    for i in range(word_len):
                        grid[y][x + i] = word[i]
                    word_positions.append({'word': word, 'x': x, 'y': y, 'direction': 'across', 'number': len(word_numbers) + 1})
                    word_numbers[word] = len(word_numbers) + 1
                    placed = True
                    break

            elif direction == 'down' and y + word_len <= grid_size:
                valid = True

                for i in range(word_len):
                    if grid[y + i][x] != ' ' and grid[y + i][x] != word[i]:
                        valid = False
                        break
                    if x > 0 and grid[y + i][x - 1] != ' ':  
                        valid = False
                        break
                    if x < grid_size - 1 and grid[y + i][x + 1] != ' ':  
                        valid = False
                        break
                    if y + i > 0 and grid[y + i - 1][x] != ' ':  
                        valid = False
                        break
                    if y + i < grid_size - 1 and grid[y + i + 1][x] != ' ': 
                        valid = False
                        break

                if valid:
                    for i in range(word_len):
                        grid[y + i][x] = word[i]
                    word_positions.append({'word': word, 'x': x, 'y': y, 'direction': 'down', 'number': len(word_numbers) + 1})
                    word_numbers[word] = len(word_numbers) + 1
                    placed = True
                    break

        return placed




    for word in sorted(words, key=lambda w: -len(w)):  
        if not place_word(word):
            print(f"Failed to place word: {word}")
    
    return grid, word_positions, word_numbers

@app.route('/generate', methods=['GET'])
def generate_crossword_api():
    words = random.sample(load_words('api/words/english.txt'), 10)  
    crossword_grid, word_positions, word_numbers = generate_crossword(words)
    clues = {word: fetch_definition(word) for word in words}
    
    sorted_word_positions = sorted(word_positions, key=lambda x: (x['direction'], x['number']))
    
    formatted_clues = [{'number': word_numbers[word], 'text': clues[word], 'length': len(word)} for word in words]
    
    formatted_clues_sorted = sorted(formatted_clues, key=lambda clue: word_numbers[words[formatted_clues.index(clue)]])

    crossword = {
        "grid": crossword_grid,
        "word_positions": sorted_word_positions,
        "clues": formatted_clues_sorted
    }
    print(words)
    return jsonify(crossword)

if __name__ == '__main__':
    app.run(debug=True)
