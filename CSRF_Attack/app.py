from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL)')
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template('transfer.html', username=username)
    else:
        return "Invalid Credentials!"

@app.route('/transfer', methods=['POST'])
def transfer():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)", (sender, receiver, amount))
    conn.commit()
    conn.close()

    return f"Transferred {amount} to {receiver}!"

@app.route('/transactions')
def transactions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
