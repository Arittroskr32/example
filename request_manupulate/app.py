from flask import Flask, request, send_file, Response

app = Flask(__name__)

FLAG_PARTS = {
    'HEAD': '',
    'TRACE': 'RCSC{http_',
    'OPTIONS': 'methods_are_',
    'POST': 'fun_to_try}'
}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/secret', methods=['GET', 'POST', 'OPTIONS', 'HEAD', 'TRACE'])
def secret():
    method = request.method

    if method == 'HEAD':
        # Build custom response with empty body and custom header
        resp = Response('', status=200)
        resp.headers['X-Flag-Part'] = FLAG_PARTS['HEAD']
        resp.headers['Content-Length'] = '0'
        return resp
    
    if method == 'TRACE':
        return f"<div style='color:#c49d0d;'>Flag Part 1: {FLAG_PARTS['TRACE']}</div>"

    if method == 'OPTIONS':
        return f"<div style='color:#c49d0d;'>Flag Part 2: {FLAG_PARTS['OPTIONS']}</div>"

    if method == 'POST':
        return f"<div style='font-size:1.3em;color:#2a7ae2;'><b>Flag Part 3:</b> {FLAG_PARTS['POST']}</div>"

    return "<div style='color:#888;'>Sometimes you should try different!</div>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4005)
