
# Biblioteca Comunitária — Desafio 06

Projeto acadêmico da disciplina Cloud Computing — Faculdade Senac Recife.

## Objetivo
Desenvolver um sistema para gerenciar o cadastro de livros, empréstimos, devoluções e consultas de exemplares disponíveis.

## Equipe
Aline, Ingrid, Juliana, Julianne, Lucas e Renata.

## Requisitos
- Cadastrar livros com ISBN único.
- Consultar livros por título ou autor.
- Emprestar livros disponíveis.
- Limitar cada leitor a 2 empréstimos ativos.
- Definir devolução prevista para 14 dias.
- Registrar devoluções.
- Consultar empréstimos atrasados.

## Arquitetura planejada
Usuário → Aplicação/API → Banco de dados relacional

## Desenvolvimento
Sprint 1: Persistência de dados.
Sprint 2: Regras de negócio, implantação e testes.

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| `app.py` | Aplicação Flask e registro das rotas |
| `db.py` | Conexão com o PostgreSQL |
| `livros.py` | Consulta de livros e disponibilidade |
| `cadastro_livros.py` | Cadastro de livros |
| `emprestimos.py` | Registro de empréstimos e regras de negócio |
| `devolucoes.py` | Registro de devoluções |
| `atrasados.py` | Consulta de empréstimos atrasados |
| `banco/` | Scripts SQL de schema e carga inicial |
| `docs/` | Documentação de implantação e de testes |
| `tests/` | Instruções de reprodução dos testes |
| `evidencias/` | Capturas de tela e resultados |

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Informações do projeto e das rotas |
| GET | `/health` | Saúde da aplicação e da conexão com o banco |
| GET | `/livros` | Lista livros e exemplares disponíveis |
| GET | `/livros?busca=termo` | Busca por título ou autor |
| POST | `/livros` | Cadastra livro com ISBN único |
| POST | `/emprestimos` | Registra empréstimo |
| PATCH | `/emprestimos/<id>/devolver` | Registra devolução |
| GET | `/emprestimos/atrasados` | Lista empréstimos atrasados |

## Qualidade e testes

Responsável: Lucas Querubim (QA, issue #7)

| Documento | Conteúdo |
|---|---|
| `docs/plano-de-testes.md` | Escopo, estratégia, ambientes e casos de teste |
| `docs/checklist-validacao.md` | Checklist de validação por área funcional |
| `docs/relatorio-testes.md` | Resultados da execução e defeitos |
| `tests/README.md` | Instruções de reprodução dos testes |
| `evidencias/` | Capturas de tela e resultados |

### Critérios de aceitação do Desafio 06

| Caso | Regra validada | Resultado esperado |
|---|---|---|
| CA1 | Empréstimo sem exemplar disponível | HTTP 409 |
| CA2 | Mais de 2 empréstimos ativos por leitor | HTTP 409 |
| CA3 | Devolução duplicada | HTTP 200 e depois HTTP 409 |
| CA4 | Listagem de atrasados não devolvidos | HTTP 200 com os registros |
| CA5 | Cadastro de ISBN duplicado | HTTP 409 |

O plano documenta 33 casos de teste, sendo 18 negativos, cobrindo os critérios
de aceitação, as validações de entrada, os códigos de status HTTP e a
persistência dos dados.

## Implantação

Responsável: Julianne Valentim (NUVEM, issue #6)

A API está publicada no Microsoft Azure App Service com banco PostgreSQL
hospedado na Render. O processo está documentado em `docs/deploy-azure.md`.

## Status

Sprint 1 e Sprint 2 concluídas. Documentação de testes elaborada e execução em
andamento.
