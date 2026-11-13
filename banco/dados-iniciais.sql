
-- DESAFIO 06 - BIBLIOTECA COMUNITÁRIA
-- Sprint 1: Dados iniciais
-- Leitores fictícios para testes

BEGIN;

-- Serializa reexecuções e evita inserções concorrentes durante a carga.
LOCK TABLE leitores IN SHARE ROW EXCLUSIVE MODE;

-- Nomes iguais já cadastrados são preservados, sem exigir nomes únicos.
INSERT INTO leitores (nome)
SELECT iniciais.nome
FROM (VALUES
    ('Ana Oliveira'),
    ('Bruno Almeida'),
    ('Carla Souza'),
    ('Daniel Ferreira'),
    ('Fernanda Lima')
) AS iniciais(nome)
WHERE NOT EXISTS (
    SELECT 1
    FROM leitores
    WHERE leitores.nome = iniciais.nome
);

COMMIT;
