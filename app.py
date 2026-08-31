import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DB_NAME = "meu_projeto.db"


def inicializar_banco():
    """Cria as tabelas se não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        descricao TEXT,
        concluida BOOLEAN DEFAULT 0,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    );
    """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Página principal que lista usuários e tarefas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Busca todos os usuários
    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()

    # Busca as tarefas fazendo JOIN com os usuários
    cursor.execute(
        """
        SELECT t.id, u.nome, t.titulo, t.descricao 
        FROM tarefas t 
        JOIN usuarios u ON t.usuario_id = u.id
    """
    )
    tarefas = cursor.fetchall()

    conn.close()
    return render_template("index.html", usuarios=usuarios, tarefas=tarefas)


@app.route("/add_usuario", methods=["POST"])
def add_usuario():
    """Rota para cadastrar novo usuário."""
    nome = request.form.get("nome")
    email = request.form.get("email")

    if nome and email:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
                (nome, email),
            )
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            pass  # Email já cadastrado

    return redirect(url_for("index"))


@app.route("/add_tarefa", methods=["POST"])
def add_tarefa():
    """Rota para cadastrar nova tarefa."""
    usuario_id = request.form.get("usuario_id")
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")

    if usuario_id and titulo:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
            (usuario_id, titulo, descricao),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
