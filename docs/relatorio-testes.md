# Relatório de Execução de Testes - Biblioteca Comunitária

**Responsável:** Lucas Querubim - QA (issue #7)
**Data da execução:** [DD/MM/2026]
**Versão testada:** branch `main`, commit `[HASH]`
**Plano de referência:** `docs/plano-de-testes.md`
**Checklist:** `docs/checklist-validacao.md`

## 1. Ambiente utilizado

| Item | Valor |
|---|---|
| Aplicação | Azure App Service (Linux, Python 3.12, Gunicorn) |
| URL pública | `[INSERIR URL]` |
| Banco de dados | PostgreSQL na Render (`sslmode=require`) |
| Versão do PostgreSQL | `[INSERIR]` |
| Ferramenta de requisição | `[navegador / curl / Postman]` |

## 2. Resumo da execução

| Indicador | Quantidade |
|---|---|
| Casos planejados | 33 |
| Executados | [ ] |
| Aprovados | [ ] |
| Reprovados | [ ] |
| Não executados | [ ] |

## 3. Resultados por caso

| Caso | Descrição | Status esperado | Status obtido | Resultado | Evidência |
|---|---|---|---|---|---|
| QA-01 | Rota inicial | 200 | | | |
| QA-02 | Saúde com banco conectado | 200 | | | |
| QA-03 | Saúde com banco indisponível | 503 | | | |
| QA-04 | Cadastro válido | 201 | | | |
| CA5 | ISBN duplicado | 409 | | | |
| QA-05 | JSON inválido | 400 | | | |
| QA-06 | Campos obrigatórios ausentes | 400 | | | |
| QA-07 | Campos em branco | 400 | | | |
| QA-08 | Exemplares igual a zero | 400 | | | |
| QA-09 | Exemplares em tipo inválido | 400 | | | |
| QA-10 | Campo acima do limite | 400 | | | |
| QA-11 | Listagem completa | 200 | | | |
| QA-12 | Busca por título | 200 | | | |
| QA-13 | Busca por autor | 200 | | | |
| QA-14 | Busca sem resultado | 200 | | | |
| QA-15 | Disponibilidade correta | 200 | | | |
| QA-16 | Empréstimo válido, prazo de 14 dias | 201 | | | |
| CA2 | Limite de 2 empréstimos ativos | 409 | | | |
| CA1 | Sem exemplar disponível | 409 | | | |
| QA-17 | Livro inexistente | 404 | | | |
| QA-18 | Leitor inexistente | 404 | | | |
| QA-19 | IDs inválidos | 400 | | | |
| QA-20 | IDs em tipo inválido | 400 | | | |
| CA3 | Devolução e devolução duplicada | 200 / 409 | | | |
| QA-21 | Exemplar liberado após devolução | 200 | | | |
| QA-22 | Empréstimo inexistente | 404 | | | |
| QA-23 | ID não numérico na rota | 404 | | | |
| CA4 | Listar atrasados | 200 | | | |
| QA-24 | Atrasado sai da lista | 200 | | | |
| QA-25 | Empréstimo no prazo não aparece | 200 | | | |
| QA-26 | Persistência após reinício | 200 | | | |
| QA-27 | Conferência direta no banco | n/a | | | |
| QA-28 | Paridade de constraints | n/a | | | |

## 4. Defeitos e observações

### D-01 - URL pública ausente na documentação

**Severidade:** baixa
**Arquivo:** `docs/deploy-azure.md`, seção 6
**Descrição:** o documento mantém o marcador
`[INSERIR AQUI A URL PÚBLICA DA APLICAÇÃO]` no lugar do endereço real da
aplicação, o que impede a reprodução dos testes por terceiros.
**Ação sugerida:** preencher a URL pública do Azure App Service.
**Situação:** aberto

### D-02 - Divergência de constraint entre ambientes

**Severidade:** média
**Caso relacionado:** QA-28
**Descrição:** conforme registrado na documentação do grupo, o banco hospedado
na Render não exigia a restrição de 336 horas presente em `banco/schema.sql`.
Sem essa constraint, o ambiente publicado aceita empréstimos com prazo
diferente de 14 dias caso a regra falhe na camada da aplicação.
**Ação sugerida:** confirmar a aplicação da constraint
`emprestimos_prazo_14_dias` no banco remoto e registrar a evidência.
**Situação:** aberto

### D-03 - Nomes de arquivo incorretos na tabela de evidências

**Severidade:** baixa
**Arquivo:** `docs/deploy-azure.md`, seção 8
**Descrição:** a tabela lista arquivos com a extensão duplicada (`.png.png`),
divergindo dos nomes reais presentes na pasta `evidencias/`.
**Ação sugerida:** corrigir os nomes na tabela.
**Situação:** aberto

### D-04 - [Preencher se surgir novo achado]

## 5. Conclusão

[Preencher após a execução: indicar se os critérios de aceite foram atendidos,
quais casos reprovaram e quais defeitos permanecem abertos.]
