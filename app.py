from flask import Flask, render_template, request, jsonify, send_file
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from functools import wraps
import face_recognition
import cv2
import numpy as np
@@ -41,9 +42,50 @@ def b64_to_bytes(b64str):
b64str = b64str.split(',', 1)[1]
return base64.b64decode(b64str)

# ─── Auth ─────────────────────────────────────────────────────────────────────
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@keyafusion.com')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'admin123')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json or {}
        email = data.get('email')
        password = data.get('password')
        if email == ADMIN_EMAIL and password == ADMIN_PASS:
            session['logged_in'] = True
            return jsonify({"success": True, "message": "Welcome back!"})
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    if session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/send_otp', methods=['POST'])
def send_otp():
    return jsonify({"success": False, "message": "Admin registration is disabled. Please sign in."}), 403

@app.route('/register', methods=['POST'])
def register():
    return jsonify({"success": False, "message": "Admin registration is disabled."}), 403

@app.route('/')
@login_required
def index():
# If this service is meant only for users, redirect home to the user panel
if os.getenv('APP_MODE') == 'USER':
@@ -60,18 +102,22 @@ def index():
recent_logs=all_logs[:8])

@app.route('/employees')
@login_required
def view_employees():
return render_template('employees.html', employees=get_all_employees())

@app.route('/add_employee')
@login_required
def add_employee_route():
return render_template('add_employee.html')

@app.route('/attendance')
@login_required
def attendance():
return render_template('attendance.html')

@app.route('/history')
@login_required
def history():
return render_template('history.html', logs=get_attendance_logs())
