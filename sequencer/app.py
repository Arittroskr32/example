from flask import Flask, request, Response
import base64
import random
import threading
import time
import os
import sys

app = Flask(__name__)

reset_tokens = {}
lock = threading.Lock()

base_dir = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML_PATH = os.path.join(base_dir, 'index.html')

def base64_encode_no_padding(s):
    return base64.b64encode(s.encode()).decode().rstrip("=")

def generate_reset_token(email):
    digit = random.randint(0, 9)
    b64_email = base64_encode_no_padding(email)
    display_token = f"rcsc{digit}{b64_email}"
    stored_digit = (digit + 1) % 10
    stored_token = f"rcsc{stored_digit}{b64_email}"
    return display_token, stored_token

def render_index_with_message(message=''):
    try:
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return Response("index.html not found", status=500)
    return Response(content.replace('{{message}}', message), mimetype='text/html')

def expire_tokens_periodically():
    while True:
        now = time.time()
        with lock:
            for email, data in list(reset_tokens.items()):
                if data['expires_at'] < now and data['token'] != 'strong_token':
                    reset_tokens[email]['token'] = 'strong_token'
                    print(f"[+] Token for {email} expired and reset to strong_token")
        time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email', '').strip().lower()

        if action == 'reset':
            if email:
                display_token, stored_token = generate_reset_token(email)
                expires_at = time.time() + 15
                with lock:
                    reset_tokens[email] = {'token': stored_token, 'expires_at': expires_at}
                message = f"Reset token generated for {email}: <b>{display_token}</b> (valid for 15 seconds)"
                print(f"[+] Generated token for {email}: {stored_token}")
            else:
                message = "Please enter a valid email for reset."

        elif action == 'update':
            token = request.form.get('token', '').strip()
            new_pass = request.form.get('new_password', '').strip()

            with lock:
                token_data = reset_tokens.get(email)

            if token == 'strong_token' or (token_data and token_data['token'] == token):
                with lock:
                    reset_tokens.pop(email, None)
                if email == 'admin@rcsc.com':
                    message = "Password updated successfully. A gift for you `RCSC{Weak_Default_Token_Bug_found}`!"
                else:
                    message = "Password updated successfully. To get flag update password for admin@rcsc.com"
                print(f"[+] Password updated for {email}")
            else:
                message = "Failed to update password. Check your token."
                print(f"[-] Failed password update attempt for {email} with token {token}")

    return render_index_with_message(message)

if __name__ == '__main__':
    threading.Thread(target=expire_tokens_periodically, daemon=True).start()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4006
    print(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
