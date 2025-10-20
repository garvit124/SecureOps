from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Visitors table
    c.execute('''CREATE TABLE IF NOT EXISTS visitors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  contact TEXT NOT NULL,
                  purpose TEXT NOT NULL,
                  id_type TEXT NOT NULL,
                  id_number TEXT NOT NULL,
                  check_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  check_out TIMESTAMP,
                  registered_by TEXT NOT NULL,
                  status TEXT DEFAULT 'checked_in')''')
    
    # Suspects table
    c.execute('''CREATE TABLE IF NOT EXISTS suspects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT NOT NULL,
                  last_seen TEXT,
                  threat_level TEXT NOT NULL,
                  added_by TEXT NOT NULL,
                  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  status TEXT DEFAULT 'active')''')
    
    # Alerts table
    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  alert_type TEXT NOT NULL,
                  description TEXT NOT NULL,
                  severity TEXT NOT NULL,
                  location TEXT,
                  created_by TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  resolved INTEGER DEFAULT 0)''')
    
    # Create default admin if doesn't exist
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        admin_password = generate_password_hash('admin123')
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  ('admin', admin_password, 'admin'))
    
    conn.commit()
    conn.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')
            
            if user[3] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/users')
@admin_required
def manage_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    
    return render_template('manage_users.html', users=users)

@app.route('/admin/add-user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # Check if username exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            flash('Username already exists!', 'danger')
            conn.close()
            return redirect(url_for('add_user'))
        
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hashed_password, role))
        conn.commit()
        conn.close()
        
        flash(f'User {username} created successfully!', 'success')
        return redirect(url_for('manage_users'))
    
    return render_template('add_user.html')

@app.route('/admin/delete-user/<int:user_id>')
@admin_required
def delete_user(user_id):
    # Prevent deleting admin account
    if user_id == 1:
        flash('Cannot delete the main admin account!', 'danger')
        return redirect(url_for('manage_users'))
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get statistics
    c.execute("SELECT COUNT(*) FROM visitors WHERE status='checked_in'")
    active_visitors = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM suspects WHERE status='active'")
    active_suspects = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM alerts WHERE resolved=0")
    pending_alerts = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    # Get recent alerts
    c.execute("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 5")
    recent_alerts = c.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html',
                          active_visitors=active_visitors,
                          active_suspects=active_suspects,
                          pending_alerts=pending_alerts,
                          total_users=total_users,
                          recent_alerts=recent_alerts)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM visitors WHERE status='checked_in'")
    active_visitors = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM alerts WHERE resolved=0")
    pending_alerts = c.fetchone()[0]
    
    c.execute("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 5")
    recent_alerts = c.fetchall()
    
    conn.close()
    
    return render_template('user_dashboard.html',
                          active_visitors=active_visitors,
                          pending_alerts=pending_alerts,
                          recent_alerts=recent_alerts)

@app.route('/register-visitor', methods=['GET', 'POST'])
@login_required
def register_visitor():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        purpose = request.form['purpose']
        id_type = request.form['id_type']
        id_number = request.form['id_number']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""INSERT INTO visitors (name, contact, purpose, id_type, id_number, registered_by)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (name, contact, purpose, id_type, id_number, session['username']))
        conn.commit()
        conn.close()
        
        flash('Visitor registered successfully!', 'success')
        return redirect(url_for('visitor_logs'))
    
    return render_template('register_visitor.html')

@app.route('/add-suspect', methods=['GET', 'POST'])
@admin_required
def add_suspect():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        last_seen = request.form['last_seen']
        threat_level = request.form['threat_level']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""INSERT INTO suspects (name, description, last_seen, threat_level, added_by)
                     VALUES (?, ?, ?, ?, ?)""",
                  (name, description, last_seen, threat_level, session['username']))
        conn.commit()
        conn.close()
        
        flash('Suspect added successfully!', 'success')
        return redirect(url_for('suspect_records'))
    
    return render_template('add_suspect.html')

@app.route('/alerts', methods=['GET', 'POST'])
@login_required
def view_alerts():
    if request.method == 'POST':
        alert_type = request.form['alert_type']
        description = request.form['description']
        severity = request.form['severity']
        location = request.form['location']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""INSERT INTO alerts (alert_type, description, severity, location, created_by)
                     VALUES (?, ?, ?, ?, ?)""",
                  (alert_type, description, severity, location, session['username']))
        conn.commit()
        conn.close()
        
        flash('Alert created successfully!', 'success')
        return redirect(url_for('view_alerts'))
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM alerts ORDER BY created_at DESC")
    alerts = c.fetchall()
    conn.close()
    
    return render_template('view_alerts.html', alerts=alerts)

@app.route('/visitor-logs')
@login_required
def visitor_logs():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM visitors ORDER BY check_in DESC")
    visitors = c.fetchall()
    conn.close()
    
    return render_template('visitor_logs.html', visitors=visitors)

@app.route('/suspect-records')
@admin_required
def suspect_records():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM suspects ORDER BY added_at DESC")
    suspects = c.fetchall()
    conn.close()
    
    return render_template('suspect_records.html', suspects=suspects)

@app.route('/checkout-visitor/<int:visitor_id>')
@login_required
def checkout_visitor(visitor_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE visitors SET check_out=?, status='checked_out' WHERE id=?",
              (datetime.now(), visitor_id))
    conn.commit()
    conn.close()
    
    flash('Visitor checked out successfully!', 'success')
    return redirect(url_for('visitor_logs'))

@app.route('/resolve-alert/<int:alert_id>')
@login_required
def resolve_alert(alert_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE alerts SET resolved=1 WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()
    
    flash('Alert resolved!', 'success')
    return redirect(url_for('view_alerts'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)