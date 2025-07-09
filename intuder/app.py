from flask import Flask, request, Response
import random
import threading
import time
import os
import sys

app = Flask(__name__)

FLAG = "RCSC{Hacker_must_learn_brute_forcing_to_win}"
current_token = None
lock = threading.Lock()

# Get absolute path of index.html relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML_PATH = os.path.join(base_dir, 'index.html')

# Store token expiration time
token_expiry = None

def generate_token():
    global current_token, token_expiry
    with lock:
        current_token = f"{random.randint(0, 9999):04d}"
        token_expiry = time.time() + 600  # 10 minutes from now
        print(f"[+] New token generated: {current_token} (valid for 10 min)")

def render_index_with_message(message=''):
    try:
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return Response("index.html not found", status=500)
    content = content.replace('{{message}}', message)
    return Response(content, mimetype='text/html')

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        guess = request.form.get('token_guess', '')
        with lock:
            token = current_token
            expiry = token_expiry
        if not token or not expiry or time.time() > expiry:
            message = "No valid token. Please generate a new token."
        elif guess == token:
            message = f"Correct! Here is your flag: <b>{FLAG}</b>"
        else:
            message = "Wrong token! Try again."
    return render_index_with_message(message)

@app.route('/generate_token', methods=['POST'])
def generate_token_api():
    generate_token()
    return {"message": "New token generated! It is valid for 10 minutes."}

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4002
    print(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
