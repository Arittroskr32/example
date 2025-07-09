from flask import Flask, request, jsonify, send_file, make_response
import jwt

app = Flask(__name__)

# Normally this should verify alg type securely
SECRET_KEY = 'fsdfvfvfvsupersecurekey123jhiahiushjbdj'  # Used in HS256

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/gettoken')
def get_token():
    token = jwt.encode({'role': 'user'}, SECRET_KEY, algorithm='HS256')
    resp = make_response(jsonify({"token": token}))
    resp.set_cookie('token', token)
    return resp

@app.route('/admin')
def admin():
    token = request.headers.get('Authorization')
    if not token:
        token = request.cookies.get('token')
    if not token:
        return "Missing token", 401

    try:
        # ❌ Vulnerable: does not restrict algorithms properly
        decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False})
        if decoded.get('role') == 'admin':
            return "Welcome admin! Flag: RCSC{jwt_alg_none_and_unverified_fun}"
        else:
            return "Access denied. You are not admin.", 403
    except jwt.InvalidTokenError as e:
        return f"Invalid token: {e}", 400

if __name__ == '__main__':
    app.run(debug=True, port=4004)
