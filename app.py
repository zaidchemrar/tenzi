from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

def get_db():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/characters')
def get_characters():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM characters")
    characters = cursor.fetchall()
    db.close()
    return jsonify(characters)

@app.route('/api/game/start', methods=['POST'])
def start_game():
    data = request.json
    game_type = data.get('type', 'all')
    db = get_db()
    cursor = db.cursor()
    if game_type == 'all':
        cursor.execute("SELECT id FROM characters")
    else:
        cursor.execute("SELECT id FROM characters WHERE type = %s", (game_type,))
    candidates = [row['id'] for row in cursor.fetchall()]
    db.close()
    return jsonify({'candidates': candidates, 'total': len(candidates)})

@app.route('/api/game/question', methods=['POST'])
def get_question():
    data = request.json
    candidates = data.get('candidates', [])
    asked = data.get('asked', [])

    if len(candidates) == 0:
        return jsonify({'error': 'No candidates left'}), 400

    # Only guess when we have exactly 1 candidate
# Only guess when we have exactly 1 candidate
    if len(candidates) == 1:
        return jsonify({'guess': True, 'candidate_id': candidates[0]})

    if len(candidates) == 2:
    # Guess but keep both in candidates list — frontend handles wrong
        return jsonify({'guess': True, 'candidate_id': candidates[0]})
    # With 2 candidates, ask one more question to narrow down
    # Don't guess yet — keep asking

    # If we've asked too many questions, guess the best remaining candidate
    if len(asked) >= 35:
     return jsonify({'guess': True, 'candidate_id': candidates[0]})

    db = get_db()
    cursor = db.cursor()

    # Get all attributes not yet asked
    if asked:
        format_strings = ','.join(['%s'] * len(asked))
        cursor.execute(f"""
            SELECT id, question, attribute_key
            FROM attributes
            WHERE id NOT IN ({format_strings})
        """, tuple(asked))
    else:
        cursor.execute("SELECT id, question, attribute_key FROM attributes")

    all_attributes = cursor.fetchall()

    if not all_attributes:
        db.close()
        return jsonify({'guess': True, 'candidate_id': candidates[0]})

    candidate_tuple = tuple(candidates)
    best_attr = None
    best_score = float('inf')
    best_yes_count = 0

    for attr in all_attributes:
        cursor.execute("""
            SELECT COUNT(*) as count FROM character_attributes
            WHERE attribute_id = %s AND character_id IN %s AND value = 1
        """, (attr['id'], candidate_tuple))
        result = cursor.fetchone()
        yes_count = result['count']
        no_count = len(candidates) - yes_count

        # Skip attributes that don't split candidates at all
        if yes_count == 0 or no_count == 0:
            continue

        # Score = how close to 50/50 split
        score = abs(yes_count - no_count)
        if score < best_score:
            best_score = score
            best_attr = attr
            best_yes_count = yes_count

    db.close()

    # If no attribute splits the candidates, guess the first one
    if not best_attr:
        return jsonify({'guess': True, 'candidate_id': candidates[0]})

    return jsonify({
        'guess': False,
        'attribute_id': best_attr['id'],
        'question': best_attr['question'],
        'yes_count': best_yes_count,
        'total': len(candidates)
    })

@app.route('/api/game/answer', methods=['POST'])
def answer_question():
    data = request.json
    candidates = data.get('candidates', [])
    attribute_id = data.get('attribute_id')
    answer = data.get('answer')

    if not candidates:
        return jsonify({'candidates': []})

    if len(candidates) == 1:
        return jsonify({'candidates': candidates})

    db = get_db()
    cursor = db.cursor()

    if answer == 'yes':
        cursor.execute("""
            SELECT character_id FROM character_attributes
            WHERE attribute_id = %s AND character_id IN %s AND value = 1
        """, (attribute_id, tuple(candidates)))
        remaining = [row['character_id'] for row in cursor.fetchall()]
    elif answer == 'no':
        cursor.execute("""
            SELECT character_id FROM character_attributes
            WHERE attribute_id = %s AND character_id IN %s AND value = 0
        """, (attribute_id, tuple(candidates)))
        remaining = [row['character_id'] for row in cursor.fetchall()]
    else:
        # Maybe - don't filter, keep all
        remaining = candidates

    db.close()

    # Never go to zero — if answer eliminated everyone, keep previous candidates
    if len(remaining) == 0:
        return jsonify({'candidates': candidates})

    return jsonify({'candidates': remaining})

@app.route('/api/character/<int:character_id>')
def get_character(character_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM characters WHERE id = %s", (character_id,))
    character = cursor.fetchone()
    db.close()
    return jsonify(character)

@app.route('/api/debug/candidates', methods=['POST'])
def debug_candidates():
    data = request.json
    candidates = data.get('candidates', [])
    db = get_db()
    cursor = db.cursor()
    if candidates:
        format_strings = ','.join(['%s'] * len(candidates))
        cursor.execute(f"SELECT id, name, type FROM characters WHERE id IN ({format_strings})", tuple(candidates))
        chars = cursor.fetchall()
    else:
        chars = []
    db.close()
    return jsonify(chars)

if __name__ == '__main__':
    app.run(debug=True)