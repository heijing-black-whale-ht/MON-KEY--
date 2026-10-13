from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   done INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()

    # 1. Start the counter at zero
    pending_count = 0

    # 2. Loop through the list of tasks
    for task in tasks:
        # 3. Check if the task is NOT done (0)
        if task['done'] == 0:
            # 4. Add 1 to the counter
            pending_count = pending_count + 1

    # 5. Hand both variables off to the HTML templates
    return render_template('index.html', tasks=tasks, pending_count=pending_count)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = get_db()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn = get_db()

    task = conn.execute('SELECT done FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task:
        new_status = 0 if task['done'] == 1 else 1
        conn.execute('UPDATE tasks SET done = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
        
    conn.close()
    return redirect(url_for('index'))

@app.route('/home')
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)