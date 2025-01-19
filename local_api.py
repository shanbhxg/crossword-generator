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

def fetch_word_data(word):
    url = f"{API_URL}{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]
    except requests.exceptions.RequestException:
        return None

def generate_fill_in_the_blank(word):
    word_data = fetch_word_data(word)
    if word_data:
        for meaning in word_data.get("meanings", []):
            for definition in meaning.get("definitions", []):
                if "example" in definition:
                    example = definition["example"]
                    blanked_example = example.replace(word, "_" * len(word))  
                    return blanked_example
    return None

def generate_definitions(word):
    word_data = fetch_word_data(word)
    if word_data:
        definitions = [definition['definition'] for meaning in word_data.get("meanings", []) for definition in meaning.get("definitions", [])]
        return definitions
    return None

def generate_synonyms(word):
    word_data = fetch_word_data(word)
    if word_data:
        synonyms = set()
        for meaning in word_data.get("meanings", []):
            for definition in meaning.get("definitions", []):
                synonyms.update(definition.get("synonyms", []))
        return list(synonyms)
    return None

def generate_clue(word, clue_type="definition"):
    if clue_type == "fill_in_the_blank":
        return generate_fill_in_the_blank(word)
    elif clue_type == "definition":
        definitions = generate_definitions(word)
        return definitions[0] if definitions else None
    elif clue_type == "synonym":
        synonyms = generate_synonyms(word)
        return "This word means the same as: " + ", ".join(synonyms) if synonyms else None
    return None

def generate_crossword(words):
    grid_size = 15
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    word_positions = []
    clues = []
    word_number = 1

    def place_word(word):
        word_len = len(word)
        for _ in range(100): 
            direction = random.choice(['across', 'down'])
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)

            if direction == 'across' and x + word_len <= grid_size:
                if all(grid[y][x + i] in [' ', word[i]] for i in range(word_len)):
                    for i in range(word_len):
                        grid[y][x + i] = word[i]
                    word_positions.append({'word': word, 'x': x, 'y': y, 'direction': 'across', 'number': word_number})
                    return True
            elif direction == 'down' and y + word_len <= grid_size:
                if all(grid[y + i][x] in [' ', word[i]] for i in range(word_len)):
                    for i in range(word_len):
                        grid[y + i][x] = word[i]
                    word_positions.append({'word': word, 'x': x, 'y': y, 'direction': 'down', 'number': word_number})
                    return True
        return False

    for word in words:
        if place_word(word):
            clue_types = ["definition", "synonym", "fill_in_the_blank"]
            random.shuffle(clue_types) 

            clue = None
            clue_type_used = None
            for clue_type in clue_types:
                clue = generate_clue(word, clue_type)
                if clue:  
                    clue_type_used = clue_type
                    break

            if not clue:  
                clue = generate_clue(word, clue_type="definition")
                clue_type_used = "definition"

            clues.append({'number': word_number, 'text': clue, 'length': len(word), 'clue_type': clue_type_used})
            word_number += 1

    return grid, word_positions, clues

@app.route('/generate', methods=['GET'])
def generate_crossword_api():
    words = random.sample(load_words('api/words/english.txt'), 10) 
    grid, word_positions, clues = generate_crossword(words)

    response = {
        'grid': grid,
        'word_positions': word_positions,
        'clues': clues,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
