# Checklist de Validação - Biblioteca Comunitária

**Projeto:** Biblioteca Comunitária - Cloud Challenge 06
**Responsável:** Lucas Querubim - QA (issue #7)
**Referência:** `docs/plano-de-testes.md`

Marcar cada item após a verificação. Registrar a evidência correspondente na
pasta `evidencias/`.

## 1. Pré-requisitos do ambiente

- [ ] Tabelas `livros`, `leitores` e `emprestimos` criadas
- [ ] Constraint `emprestimos_prazo_14_dias` ativa no banco
- [ ] Constraint `emprestimos_devolucao_cronologica` ativa no banco
- [ ] Restrição UNIQUE no campo `isbn` confirmada
- [ ] Carga inicial de leitores aplicada (ids 1 a 5)
- [ ] `DATABASE_URL` configurada com `sslmode=require`
- [ ] Dependências de `requirements.txt` instaladas sem erro
- [ ] Aplicação publicada e acessível pela URL pública

## 2. Disponibilidade do serviço

- [ ] `GET /` responde 200 com os dados do projeto
- [ ] `GET /health` responde 200 com `banco: "conectado"`
- [ ] `GET /health` responde 503 quando o banco está indisponível
- [ ] Todas as rotas listadas em `/` respondem

## 3. Cadastro de livros

- [ ] Cadastro válido retorna 201 com `id` gerado
- [ ] ISBN duplicado retorna 409 (CA5)
- [ ] Corpo não JSON retorna 400
- [ ] Campos obrigatórios ausentes retornam 400
- [ ] Campos apenas com espaços retornam 400
- [ ] `exemplares` igual a 0 retorna 400
- [ ] `exemplares` negativo retorna 400
- [ ] `exemplares` como texto retorna 400
- [ ] Título acima de 200 caracteres retorna 400
- [ ] Autor acima de 150 caracteres retorna 400
- [ ] ISBN acima de 20 caracteres retorna 400

## 4. Consulta de livros

- [ ] `GET /livros` lista todos os registros
- [ ] Busca por título retorna o livro correto
- [ ] Busca por autor retorna o livro correto
- [ ] Busca é insensível a maiúsculas e minúsculas
- [ ] Busca parcial funciona com trecho do título
- [ ] Busca sem correspondência retorna lista vazia
- [ ] Campo `disponiveis` é exibido em todos os registros
- [ ] `disponiveis` desconta os empréstimos ativos
- [ ] `disponiveis` volta ao total após as devoluções

## 5. Empréstimos

- [ ] Empréstimo válido retorna 201
- [ ] `previsto_para` é exatamente 14 dias após `emprestado_em`
- [ ] Segundo empréstimo do mesmo leitor é aceito
- [ ] Terceiro empréstimo do mesmo leitor retorna 409 (CA2)
- [ ] Empréstimo sem exemplar disponível retorna 409 (CA1)
- [ ] Livro inexistente retorna 404
- [ ] Leitor inexistente retorna 404
- [ ] `livro_id` ou `leitor_id` negativo retorna 400
- [ ] `livro_id` ou `leitor_id` igual a 0 retorna 400
- [ ] IDs enviados como texto retornam 400
- [ ] Corpo sem os campos obrigatórios retorna 400

## 6. Devoluções

- [ ] Devolução válida retorna 200 com `devolvido_em`
- [ ] Segunda devolução do mesmo empréstimo retorna 409 (CA3)
- [ ] Exemplar volta a ficar disponível após a devolução
- [ ] Leitor volta a poder emprestar após a devolução
- [ ] Empréstimo inexistente retorna 404
- [ ] ID não numérico na rota retorna 404

## 7. Empréstimos atrasados

- [ ] Empréstimo vencido e não devolvido aparece na lista (CA4)
- [ ] Resposta traz `total` com a contagem correta
- [ ] Cada item traz título, autor e nome do leitor
- [ ] Empréstimo dentro do prazo não aparece
- [ ] Empréstimo devolvido não aparece, mesmo vencido
- [ ] Ordenação segue a data prevista em ordem crescente

## 8. Persistência

- [ ] Registros permanecem após reiniciar a aplicação
- [ ] `SELECT` em `livros` confirma os cadastros feitos pela API
- [ ] `SELECT` em `emprestimos` confirma os empréstimos registrados
- [ ] Datas gravadas no banco conferem com as respostas HTTP
- [ ] Devoluções gravam `devolvido_em` no banco

## 9. Documentação e evidências

- [ ] Plano de testes versionado no repositório
- [ ] Checklist preenchido e versionado
- [ ] `README.md` com a seção de qualidade e testes
- [ ] Pasta `evidencias/` com README atualizado
- [ ] Uma evidência por caso de teste executado
- [ ] Evidências seguindo a nomenclatura padronizada
- [ ] Capturas exibindo rota, status HTTP e corpo da resposta
- [ ] URL pública preenchida em `docs/deploy-azure.md`
- [ ] Defeitos encontrados registrados em `docs/relatorio-testes.md`

## 10. Critérios de aceite do Desafio 06

- [ ] CA1 validado e com evidência
- [ ] CA2 validado e com evidência
- [ ] CA3 validado e com evidência
- [ ] CA4 validado e com evidência
- [ ] CA5 validado e com evidência

## Encerramento

Assinatura do QA: ______________________

Data: ____/____/2026

Resultado geral: [ ] Aprovado  [ ] Aprovado com ressalvas  [ ] Reprovado
