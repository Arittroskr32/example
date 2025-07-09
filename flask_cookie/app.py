import os
import sys
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'secret123'  # Used to sign the session cookie

# Serve the frontend index.html at the root URL
@app.route('/')
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        return f.read()

# Set user as 'user' in session when /setsession is visited
@app.route('/setsession')
def set_session():
    session['user'] = 'user'
    return "Session cookie set with user: user"

# Retrieve session value
@app.route('/getsession')
def get_session():
    user = session.get('user')
    return f"Session cookie value: {user}" if user else "No session cookie found"

# Only allow admin access if session user is 'admin'
@app.route('/admin')
def admin():
    user = session.get('user')
    if user == 'admin':
        return "Welcome admin Flag: RCSC{admin_access_granted}"
    else:
        return "You are not admin"

if __name__ == '__main__':
    # Accept port from command line, default to 4003
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4003
    app.run(host='0.0.0.0', debug=True, port=port)
