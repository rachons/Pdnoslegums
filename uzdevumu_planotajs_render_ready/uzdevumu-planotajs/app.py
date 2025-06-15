from flask import Flask, render_template, request, redirect, session
import sqlite3, bcrypt
import os

app = Flask(__name__)
app.secret_key = 'slepena_atslega'

def init_db():
    if not os.path.exists('planotajs.db'):
        conn = sqlite3.connect('planotajs.db')
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.close()

def get_db():
    conn = sqlite3.connect('planotajs.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def before_first_request():
    init_db()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    tasks = db.execute('SELECT * FROM uzdevumi WHERE lietotajs_id = ?', (session['user_id'],)).fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute('SELECT * FROM lietotaji WHERE lietotajvards = ?', (request.form['lietotajvards'],)).fetchone()
        if user and bcrypt.checkpw(request.form['parole'].encode(), user['parole']):
            session['user_id'] = user['id']
            return redirect('/')
    return render_template('login.html')

@app.route('/add', methods=['POST'])
def add():
    db = get_db()
    db.execute('INSERT INTO uzdevumi (lietotajs_id, nosaukums, termins, prioritate) VALUES (?, ?, ?, ?)',
               (session['user_id'], request.form['nosaukums'], request.form['termins'], request.form['prioritate']))
    db.commit()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
