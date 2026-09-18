import sqlite3
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = 'budget.db'

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Utility function to get a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions ORDER BY date DESC, id DESC').fetchall()
    conn.close()
    return jsonify([dict(tx) for tx in transactions])

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    description = data.get('description')
    amount = float(data.get('amount', 0))
    tx_type = data.get('type')
    category = data.get('category')
    date = data.get('date')

    if not description or amount <= 0 or not tx_type or not category or not date:
        return jsonify({'error': 'Invalid input fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)',
        (description, amount, tx_type, category, date)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        'id': new_id,
        'description': description,
        'amount': amount,
        'type': tx_type,
        'category': category,
        'date': date
    }), 201

@app.route('/api/transactions/<int:tx_id>', methods=['DELETE'])
def delete_transaction(tx_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transactions WHERE id = ?', (tx_id,))
    conn.commit()
    conn.close()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    # Automatically initialize DB before running server
    init_db()
    print("Database initialized successfully.")
    print("Starting Web Server at http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)