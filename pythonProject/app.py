from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('educational.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cursos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    carga_horaria INTEGER NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    descricao TEXT,
                    tipo TEXT CHECK(tipo IN ('aula', 'evento')) NOT NULL
                )''')
    conn.commit()
    conn.close()

criar_tabelas()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    conn = get_db_connection()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        carga_horaria = request.form['carga_horaria']
        conn.execute('INSERT INTO cursos (titulo, descricao, carga_horaria) VALUES (?, ?, ?)',
                     (titulo, descricao, carga_horaria))
        conn.commit()
        return redirect(url_for('cursos'))
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    conn.close()
    return render_template('cursos.html', cursos=cursos)

@app.route('/eventos', methods=['GET', 'POST'])
def eventos():
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.form['data']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        conn.execute('INSERT INTO eventos (data, descricao, tipo) VALUES (?, ?, ?)',
                     (data, descricao, tipo))
        conn.commit()
        return redirect(url_for('eventos'))
    eventos = conn.execute('SELECT * FROM eventos').fetchall()
    conn.close()
    return render_template('eventos.html', eventos=eventos)

if __name__ == "__main__":
    app.run(debug=True)