DROP TABLE IF EXISTS pecas;
DROP TABLE IF EXISTS servicos;

CREATE TABLE pecas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    preco NUMERIC(10,2) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    categoria VARCHAR(50)
);

CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10,2) NOT NULL,
    duracao INTEGER -- duração em minutos
);

INSERT INTO pecas (nome, descricao, preco, quantidade, categoria) VALUES
('Kit Relacao', 'Kit com corrente e pinhoes', 250.00, 10, 'Transmissão'),
('Pastilha de Freio', 'Pastilha de freio dianteiro', 50.00, 25, 'Freio');

INSERT INTO servicos (nome, descricao, preco, duracao) VALUES
('Troca de OleO', 'Troca completa com filtro', 80.00, 30),
('Revisao Completa', 'Checagem geral com troca de peças', 500.00, 120);
