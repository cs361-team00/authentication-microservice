from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import sqlite3
import uuid

app = Flask(__name__)
bcrypt = Bcrypt(app)

DB_NAME = 'users.db'

# temp dictionary for token storage
reset_tokens = {}

# initialize database
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL
                    )''')
        conn.commit()
init_db()


# USER STORY 1: RESIGTER
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(force=True, silent=True) or {}
    email = data.get('user_email')
    # Fixed key to user_pass to match your test scripts
    password = data.get('user_pass') 

    # if no email or password was entered
    if not email or not password:
        return jsonify({"status": "error", "error_message": "Email and password required.",}), 400
    
    # hashes password and decodes it into text string so SQLite can read
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)",
                           (email, hashed_password))
            user_id = cursor.lastrowid
            conn.commit()

        return jsonify({
            "status": "success",
            "user_id": user_id,
            "error_message": None
        }), 201
    
    # error if email wasn't unique
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "error_message": "Email already registered."}), 400


# USER STORY 2: LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True, silent=True) or {}
    email = data.get('user_email')
    password = data.get('user_pass')

    # searches database for matching email
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[1], password):
        session_token = str(uuid.uuid4()) 
        return jsonify({"status": "success", "user_id": user[0], "session_token": session_token}), 200
    else:
        return jsonify({"status": "denied", "error_message": "Invalid email or password."}), 401
    

# USER STORY 3: RESET PASSWORD 
@app.route('/api/request-reset', methods=['POST'])
def request_reset():
    data = request.get_json(force=True, silent=True) or {}
    email = data.get('user_email')

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

    # if user exists, generate token and attach it to dictionary
    if user:
        token = str(uuid.uuid4())
        reset_tokens[token] = email
        return jsonify({"status": "success", "reset_token": token}), 200
    else:
        return jsonify({"status": "error", "error_message": "Email not found."}), 404


@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json(force=True, silent=True) or {}
    token = data.get('reset_token')
    new_password = data.get('new_password')

    email = reset_tokens.get(token)

    if email and new_password:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (hashed_password, email))
            conn.commit()
        
        # Revoke token after use
        if token in reset_tokens:
            del reset_tokens[token] 
        
        return jsonify({
            "status": "success",
            "message": "Password updated successfully.",
        }), 200
    else:
        return jsonify({"status": "error", "error_message": "Invalid or expired token."}), 400

if __name__ == '__main__':

    app.run(port=5000, debug=True)
