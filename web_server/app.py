from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo_only'

# HSTS Configuration
ENABLE_HSTS = False

@app.before_request
def ensure_secure():
    # In a real scenario, we would redirect to HTTPS here.
    # For this simulation, we heavily rely on the headers being present.
    pass

@app.after_request
def apply_hsts(response):
    if ENABLE_HSTS:
        # Strict-Transport-Security: max-age=31536000; includeSubDomains
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/toggle_security')
def toggle_security():
    global ENABLE_HSTS
    ENABLE_HSTS = not ENABLE_HSTS
    status = "enabled" if ENABLE_HSTS else "disabled"
    flash(f'HSTS Protection {status}!')
    return redirect(url_for('index'))

# Mock database
users = {
    "admin": "password123",
    "user": "securepass"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Run on 0.0.0.0 so it's accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)
