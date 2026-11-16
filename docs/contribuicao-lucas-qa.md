# Contribuição - Lucas Querubim

**Papel:** QA - Qualidade e Documentação (issue #7)
**Branch:** `feature/lucas-qa-testes`

Lucas ficou responsável pelo planejamento dos testes e pela documentação da
qualidade do projeto. Elaborou o plano de testes em `docs/plano-de-testes.md`,
definindo escopo, estratégia, ambientes, critérios de aceite, critério de parada
e 33 casos de teste, incluindo os critérios de aceitação CA1 a CA5 do Desafio 06
e 18 casos negativos de validação de entrada, códigos de status HTTP e
disponibilidade do serviço.

Organizou a matriz de rastreabilidade entre os requisitos do desafio e os casos
de teste, garantindo que cada regra de negócio tivesse cobertura documentada.
Produziu o checklist de validação em `docs/checklist-validacao.md`, com
verificações agrupadas em dez áreas, do preparo do ambiente ao encerramento
formal do ciclo de testes.

Estruturou o relatório de execução em `docs/relatorio-testes.md`, com resultado
por caso, registro de defeitos e conclusão, e padronizou o registro das
evidências na pasta `evidencias/`, definindo a nomenclatura dos arquivos e o
conteúdo mínimo de cada captura.

Atualizou a documentação do repositório, incluindo a estrutura de pastas, a
tabela de rotas da API, a seção de qualidade e testes no `README.md` e as
instruções de reprodução dos cenários em `tests/README.md`, com os comandos de
requisição e as consultas SQL usadas na preparação dos dados.

Registrou como achados de QA a ausência da URL pública na documentação de
implantação, a divergência da constraint de prazo de 14 dias entre o schema
local e o banco hospedado na Render e as inconsistências nos nomes dos arquivos
de evidência citados em `docs/deploy-azure.md`.

## Entregáveis

| Arquivo | Descrição |
|---|---|
| `docs/plano-de-testes.md` | Plano de testes com 33 casos e resultados esperados |
| `docs/checklist-validacao.md` | Checklist de validação em 10 áreas |
| `docs/relatorio-testes.md` | Modelo de relatório de execução e defeitos |
| `tests/README.md` | Instruções de reprodução dos testes |
| `evidencias/README.md` | Estrutura e nomenclatura das evidências |
| `README.md` | Organização da documentação do projeto |
