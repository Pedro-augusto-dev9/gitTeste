-- 1. Cria o banco de dados (se não existir) e entra nele
CREATE DATABASE IF NOT EXISTS meu_projeto;
USE meu_projeto;

-- 2. Cria a tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Cria a tabela de Tarefas (relacionada aos usuários)
CREATE TABLE IF NOT EXISTS tarefas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    concluida BOOLEAN DEFAULT FALSE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- Garante que a tarefa pertence a um usuário real da tabela acima
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 4. Insere dados de teste (Apenas para você testar as tabelas)
INSERT INTO usuarios (nome, email) VALUES 
('Pedro Augusto', 'pedroaugust.master10@gmail.com'),
('Maria Silva', 'maria.silva@email.com');

INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES 
(1, 'Estudar Git e GitHub', 'Praticar os comandos git add, commit e push no terminal.'),
(1, 'Aprender SQL', 'Criar e testar o script de criação de tabelas relacionais.'),
(2, 'Organizar repositório', 'Deixar a branch main atualizada e limpa.');

-- 5. Comando para visualizar tudo junto (Opcional)
-- SELECT t.id, u.nome AS 'Responsável', t.titulo, t.concluida 
-- FROM tarefas t 
-- JOIN usuarios u ON t.usuario_id = u.id;
