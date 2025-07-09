from flask import Flask, request, jsonify, send_file
import jwt

app = Flask(__name__)
SECRET_KEY = 'password123456'  # Hidden from attacker (bruteforce target)


# Serve index.html at root
@app.route('/')
def index():
    return send_file('index.html')

# Issue a JWT for role=user and set it as a cookie
from flask import make_response

@app.route('/gettoken')
def get_token():
    token = jwt.encode({'role': 'user'}, SECRET_KEY, algorithm='HS256')
    resp = make_response(jsonify({"token": token}))
    resp.set_cookie('token', token)
    return resp


# Protected admin route
@app.route('/admin')
def admin():
    # Try to get token from Authorization header, then from cookie
    token = request.headers.get('Authorization')
    if not token:
        token = request.cookies.get('token')
    if not token:
        return "Missing token", 401

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if decoded.get('role') == 'admin':
            return "Welcome admin! Flag: RCSC{IS_jwt_awesome_for_authentication}"
        else:
            return "Access denied. You are not admin.", 403
    except jwt.InvalidTokenError:
        return "Invalid token", 400


if __name__ == '__main__':
    app.run(debug=True, port=4003)
