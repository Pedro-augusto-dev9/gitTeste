import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "meu_projeto.db"


def inicializar_banco():
    """Cria as tabelas e insere dados iniciais se o banco estiver vazio."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Criação das tabelas (Adaptado para SQLite)
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

    # 2. Insere dados de teste apenas se a tabela de usuários estiver vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
            ("Pedro Augusto", "pedroaugust.master10@gmail.com"),
        )
        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
            ("Maria Silva", "maria.silva@email.com"),
        )

        cursor.execute(
            "INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
            (
                1,
                "Estudar Git e GitHub",
                "Praticar os comandos git add, commit e push no terminal.",
            ),
        )
        cursor.execute(
            "INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
            (
                1,
                "Aprender SQL",
                "Criar e testar o script de criação de tabelas relacionais.",
            ),
        )
        cursor.execute(
            "INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
            (2, "Organizar repositório", "Deixar a branch main atualizada e limpa."),
        )

    conn.commit()
    conn.close()


class AppSistema:

    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas e Usuários")
        self.root.geometry("650x550")

        # --- ABAS ---
        self.tab_control = ttk.Notebook(root)
        self.tab_usuarios = ttk.Frame(self.tab_control)
        self.tab_tarefas = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_usuarios, text="Usuários")
        self.tab_control.add(self.tab_tarefas, text="Tarefas")
        self.tab_control.pack(expand=1, fill="both")

        # Inicializa as interfaces de cada aba
        self.setup_aba_usuarios()
        self.setup_aba_tarefas()

        # Carrega os dados iniciais nas tabelas visuais
        self.atualizar_combobox_usuarios()
        self.listar_usuarios()
        self.listar_tarefas()

    # --- ABA USUÁRIOS ---
    def setup_aba_usuarios(self):
        # Formulário
        lbl_nome = tk.Label(self.tab_usuarios, text="Nome:")
        lbl_nome.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ent_nome = tk.Entry(self.tab_usuarios, width=30)
        self.ent_nome.grid(row=0, column=1, padx=10, pady=10)

        lbl_email = tk.Label(self.tab_usuarios, text="Email:")
        lbl_email.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ent_email = tk.Entry(self.tab_usuarios, width=30)
        self.ent_email.grid(row=1, column=1, padx=10, pady=10)

        btn_salvar = tk.Button(
            self.tab_usuarios, text="Salvar Usuário", command=self.salvar_usuario
        )
        btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

        # Visualização (Treeview)
        self.tree_usuarios = ttk.Treeview(
            self.tab_usuarios, columns=("ID", "Nome", "Email"), show="headings"
        )
        self.tree_usuarios.heading("ID", text="ID")
        self.tree_usuarios.heading("Nome", text="Nome")
        self.tree_usuarios.heading("Email", text="Email")
        self.tree_usuarios.column("ID", width=50, anchor="center")
        self.tree_usuarios.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

    def salvar_usuario(self):
        nome = self.ent_nome.get().strip()
        email = self.ent_email.get().strip()

        if not nome or not email:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.ent_nome.delete(0, tk.END)
            self.ent_email.delete(0, tk.END)

            self.listar_usuarios()
            self.atualizar_combobox_usuarios()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este e-mail já está cadastrado.")

    def listar_usuarios(self):
        for i in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(i)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios")
        for linha in cursor.fetchall():
            self.tree_usuarios.insert("", tk.END, values=linha)
        conn.close()

    # --- ABA TAREFAS ---
    def setup_aba_tarefas(self):
        # Formulário
        lbl_user = tk.Label(self.tab_tarefas, text="Responsável:")
        lbl_user.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.cb_usuarios = ttk.Combobox(self.tab_tarefas, width=27, state="readonly")
        self.cb_usuarios.grid(row=0, column=1, padx=10, pady=10)

        lbl_titulo = tk.Label(self.tab_tarefas, text="Título da Tarefa:")
        lbl_titulo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ent_titulo = tk.Entry(self.tab_tarefas, width=30)
        self.ent_titulo.grid(row=1, column=1, padx=10, pady=10)

        lbl_desc = tk.Label(self.tab_tarefas, text="Descrição:")
        lbl_desc.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        self.txt_desc = tk.Text(self.tab_tarefas, width=30, height=4)
        self.txt_desc.grid(row=2, column=1, padx=10, pady=10)

        btn_salvar_tarefa = tk.Button(
            self.tab_tarefas, text="Salvar Tarefa", command=self.salvar_tarefa
        )
        btn_salvar_tarefa.grid(row=3, column=0, columnspan=2, pady=10)

        # Visualização (Treeview)
        self.tree_tarefas = ttk.Treeview(
            self.tab_tarefas,
            columns=("ID", "Responsavel", "Titulo", "Descricao"),
            show="headings",
        )
        self.tree_tarefas.heading("ID", text="ID")
        self.tree_tarefas.heading("Responsavel", text="Responsável")
        self.tree_tarefas.heading("Titulo", text="Título")
        self.tree_tarefas.heading("Descricao", text="Descrição")
        self.tree_tarefas.column("ID", width=40, anchor="center")
        self.tree_tarefas.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

    def atualizar_combobox_usuarios(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios")
        self.lista_usuarios_db = cursor.fetchall()
        conn.close()

        # Preenche o combobox mostrando "ID - Nome"
        self.cb_usuarios["values"] = [
            f"{u[0]} - {u[1]}" for u in self.lista_usuarios_db
        ]

    def salvar_tarefa(self):
        selecionado = self.cb_usuarios.get()
        titulo = self.ent_titulo.get().strip()
        descricao = self.txt_desc.get("1.0", tk.END).strip()

        if not selecionado or not titulo:
            messagebox.showwarning("Erro", "Selecione um usuário e digite um título!")
            return

        # Pega o ID do usuário (número antes do primeiro hífen)
        usuario_id = int(selecionado.split(" - ")[0])

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
            (usuario_id, titulo, descricao),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Tarefa cadastrada com sucesso!")
        self.ent_titulo.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)
        self.listar_tarefas()

    def listar_tarefas(self):
        for i in self.tree_tarefas.get_children():
            self.tree_tarefas.delete(i)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Faz o JOIN exatamente como sugerido no seu script SQL original
        cursor.execute(
            """
            SELECT t.id, u.nome, t.titulo, t.descricao 
            FROM tarefas t 
            JOIN usuarios u ON t.usuario_id = u.id
        """
        )
        for linha in cursor.fetchall():
            self.tree_tarefas.insert("", tk.END, values=linha)
        conn.close()


if __name__ == "__main__":
    inicializar_banco()
    root = tk.Tk()
    app = AppSistema(root)
    root.mainloop()
