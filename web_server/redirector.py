from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
def catch_all(path):
    # Redirect all HTTP traffic to HTTPS (port 443)
    # We use 307 Temporary Redirect to preserve the method (e.g., POST stays POST)
    # so that if simple_login flows hit this, they get redirected with data intact.
    # Note: Flask's default redirect is 302 (Found).
    return redirect(request.url.replace("http://", "https://"), code=307)

if __name__ == "__main__":
    print("Starting HTTP Redirector on port 80...")
    app.run(host='0.0.0.0', port=80)
