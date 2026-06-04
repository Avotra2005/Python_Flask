import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'user_dashboard_secret_key' 
DB_FILE = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- LOGIN ROUTE ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template('login.html')

# --- REGISTER ROUTE ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template('register.html')
            
        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            
            flash("Registration successful! Please login below.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
            
    return render_template('register.html')

# --- USER DASHBOARD ROUTE ---
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Route Guard: Block unauthenticated users
    if 'user_id' not in session:
        flash("Please login to view your dashboard.", "warning")
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    
    if request.method == 'POST':
        new_username = request.form['username']
        
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            conn.commit()
            conn.close()
            
            session['username'] = new_username
            flash("Profile updated successfully!", "success")
        except sqlite3.IntegrityError:
            flash("That username is already taken.", "danger")
            
    return render_template('dashboard.html')

# --- LOGOUT ROUTE ---
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
