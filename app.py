from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DB_NAME = 'inventory.db'

# Init DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        name TEXT,
        location TEXT,
        status TEXT,
        last_update TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        action TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    code = data.get('code')
    action = data.get('action')
    name = data.get('name')
    location = data.get('location')
    status = data.get('status')

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if item exists
    c.execute("SELECT * FROM items WHERE code = ?", (code,))
    item = c.fetchone()

    if item:
        c.execute("UPDATE items SET location = ?, status = ?, last_update = ? WHERE code = ?", (location, status, timestamp, code))
    else:
        c.execute("INSERT INTO items (code, name, location, status, last_update) VALUES (?, ?, ?, ?, ?)", (code, name, location, status, timestamp))

    c.execute("INSERT INTO log (code, action, timestamp) VALUES (?, ?, ?)", (code, action, timestamp))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/items')
def get_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT code, name, location, status, last_update FROM items")
    items = c.fetchall()
    conn.close()
    return render_template('items.html', items=items)

@app.route('/log')
def get_log():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT code, action, timestamp FROM log ORDER BY timestamp DESC")
    logs = c.fetchall()
    conn.close()
    return render_template('log.html', logs=logs)

if __name__ == '__main__':
    init_db()
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True, host='0.0.0.0')
