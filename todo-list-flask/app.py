from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Use /tmp folder on Vercel (writable), local path otherwise
DB_PATH = '/tmp/database.db' if os.environ.get('VERCEL') else 'database.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Auto-initialize DB on startup
init_db()

@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    date = request.form['date']
    conn = get_db()
    conn.execute('INSERT INTO tasks (task, date, status) VALUES (?, ?, ?)',
                 (task, date, 'Pending'))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    conn.execute('UPDATE tasks SET status="Completed" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)