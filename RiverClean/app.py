import os
import sqlite3
from datetime import datetime
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DB_PATH = 'database.db'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super_secret_key_riverclean' # for development

from tensorflow.keras.layers import DepthwiseConv2D

class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, **kwargs):
        kwargs.pop('groups', None)
        super().__init__(**kwargs)

MODEL_PATH = 'model.h5'
model = load_model(MODEL_PATH, compile=False, custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D})

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Users table: is_admin 1 for admin, 0 for regular users
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            is_admin BOOLEAN DEFAULT 0
        )
    ''')
    # Reports table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'Pending',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('detect.html', username=session.get('username'), is_admin=session.get('is_admin'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        # For demo purposes, the first user named 'admin' gets admin rights
        is_admin = 1 if username.lower() == 'admin' else 0
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                         (username, generate_password_hash(password), is_admin))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
        finally:
            conn.close()
    return render_template('login.html', action='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', action='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    reports = conn.execute('SELECT * FROM reports WHERE user_id = ? ORDER BY timestamp DESC', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', user=user, reports=reports)

@app.route('/admin')
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    # Get all polluted reports with user info
    reports = conn.execute('''
        SELECT r.*, u.username 
        FROM reports r 
        JOIN users u ON r.user_id = u.id 
        WHERE r.category = 'Polluted'
        ORDER BY r.timestamp DESC
    ''').fetchall()
    conn.close()
    return render_template('admin.html', reports=reports)

@app.route('/update_status/<int:report_id>', methods=['POST'])
def update_status(report_id):
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
        
    conn = get_db_connection()
    conn.execute('UPDATE reports SET status = ? WHERE id = ?', ('Done', report_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/detect', methods=['POST'])
def detect():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized. Please log in.'}), 401
        
    user_id = session['user_id']
    location = request.form.get('location', 'Unknown Location')
    photo = request.files.get('photo')

    if not photo:
        return jsonify({'error': 'Please provide a river photo.'})

    if not allowed_file(photo.filename):
        return jsonify({'error': 'Invalid file type. Please upload a PNG or JPG image.'})

    filename = secure_filename(photo.filename)
    # Add timestamp to avoid overwriting
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(save_path)

    # Preprocess image for model
    img = image.load_img(save_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Prediction
    preds = model.predict(img_array)
    pred_class = np.argmax(preds, axis=1)[0]
    class_names = ['Clean', 'Polluted']  # adjust as per your model
    result = class_names[pred_class]

    authorities_notified = False
    
    conn = get_db_connection()
    try:
        # Save report
        conn.execute('INSERT INTO reports (user_id, filename, category, location) VALUES (?, ?, ?, ?)',
                     (user_id, filename, result, location))
        
        # Optionally, save report if polluted
        if result == 'Polluted':
            authorities_notified = True
            # Add a point
            conn.execute('UPDATE users SET points = points + 1 WHERE id = ?', (user_id,))
            
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return jsonify({
        'category': result,
        'location': location,
        'authorities_notified': authorities_notified
    })

# Initialize configuration for hosting
if __name__ == '__main__':
    app.run(debug=True)