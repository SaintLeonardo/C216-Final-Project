DROP TABLE IF EXISTS pecas;
DROP TABLE IF EXISTS servicos;

CREATE TABLE pecas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    preco NUMERIC(10,2) NOT NULL
);

CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco NUMERIC(10,2) NOT NULL
);

INSERT INTO pecas (nome, descricao, preco) VALUES
('Kit Relacao', 'Kit com corrente e pinhoes', 250.00),
('Pastilha de Freio', 'Pastilha de freio dianteiro', 50.00);

INSERT INTO servicos (nome, preco) VALUES
('Troca de OleO', 80.00),
('Revisao Completa', 500.00);