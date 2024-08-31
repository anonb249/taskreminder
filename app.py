from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    db.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        db = get_db()
        cur = db.cursor()
        cur.execute('INSERT INTO tasks (description) VALUES (?)', (task,))
        db.commit()
        db.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    db.close()
    return '', 204  # No content

if __name__ == '__main__':
    app.run(debug=True)
