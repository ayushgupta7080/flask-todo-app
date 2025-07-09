from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create the DB and tasks table (if not exists)
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            is_done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET is_done = NOT is_done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/clear')
def clear_all():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    if request.method == 'POST':
        new_content = request.form.get('task')
        c.execute("UPDATE tasks SET content = ? WHERE id = ?", (new_content, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
