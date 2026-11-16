# Testes - Biblioteca Comunitária

Documentação de testes do projeto, sob responsabilidade de Lucas Querubim
(QA, issue #7).

## Documentos

| Documento | Conteúdo |
|---|---|
| `../docs/plano-de-testes.md` | Escopo, estratégia, ambientes e os 33 casos de teste |
| `../docs/checklist-validacao.md` | Checklist de validação por área funcional |
| `../docs/relatorio-testes.md` | Resultados da execução, defeitos e conclusão |
| `../evidencias/` | Capturas de tela e resultados das requisições |

## Casos de aceite do desafio

- CA1: impedir empréstimo quando não houver exemplar disponível.
- CA2: impedir que um leitor tenha mais de 2 empréstimos ativos.
- CA3: registrar devolução e impedir devolução duplicada.
- CA4: listar empréstimos atrasados não devolvidos.
- CA5: impedir cadastro de ISBN duplicado.

Os casos CA1 a CA5 estão detalhados no plano de testes junto aos casos
complementares de validação de entrada, códigos de status HTTP, disponibilidade
do serviço e persistência dos dados.

## Como reproduzir os testes

### Ambiente local

```bash
pip install -r requirements.txt
# criar o arquivo .env a partir de .env.example
python app.py
```

A aplicação responde em `http://localhost:5000`.

### Ambiente publicado

Utilizar a URL pública do Azure App Service informada em
`docs/deploy-azure.md`.

### Exemplos de requisição

```bash
# Saúde da aplicação
curl -i http://localhost:5000/health

# Cadastro de livro
curl -i -X POST http://localhost:5000/livros \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Dom Casmurro","autor":"Machado de Assis","isbn":"9788535910663","exemplares":5}'

# Consulta por autor
curl -i "http://localhost:5000/livros?busca=Machado"

# Empréstimo
curl -i -X POST http://localhost:5000/emprestimos \
  -H "Content-Type: application/json" \
  -d '{"livro_id":1,"leitor_id":1}'

# Devolução
curl -i -X PATCH http://localhost:5000/emprestimos/1/devolver

# Atrasados
curl -i http://localhost:5000/emprestimos/atrasados
```

### Preparação de cenários

Para o caso CA4, ajustar a data prevista de um empréstimo ativo diretamente no
banco:

```sql
UPDATE emprestimos
SET emprestado_em = NOW() - INTERVAL '20 days',
    previsto_para = NOW() - INTERVAL '6 days'
WHERE id = 1;
```

Para conferir a persistência:

```sql
SELECT id, titulo, autor, isbn, exemplares FROM livros;

SELECT id, livro_id, leitor_id, emprestado_em,
       previsto_para, devolvido_em
FROM emprestimos;
```

Para conferir as constraints do banco (QA-28):

```sql
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'emprestimos'::regclass;
```
