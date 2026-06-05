# Simplified HTTPS Flask app as a single file.
# Now includes a single main page at root '/' with forms and JS for all actions.
# Auto-opens the browser to https://localhost:5000 after starting.
# Requires: pip install flask cryptography
# Run: python this_file.py

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import requests
import os
import threading
import webbrowser
import time

app = Flask(__name__)

# Database setup
DB_FILE = 'telegram_clone.db'

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, stars_balance INTEGER DEFAULT 0)''')
        c.execute('''CREATE TABLE gifts (id INTEGER PRIMARY KEY, name TEXT, description TEXT, image_url TEXT, owner_id INTEGER, level INTEGER DEFAULT 1)''')
        conn.commit()
        conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# API Endpoints (same as before)

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        c.execute('SELECT * FROM gifts WHERE owner_id = ?', (user['id'],))
        gifts = c.fetchall()
        
        return jsonify({
            'username': user['username'],
            'stars_balance': user['stars_balance'],
            'gifts': [{'id': g['id'], 'name': g['name'], 'description': g['description'], 'image_url': g['image_url'], 'level': g['level']} for g in gifts]
        })

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400
    
    with get_db() as conn:
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username) VALUES (?)', (username,))
            conn.commit()
            return jsonify({'message': 'User created', 'username': username})
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username exists'}), 400

@app.route('/add_stars', methods=['POST'])
def add_stars():
    data = request.json
    username = data.get('username')
    amount = data.get('amount', 0)
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET stars_balance = stars_balance + ? WHERE username = ?', (amount, username))
        conn.commit()
        if c.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': f'Added {amount} stars'})

@app.route('/create_gift', methods=['POST'])
def create_gift():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    image_path = data.get('image_path')
    owner_username = data.get('owner_username')
    
    image_url = f'https://cdn.changes.tg/{image_path}'
    
    try:
        resp = requests.head(image_url)
        if resp.status_code != 200:
            return jsonify({'error': 'Image not found on CDN'}), 400
    except:
        return jsonify({'error': 'CDN error'}), 500
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = ?', (owner_username,))
        owner = c.fetchone()
        if not owner:
            return jsonify({'error': 'Owner not found'}), 404
        
        c.execute('INSERT INTO gifts (name, description, image_url, owner_id, level) VALUES (?, ?, ?, ?, 1)',
                  (name, description, image_url, owner['id']))
        conn.commit()
        gift_id = c.lastrowid
        return jsonify({'message': 'Gift created', 'gift_id': gift_id})

@app.route('/send_gift', methods=['POST'])
def send_gift():
    data = request.json
    gift_id = data.get('gift_id')
    sender_username = data.get('sender_username')
    recipient_username = data.get('recipient_username')
    stars_cost = data.get('stars_cost', 0)
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id, stars_balance FROM users WHERE username = ?', (sender_username,))
        sender = c.fetchone()
        if not sender:
            return jsonify({'error': 'Sender not found'}), 404
        if stars_cost > sender['stars_balance']:
            return jsonify({'error': 'Insufficient stars'}), 400
        
        c.execute('SELECT id FROM users WHERE username = ?', (recipient_username,))
        recipient = c.fetchone()
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        
        c.execute('SELECT owner_id FROM gifts WHERE id = ?', (gift_id,))
        gift = c.fetchone()
        if not gift or gift['owner_id'] != sender['id']:
            return jsonify({'error': 'Gift not owned by sender'}), 404
        
        c.execute('UPDATE gifts SET owner_id = ? WHERE id = ?', (recipient['id'], gift_id))
        if stars_cost > 0:
            c.execute('UPDATE users SET stars_balance = stars_balance - ? WHERE id = ?', (stars_cost, sender['id']))
        conn.commit()
        return jsonify({'message': 'Gift sent'})

@app.route('/upgrade_gift', methods=['POST'])
def upgrade_gift():
    data = request.json
    gift_id = data.get('gift_id')
    owner_username = data.get('owner_username')
    stars_cost = data.get('stars_cost', 100)
    level_increase = data.get('level_increase', 1)
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT id, stars_balance FROM users WHERE username = ?', (owner_username,))
        owner = c.fetchone()
        if not owner:
            return jsonify({'error': 'Owner not found'}), 404
        if stars_cost > owner['stars_balance']:
            return jsonify({'error': 'Insufficient stars'}), 400
        
        c.execute('SELECT owner_id, level FROM gifts WHERE id = ?', (gift_id,))
        gift = c.fetchone()
        if not gift or gift['owner_id'] != owner['id']:
            return jsonify({'error': 'Gift not owned'}), 404
        
        new_level = gift['level'] + level_increase
        c.execute('UPDATE gifts SET level = ? WHERE id = ?', (new_level, gift_id))
        c.execute('UPDATE users SET stars_balance = stars_balance - ? WHERE id = ?', (stars_cost, owner['id']))
        conn.commit()
        return jsonify({'message': 'Gift upgraded', 'new_level': new_level})

# Single main page with all forms
@app.route('/')
def main_page():
    html = '''
    <html>
    <head><title>Telegram Gifts Demo</title></head>
    <body>
        <h1>Telegram Gifts Demo (Single Page)</h1>
        
        <h2>Create User</h2>
        <form id="createUserForm">
            <label>Username: <input name="username"></label><br>
            <button type="button" onclick="submitForm('createUserForm', '/create_user')">Create</button>
        </form>
        
        <h2>Add Stars</h2>
        <form id="addStarsForm">
            <label>Username: <input name="username"></label><br>
            <label>Amount: <input name="amount" type="number"></label><br>
            <button type="button" onclick="submitForm('addStarsForm', '/add_stars')">Add</button>
        </form>
        
        <h2>Create Gift</h2>
        <form id="createGiftForm">
            <label>Name: <input name="name"></label><br>
            <label>Description: <input name="description"></label><br>
            <label>Image Path (on CDN): <input name="image_path"></label><br>
            <label>Owner Username: <input name="owner_username"></label><br>
            <button type="button" onclick="submitForm('createGiftForm', '/create_gift')">Create</button>
        </form>
        
        <h2>Send Gift</h2>
        <form id="sendGiftForm">
            <label>Gift ID: <input name="gift_id" type="number"></label><br>
            <label>Sender Username: <input name="sender_username"></label><br>
            <label>Recipient Username: <input name="recipient_username"></label><br>
            <label>Stars Cost: <input name="stars_cost" type="number" value="0"></label><br>
            <button type="button" onclick="submitForm('sendGiftForm', '/send_gift')">Send</button>
        </form>
        
        <h2>Upgrade Gift</h2>
        <form id="upgradeGiftForm">
            <label>Gift ID: <input name="gift_id" type="number"></label><br>
            <label>Owner Username: <input name="owner_username"></label><br>
            <label>Stars Cost: <input name="stars_cost" type="number" value="100"></label><br>
            <label>Level Increase: <input name="level_increase" type="number" value="1"></label><br>
            <button type="button" onclick="submitForm('upgradeGiftForm', '/upgrade_gift')">Upgrade</button>
        </form>
        
        <h2>View Profile</h2>
        <form id="viewProfileForm">
            <label>Username: <input name="username"></label><br>
            <button type="button" onclick="viewProfile()">View</button>
        </form>
        <div id="profileResult"></div>
        
        <script>
            function submitForm(formId, url) {
                const form = document.getElementById(formId);
                const data = {};
                new FormData(form).forEach((value, key) => data[key] = value);
                fetch(url, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                }).then(response => response.json())
                  .then(result => alert(JSON.stringify(result)))
                  .catch(error => alert('Error: ' + error));
            }
            
            function viewProfile() {
                const form = document.getElementById('viewProfileForm');
                const username = form.querySelector('input[name="username"]').value;
                fetch(`/profile/${username}`)
                  .then(response => response.json())
                  .then(result => {
                      document.getElementById('profileResult').innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
                  })
                  .catch(error => alert('Error: ' + error));
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

# Function to open browser
def open_browser():
    time.sleep(1)  # Wait for server to start
    webbrowser.open('https://localhost:5000')

# Run the app with HTTPS
if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True, ssl_context='adhoc')