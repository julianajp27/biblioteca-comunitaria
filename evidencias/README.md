# Evidências - Biblioteca Comunitária

Registros das validações do projeto Cloud Challenge 06.

## Evidências de infraestrutura e deploy

Responsável: Julianne Valentim (NUVEM, issue #6)

| Arquivo | Descrição |
|---|---|
| `01-AmbienteAzure.png` | Configuração do Azure App Service |
| `02-API-Azure-Funcionando.png` | Resposta da API pela URL pública |
| `03-configuracao-gunicorn-azure.png` | Comando de inicialização com Gunicorn |
| `04-variaveis-ambiente-azure.png` | Variáveis de ambiente configuradas |
| `05-logs-aplicacao-azure.png` | Fluxo de logs do App Service |
| `06-health-banco-conectado.png` | Rota `/health` com o banco conectado |

## Evidências de testes funcionais

Responsável: Lucas Querubim (QA, issue #7)

Padrão de nomenclatura: `qa-<caso>-<descricao>.png`

| Arquivo | Caso | Descrição |
|---|---|---|
| `qa-01-rota-inicial.png` | QA-01 | Resposta da rota `/` |
| `qa-02-health-ok.png` | QA-02 | Rota `/health` com banco conectado |
| `qa-03-health-indisponivel.png` | QA-03 | Rota `/health` sem conexão |
| `qa-04-cadastro-201.png` | QA-04 | Cadastro de livro aprovado |
| `qa-ca5-isbn-duplicado-409.png` | CA5 | ISBN duplicado recusado |
| `qa-validacoes-400.png` | QA-05 a QA-10 | Validações de entrada |
| `qa-11-listagem.png` | QA-11 | Listagem de livros |
| `qa-12-busca-titulo.png` | QA-12 | Busca por título |
| `qa-13-busca-autor.png` | QA-13 | Busca por autor |
| `qa-15-disponibilidade.png` | QA-15 | Disponibilidade calculada |
| `qa-16-emprestimo-14-dias.png` | QA-16 | Empréstimo com prazo correto |
| `qa-ca2-limite-leitor-409.png` | CA2 | Limite de 2 empréstimos ativos |
| `qa-ca1-sem-exemplar-409.png` | CA1 | Empréstimo sem exemplar disponível |
| `qa-17-18-nao-encontrado-404.png` | QA-17, QA-18 | Livro e leitor inexistentes |
| `qa-19-20-ids-invalidos-400.png` | QA-19, QA-20 | IDs inválidos |
| `qa-ca3-devolucao-200.png` | CA3 | Devolução registrada |
| `qa-ca3-devolucao-duplicada-409.png` | CA3 | Devolução duplicada recusada |
| `qa-22-23-devolucao-404.png` | QA-22, QA-23 | Empréstimo inexistente e id inválido |
| `qa-ca4-atrasados.png` | CA4 | Lista de empréstimos atrasados |
| `qa-24-atrasado-removido.png` | QA-24 | Atrasado removido após devolução |
| `qa-26-persistencia-reinicio.png` | QA-26 | Dados após reiniciar a aplicação |
| `qa-27-consulta-banco.png` | QA-27 | Consulta direta no PostgreSQL |
| `qa-28-constraints-banco.png` | QA-28 | Constraints do banco remoto |

## Orientações de registro

- Cada captura deve exibir a rota requisitada, o código de status HTTP e o
  corpo da resposta.
- As capturas dos testes em nuvem devem mostrar a URL pública do Azure App
  Service.
- As consultas ao banco devem exibir o comando executado e o resultado
  retornado.
- O nome do arquivo deve corresponder ao id do caso no plano de testes.

Status: estrutura preparada, aguardando o registro das capturas conforme a
execução. Os resultados consolidados ficam em `docs/relatorio-testes.md`.
