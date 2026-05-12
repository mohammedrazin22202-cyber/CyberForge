import os
import json
import re
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
# Allow requests from portfolio (file:// and localhost variants)
CORS(app, resources={r"/*": {"origins": "*"}})

# ── Config ──────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH  = os.path.join(BASE_DIR, 'dataset.json')
RESPONSES_DIR = os.path.join(BASE_DIR, 'responses')

# Portfolio files folder — place your portfolio index.html here
# or point PORTFOLIO_DIR to wherever your portfolio files live
PORTFOLIO_DIR = os.path.join(BASE_DIR, 'portfolio')

# ── Load dataset ─────────────────────────────────────────────────────────────
with open(DATASET_PATH, 'r') as f:
    DATASET = json.load(f)

# ── Scoring engine ────────────────────────────────────────────────────────────
def score_input(user_input: str) -> dict:
    """
    STRICT MATCH ENGINE
    Response only triggers if full keyword or full sentence matches.
    """

    user_lower = user_input.lower().strip().rstrip('?!.,;:')

    for entry in DATASET:

        # STRICT key sentence match
        for sentence in entry['key_sentences']:
            if sentence and sentence.lower().strip() == user_lower:
                return {
                    'file_name': entry['file_name'],
                    'score': 100,
                    'matched': [('sentence', sentence)]
                }

        # STRICT keyword match
        for kw in entry['keywords']:
            if kw and kw.lower().strip() == user_lower:
                return {
                    'file_name': entry['file_name'],
                    'score': 100,
                    'matched': [('keyword', kw)]
                }

    return None
def load_response(file_name: str) -> str:
    """Load the response text from the responses folder."""
    path = os.path.join(RESPONSES_DIR, file_name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def get_fallback_response() -> str:
    fallback_path = os.path.join(RESPONSES_DIR, 'fallback.txt')
    if os.path.exists(fallback_path):
        with open(fallback_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return (
        ">> QUERY UNRESOLVED. No matching data found in neural matrix.\n"
        ">> Please rephrase your query or try keywords like: skills, projects, VConnect, LogiSense, Python."
    )

# ── API Routes ────────────────────────────────────────────────────────────────

# Serve standalone chatbot UI at /chatbot
@app.route('/chatbot')
def chatbot():
    return send_from_directory('static', 'index.html')

# Serve portfolio at root if portfolio/index.html exists,
# otherwise fall back to chatbot UI
@app.route('/')
def index():
    portfolio_index = os.path.join(PORTFOLIO_DIR, 'index.html')
    if os.path.exists(portfolio_index):
        return send_from_directory(PORTFOLIO_DIR, 'index.html')
    return send_from_directory('static', 'index.html')

# Serve any portfolio static assets (logo, certs, resume, etc.)
@app.route('/<path:filename>')
def portfolio_assets(filename):
    # Don't intercept API routes
    if filename.startswith(('chat', 'status', 'static/')):
        return jsonify({'error': 'not found'}), 404
    portfolio_file = os.path.join(PORTFOLIO_DIR, filename)
    if os.path.exists(portfolio_file):
        return send_from_directory(PORTFOLIO_DIR, filename)
    # fallback to chatbot static
    return send_from_directory('static', filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({'response': '>> NULL INPUT DETECTED. Enter your query, human.', 'score': 0, 'file': None})

    result = score_input(user_input)

    if not result or result['score'] == 0:
        return jsonify({
            'response': get_fallback_response(),
            'score': 0,
            'file': None,
            'matched': []
        })

    response_text = load_response(result['file_name'])

    if not response_text:
        response_text = (
            f">> RESPONSE FILE NOT FOUND: {result['file_name']}\n"
            f">> Place your response .txt files inside the 'responses/' folder."
        )

    return jsonify({
        'response': response_text,
        'score': result['score'],
        'file': result['file_name'],
        'matched': result['matched'][:10]
    })

@app.route('/status', methods=['GET'])
def status():
    total = len(DATASET)
    loaded = sum(1 for e in DATASET if os.path.exists(os.path.join(RESPONSES_DIR, e['file_name'])))
    return jsonify({'total_entries': total, 'responses_loaded': loaded, 'status': 'ONLINE'})

if __name__ == '__main__':
    if not os.path.exists(PORTFOLIO_DIR):
        os.makedirs(PORTFOLIO_DIR)
        print(f"\n>> Created 'portfolio/' folder.")
        print(f">> Copy your portfolio index.html + assets into: {PORTFOLIO_DIR}")

    port = int(os.environ.get('PORT', 5000))
    print("\n>> MEGATRON OS — CYBERFORGE AI SYSTEM INITIALIZING...")
    print(f">> Portfolio:  http://localhost:{port}/")
    print(f">> Chatbot UI: http://localhost:{port}/chatbot")
    print(f">> Chat API:   http://localhost:{port}/chat")
    print(f">> Status API: http://localhost:{port}/status\n")
    app.run(debug=False, host='0.0.0.0', port=port)