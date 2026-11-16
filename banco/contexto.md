# Implementação PostgreSQL — Biblioteca Comunitária

## 1. Objetivo

Implementar a camada de persistência de dados do projeto Biblioteca Comunitária utilizando PostgreSQL, com banco hospedado na Render.

O trabalho contemplou a criação das tabelas, definição de relacionamentos, aplicação de restrições de integridade, criação de índices, inserção de dados iniciais e atualização das regras de empréstimo.

## 2. Tecnologias utilizadas

- PostgreSQL 18
- Render — hospedagem do banco de dados
- psql — ferramenta de acesso e execução de comandos SQL
- Visual Studio Code — edição dos scripts SQL

## 3. Estrutura do banco de dados

Foi criado o banco `biblioteca_comunitaria`, contendo três tabelas principais:

### 3.1. Tabela `livros`

Responsável por armazenar os livros disponíveis na biblioteca.

Campos:
- `id`: identificador único, gerado automaticamente e chave primária.
- `titulo`: título do livro.
- `autor`: nome do autor.
- `isbn`: código ISBN, com restrição de unicidade.
- `exemplares`: quantidade de exemplares disponíveis.

Restrições:
- Campos obrigatórios definidos com `NOT NULL`.
- ISBN único.
- Quantidade de exemplares deve ser igual ou superior a 1.

### 3.2. Tabela `leitores`

Responsável por armazenar os leitores cadastrados.

Campos:
- `id`: identificador único, gerado automaticamente e chave primária.
- `nome`: nome do leitor.

### 3.3. Tabela `emprestimos`

Responsável por registrar os empréstimos de livros.

Campos:
- `id`: identificador único, gerado automaticamente e chave primária.
- `livro_id`: referência ao livro emprestado.
- `leitor_id`: referência ao leitor responsável pelo empréstimo.
- `emprestado_em`: data e horário do empréstimo, preenchidos automaticamente.
- `previsto_para`: data e horário previstos para devolução, inicialmente definidos para 14 dias após o empréstimo.
- `devolvido_em`: data e horário da devolução efetiva, permitindo valor nulo enquanto o empréstimo estiver ativo.

Restrições:
- Chaves estrangeiras para as tabelas `livros` e `leitores`.
- Exclusão restrita para registros referenciados.
- Data prevista de devolução não pode ser anterior ao empréstimo.
- Data efetiva de devolução não pode ser anterior ao empréstimo.

## 4. Índices criados

Foram criados índices para otimizar consultas frequentes:

- `idx_livros_titulo`: pesquisas por título.
- `idx_livros_autor`: pesquisas por autor.
- `idx_emprestimos_leitor_ativos`: localização de empréstimos ativos por leitor.
- `idx_emprestimos_livro_ativos`: localização de empréstimos ativos por livro.
- `idx_emprestimos_atrasados`: consultas de empréstimos em atraso.

Os índices relacionados aos empréstimos ativos utilizam condições para considerar apenas registros ainda não devolvidos.

## 5. Dados iniciais

Foi realizada a carga inicial de leitores utilizando um comando `INSERT` com proteção `WHERE NOT EXISTS`, evitando a inserção de nomes que já estivessem cadastrados.

Leitores inseridos:
- Ana Oliveira
- Bruno Almeida
- Carla Souza
- Daniel Ferreira
- Fernanda Lima

A carga inicial foi executada no banco hospedado na Render.

## 6. Hospedagem e conexão com a Render

O banco foi disponibilizado na plataforma Render.

A conexão foi realizada por meio do cliente `psql`, utilizando:
- Host do banco hospedado na Render.
- Porta 5432.
- Banco `biblioteca_comunitaria`.
- Usuário autorizado.
- Conexão SSL obrigatória.

A conexão foi estabelecida com sucesso, permitindo executar os scripts e consultar os dados remotamente.

A variável `DATABASE_URL` compartilhada foi mantida, sem alteração durante esta implementação, preservando a configuração utilizada pelos demais integrantes e ambientes do projeto.

**Segurança:** credenciais e senhas não devem ser incluídas nos scripts versionados ou no GitHub. A rotação da credencial anteriormente exposta deve ser coordenada com os responsáveis pelos ambientes compartilhados.

## 7. Atualização da regra de prazo dos empréstimos

Foi identificada a necessidade de adicionar uma restrição para garantir que a data prevista de devolução corresponda exatamente a 336 horas após a realização do empréstimo.

A restrição criada foi:

`emprestimos_prazo_14_dias`

Comando executado:

```sql
BEGIN;

SET LOCAL lock_timeout = '5s';

ALTER TABLE public.emprestimos
ADD CONSTRAINT emprestimos_prazo_14_dias
CHECK (
    previsto_para =
    emprestado_em + INTERVAL '336 hours'
);

COMMIT;
```

### 7.1. Verificações realizadas antes da alteração

Antes da inclusão da restrição, foram realizadas consultas para verificar a integridade dos registros existentes.

Resultado da consulta de empréstimos incompatíveis:

- Total de registros incompatíveis: 0.

Contagem de registros antes da alteração:

| Tabela | Quantidade |
|---|---:|
| livros | 2 |
| leitores | 5 |
| emprestimos | 3 |

Também foi verificado que a restrição `emprestimos_prazo_14_dias` ainda não existia.

### 7.2. Resultado da execução

A alteração foi executada com sucesso no PostgreSQL da Render.

Retorno apresentado pelo terminal:

```text
BEGIN
SET
ALTER TABLE
COMMIT
```

Isso confirma que a restrição foi adicionada e a transação foi confirmada.

## 8. Validações finais pendentes

A execução do `ALTER TABLE` foi concluída com sucesso. Para finalizar a documentação técnica da alteração, ainda podem ser realizadas as seguintes verificações:

**Verificar a restrição:**

```sql
SELECT
    conname,
    pg_get_constraintdef(oid) AS definicao,
    convalidated
FROM pg_constraint
WHERE conrelid = 'public.emprestimos'::regclass
  AND conname = 'emprestimos_prazo_14_dias';
```

**Conferir as quantidades:**

```sql
SELECT 'livros' AS tabela, COUNT(*) AS quantidade
FROM public.livros

UNION ALL

SELECT 'leitores', COUNT(*)
FROM public.leitores

UNION ALL

SELECT 'emprestimos', COUNT(*)
FROM public.emprestimos;
```

**Verificar novamente os prazos:**

```sql
SELECT COUNT(*) AS total_incompativel
FROM public.emprestimos
WHERE previsto_para IS DISTINCT FROM
      emprestado_em + INTERVAL '336 hours';
```

Essas consultas foram preparadas para a conferência posterior à alteração. Seus resultados finais ainda não foram registrados nesta documentação.

## 9. Arquivos relacionados

Arquivos previstos para versionamento no repositório:

- `schema.sql`: criação das tabelas, relacionamentos, restrições e índices.
- `dados-iniciais.sql`: inserção dos dados iniciais.
- `contexto.md`: documentação das atividades realizadas.

## 10. Resultado da implementação

Foi realizada a implementação da estrutura de persistência da Biblioteca Comunitária utilizando PostgreSQL, com banco hospedado na Render.

As tabelas, os relacionamentos, as restrições iniciais e os índices foram criados. Os dados iniciais de leitores foram inseridos e a nova restrição de prazo de empréstimos foi adicionada com sucesso.

A alteração foi realizada diretamente na estrutura existente, sem recriação das tabelas, exclusão dos dados cadastrados ou modificação da URL de conexão compartilhada.

**Status:** alteração SQL executada e confirmada. Validações finais e rotação coordenada da credencial permanecem como atividades de acompanhamento.