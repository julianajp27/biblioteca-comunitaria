
-- DESAFIO 06 - BIBLIOTECA COMUNITÁRIA
-- Sprint 1: Persistência
-- Banco de dados: PostgreSQL

-- Tabela de livros
CREATE TABLE livros (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    exemplares INTEGER NOT NULL
        CHECK (exemplares >= 1)
);

-- Tabela de leitores
CREATE TABLE leitores (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
);

-- Tabela de empréstimos
CREATE TABLE emprestimos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    livro_id INTEGER NOT NULL
        REFERENCES livros(id),
    leitor_id INTEGER NOT NULL
        REFERENCES leitores(id),
    emprestado_em TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    previsto_para TIMESTAMPTZ NOT NULL,
    devolvido_em TIMESTAMPTZ NULL,
    CONSTRAINT emprestimos_prazo_14_dias
        CHECK (previsto_para - emprestado_em = INTERVAL '336 hours'),
    CONSTRAINT emprestimos_devolucao_cronologica
        CHECK (devolvido_em IS NULL OR devolvido_em >= emprestado_em)
);
