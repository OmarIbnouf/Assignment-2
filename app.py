from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Helper function to add a new transaction
def add_transaction(transaction_type, category, amount):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)''',
              (transaction_type, category, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# Helper function to retrieve all transactions
def get_transactions():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return transactions

# Helper function to calculate income, expenses, and balance
def calculate_summary():
    transactions = get_transactions()
    total_income = sum(t[3] for t in transactions if t[1] == 'income')
    total_expenses = sum(t[3] for t in transactions if t[1] == 'expense')
    remaining_balance = total_income - total_expenses
    return total_income, total_expenses, remaining_balance

@app.route('/')
def index():
    transactions = get_transactions()
    total_income, total_expenses, remaining_balance = calculate_summary()
    return render_template('index.html', transactions=transactions, total_income=total_income,
                           total_expenses=total_expenses, remaining_balance=remaining_balance)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        transaction_type = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])
        add_transaction(transaction_type, category, amount)
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)