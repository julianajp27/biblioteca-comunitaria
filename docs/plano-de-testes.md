# Plano de Testes - Biblioteca Comunitária

**Projeto:** Biblioteca Comunitária - Cloud Challenge 06
**Disciplina:** Cloud Computing - Faculdade Senac Recife
**Responsável:** Lucas Querubim
**Papel:** QA - Planejamento de testes e documentação (issue #7)
**Versão:** 1.0

## 1. Objetivo

Definir a estratégia, o escopo e os casos de teste utilizados para validar a API
da Biblioteca Comunitária, verificando o atendimento aos requisitos funcionais,
às regras de negócio e à persistência dos dados em ambiente de nuvem.

## 2. Escopo

### 2.1 Em escopo

- Cadastro de livros com ISBN único.
- Consulta de livros por título ou autor.
- Cálculo de exemplares disponíveis.
- Registro de empréstimos com limite de 2 ativos por leitor.
- Prazo de devolução de 14 dias.
- Registro de devoluções e bloqueio de devolução duplicada.
- Consulta de empréstimos atrasados.
- Verificação de saúde da aplicação e da conexão com o banco.
- Validação de entradas e códigos de status HTTP.
- Persistência dos dados após reinicialização da aplicação.

### 2.2 Fora de escopo

- Testes de carga e desempenho.
- Testes de segurança e autenticação, pois a API não possui camada de
  autenticação nesta entrega.
- Cadastro de leitores por API, não previsto nos requisitos. Os leitores vêm da
  carga inicial em `banco/dados-iniciais.sql`.
- Interface de usuário, pois o projeto entrega apenas a API.

## 3. Ambientes de teste

| Ambiente | Aplicação | Banco de dados |
|---|---|---|
| Local | Flask em `localhost:5000` | PostgreSQL na Render |
| Nuvem | Azure App Service com Gunicorn | PostgreSQL na Render |

**URL pública:** `[INSERIR URL DO AZURE]`

### 3.1 Pré-condições gerais

- Tabelas `livros`, `leitores` e `emprestimos` criadas conforme
  `banco/schema.sql`.
- Carga inicial de leitores aplicada via `banco/dados-iniciais.sql`,
  resultando nos leitores de id 1 a 5.
- Variável de ambiente `DATABASE_URL` configurada com `sslmode=require`.
- Dependências de `requirements.txt` instaladas.

## 4. Estratégia

Os testes são funcionais, de caixa preta, executados por requisições HTTP
diretas às rotas da API. Cada caso registra método, rota, corpo enviado, status
HTTP esperado e corpo esperado. Os resultados são confrontados com consultas
diretas ao PostgreSQL quando o caso envolve persistência.

A execução cobre primeiro o ambiente local e depois o ambiente publicado no
Azure, de forma a identificar divergências entre os dois.

### 4.1 Critérios de aceite

- Todos os casos de prioridade alta aprovados.
- Nenhum defeito aberto de severidade alta.
- Evidência registrada para cada caso executado.

### 4.2 Critério de parada

A execução é interrompida se a rota `GET /health` não retornar `status: ok`,
pois isso indica indisponibilidade do banco e invalida os demais casos.

## 5. Casos de teste

### 5.1 Saúde e rota inicial

**QA-01 - Rota inicial responde**
Método: `GET /`
Esperado: HTTP 200 com JSON contendo `projeto`, `desafio`, `status` e o objeto
`rotas`.

**QA-02 - Saúde com banco conectado**
Método: `GET /health`
Esperado: HTTP 200 com `status: "ok"`, `banco: "conectado"` e campo
`iniciado_em` no formato ISO 8601.

**QA-03 - Saúde com banco indisponível (negativo)**
Pré-condição: `DATABASE_URL` apontando para host inválido.
Método: `GET /health`
Esperado: HTTP 503 com `status: "indisponivel"` e `banco: "sem_conexao"`.
Observação: executado apenas em ambiente local, para não interromper o serviço
publicado.

### 5.2 Cadastro de livros

**QA-04 - Cadastro válido**
Método: `POST /livros`
Corpo:

```json
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "isbn": "9788535910663",
  "exemplares": 5
}
```

Esperado: HTTP 201 com `id` numérico, mensagem de sucesso e os dados enviados.

**CA5 - ISBN duplicado (negativo)**
Pré-condição: QA-04 executado.
Método: `POST /livros` com o mesmo ISBN.
Esperado: HTTP 409 com `erro: "Ja existe um livro com este ISBN."`

**QA-05 - Corpo não é JSON válido (negativo)**
Método: `POST /livros` com corpo em texto puro.
Esperado: HTTP 400 com `erro: "Envie um JSON valido."`

**QA-06 - Campos obrigatórios ausentes (negativo)**
Corpo: `{"titulo": "Teste"}`
Esperado: HTTP 400 com `erro: "Titulo, autor e ISBN sao obrigatorios."`

**QA-07 - Campos apenas com espaços (negativo)**
Corpo: `{"titulo": "   ", "autor": "   ", "isbn": "   ", "exemplares": 1}`
Esperado: HTTP 400 com a mesma mensagem de QA-06.

**QA-08 - Exemplares igual a zero (negativo)**
Corpo: título, autor e ISBN válidos com `"exemplares": 0`
Esperado: HTTP 400 com
`erro: "Exemplares deve ser um inteiro maior ou igual a 1."`

**QA-09 - Exemplares em tipo inválido (negativo)**
Corpo: `"exemplares": "cinco"`
Esperado: HTTP 400 com a mesma mensagem de QA-08.

**QA-10 - Campo acima do limite (negativo)**
Corpo: título com mais de 200 caracteres, ou autor com mais de 150, ou ISBN com
mais de 20.
Esperado: HTTP 400 com `erro: "Um dos campos ultrapassa o limite permitido."`

### 5.3 Consulta de livros

**QA-11 - Listagem completa**
Método: `GET /livros`
Esperado: HTTP 200 com lista de objetos contendo `id`, `titulo`, `autor`,
`isbn`, `exemplares` e `disponiveis`.

**QA-12 - Busca por título**
Método: `GET /livros?busca=Casmurro`
Esperado: HTTP 200 com o registro de Dom Casmurro.

**QA-13 - Busca por autor**
Método: `GET /livros?busca=Machado`
Esperado: HTTP 200 com o mesmo registro.

**QA-14 - Busca sem resultado**
Método: `GET /livros?busca=zzzzzz`
Esperado: HTTP 200 com lista vazia.

**QA-15 - Disponibilidade reflete empréstimos ativos**
Pré-condição: um empréstimo ativo do livro consultado.
Método: `GET /livros?busca=Casmurro`
Esperado: campo `disponiveis` igual a `exemplares` menos a quantidade de
empréstimos ativos.

### 5.4 Empréstimos

**QA-16 - Empréstimo válido com prazo de 14 dias**
Método: `POST /emprestimos`
Corpo: `{"livro_id": 1, "leitor_id": 1}`
Esperado: HTTP 201 com `emprestado_em` e `previsto_para`, sendo a diferença
entre eles exatamente 14 dias.

**CA2 - Limite de 2 empréstimos ativos por leitor (negativo)**
Pré-condição: leitor com 2 empréstimos ativos.
Método: `POST /emprestimos` para um terceiro livro.
Esperado: HTTP 409 com `erro: "Leitor ja possui 2 emprestimos ativos."`

**CA1 - Sem exemplar disponível (negativo)**
Pré-condição: livro com todos os exemplares emprestados.
Método: `POST /emprestimos`
Esperado: HTTP 409 com `erro: "Nao ha exemplares disponiveis."`

**QA-17 - Livro inexistente (negativo)**
Corpo: `{"livro_id": 999999, "leitor_id": 1}`
Esperado: HTTP 404 com `erro: "Livro nao encontrado."`

**QA-18 - Leitor inexistente (negativo)**
Corpo: `{"livro_id": 1, "leitor_id": 999999}`
Esperado: HTTP 404 com `erro: "Leitor nao encontrado."`

**QA-19 - IDs inválidos (negativo)**
Corpo: `{"livro_id": -1, "leitor_id": 0}`
Esperado: HTTP 400 com
`erro: "livro_id e leitor_id devem ser inteiros positivos."`

**QA-20 - IDs em tipo inválido (negativo)**
Corpo: `{"livro_id": "1", "leitor_id": "1"}`
Esperado: HTTP 400 com a mesma mensagem de QA-19.

### 5.5 Devoluções

**CA3 - Devolução válida e devolução duplicada (negativo na segunda chamada)**
Método: `PATCH /emprestimos/<id>/devolver`
Esperado na primeira chamada: HTTP 200 com `devolvido_em` preenchido.
Esperado na segunda chamada: HTTP 409 com
`erro: "Este emprestimo ja foi devolvido."`

**QA-21 - Exemplar liberado após devolução**
Pré-condição: CA3 executado.
Método: `GET /livros?busca=<titulo>`
Esperado: `disponiveis` incrementado em uma unidade.

**QA-22 - Empréstimo inexistente (negativo)**
Método: `PATCH /emprestimos/999999/devolver`
Esperado: HTTP 404 com `erro: "Emprestimo nao encontrado."`

**QA-23 - ID não numérico na rota (negativo)**
Método: `PATCH /emprestimos/abc/devolver`
Esperado: HTTP 404, pois a rota exige um inteiro.

### 5.6 Atrasados

**CA4 - Listar empréstimos atrasados**
Pré-condição: empréstimo com `previsto_para` no passado e `devolvido_em` nulo,
ajustado diretamente no banco.
Método: `GET /emprestimos/atrasados`
Esperado: HTTP 200 com `total` maior que zero e o empréstimo presente em
`emprestimos_atrasados`, com título, autor e nome do leitor.

**QA-24 - Atrasado sai da lista após devolução**
Pré-condição: CA4 executado e o empréstimo devolvido.
Método: `GET /emprestimos/atrasados`
Esperado: o empréstimo não consta mais na lista.

**QA-25 - Empréstimo no prazo não aparece**
Pré-condição: empréstimo criado no momento do teste.
Método: `GET /emprestimos/atrasados`
Esperado: o empréstimo não consta na lista.

### 5.7 Persistência

**QA-26 - Persistência após reinício da aplicação**
Passos: cadastrar livro e empréstimo, reiniciar a aplicação no Azure App
Service, consultar novamente as rotas.
Esperado: os registros permanecem disponíveis.

**QA-27 - Conferência direta no banco**
Passos: executar `SELECT` em `livros` e `emprestimos` no PostgreSQL da Render.
Esperado: os registros criados pela API estão presentes e consistentes com as
respostas HTTP.

**QA-28 - Paridade entre schema local e banco remoto**
Passos: comparar as constraints de `banco/schema.sql` com as constraints
existentes no banco da Render.
Esperado: as constraints `emprestimos_prazo_14_dias` e
`emprestimos_devolucao_cronologica` presentes nos dois ambientes.

## 6. Matriz de rastreabilidade

| Requisito | Casos |
|---|---|
| Cadastrar livros com ISBN único | QA-04, CA5, QA-05 a QA-10 |
| Consultar livros por título ou autor | QA-11 a QA-15 |
| Emprestar livros disponíveis | QA-16, CA1, QA-17 a QA-20 |
| Limitar cada leitor a 2 empréstimos ativos | CA2 |
| Definir devolução prevista para 14 dias | QA-16, QA-28 |
| Registrar devoluções | CA3, QA-21 a QA-23 |
| Consultar empréstimos atrasados | CA4, QA-24, QA-25 |
| Persistência dos dados | QA-26, QA-27 |
| Disponibilidade do serviço | QA-01 a QA-03 |

## 7. Resumo quantitativo

| Indicador | Quantidade |
|---|---|
| Casos de teste documentados | 33 |
| Casos negativos | 18 |
| Critérios de aceite cobertos | CA1 a CA5 |

## 8. Registro de resultados

Os resultados da execução são registrados em `docs/relatorio-testes.md`, com o
acompanhamento item a item em `docs/checklist-validacao.md` e as evidências
correspondentes armazenadas na pasta `evidencias/`.
