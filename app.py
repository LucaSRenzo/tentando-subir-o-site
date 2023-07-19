import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'database.db'

def criar_tabela():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mensagens
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       email TEXT NOT NULL,
                       mensagem TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mensagens (nome, email, mensagem) VALUES (?, ?, ?)',
                       (nome, email, mensagem))
        conn.commit()
        conn.close()

        return redirect(url_for('mensagens'))

    return render_template('contato.html')

@app.route('/mensagens')
def mensagens():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mensagens')
    mensagens = cursor.fetchall()
    conn.close()

    return render_template('mensagens.html', mensagens=mensagens)

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)


