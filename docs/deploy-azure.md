# Implantação da API Biblioteca Comunitária no Microsoft Azure

## 1. Objetivo

Este documento apresenta as etapas realizadas para configurar e implantar a API do projeto **Biblioteca Comunitária — Cloud Challenge 06**, desenvolvido na disciplina de Cloud Computing da Faculdade Senac.

A implantação foi realizada utilizando o Microsoft Azure App Service, com o objetivo de disponibilizar a API Flask em um ambiente de nuvem acessível por meio de uma URL pública.

**Responsável:** Julliane Valentin  
**Papel:** NUVEM — Configuração e Implantação

## 2. Tecnologias utilizadas

- Microsoft Azure — plataforma de computação em nuvem.
- Azure App Service — hospedagem da aplicação.
- Python 3.12 — linguagem utilizada pela API.
- Flask — framework de desenvolvimento da API.
- Gunicorn — servidor utilizado para executar a aplicação.
- Visual Studio Code — ambiente de desenvolvimento e implantação.
- Git e GitHub — versionamento e colaboração.

## 3. Configuração do ambiente Azure

Foi utilizada a assinatura **Azure for Students** para preparar o ambiente de implantação.

As configurações realizadas foram:

| Recurso | Configuração |
|---|---|
| Grupo de recursos | `rg-cloud-gXX` |
| App Service | `app-biblioteca-cloud-jv` |
| Sistema operacional | Linux |
| Linguagem | Python 3.12 |
| Plano de hospedagem | Free F1 |
| Região | Chile Central |

O plano Free F1 foi escolhido para utilizar a camada gratuita do Azure App Service.

## 4. Configuração da inicialização

Para executar a API Flask no ambiente de produção, foi configurado o seguinte comando de inicialização:

```bash
gunicorn --bind=0.0.0.0:8000 app:app
```

O Gunicorn é responsável por iniciar a aplicação Flask e disponibilizá-la na porta configurada.

Também foi adicionada a variável de ambiente:

```env
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Essa configuração habilita a execução do processo de build durante a implantação, permitindo a instalação das dependências declaradas no arquivo `requirements.txt`.

## 5. Processo de implantação

A implantação foi realizada diretamente pelo Visual Studio Code, utilizando a extensão do Azure App Service.

Etapas executadas:

1. Autenticação na assinatura Azure for Students.
2. Criação e configuração do Azure App Service.
3. Configuração do ambiente Python e do comando de inicialização.
4. Configuração da variável de ambiente para o processo de build.
5. Seleção da pasta principal do projeto no Visual Studio Code.
6. Publicação da aplicação por meio da opção **Deploy to Web App**.
7. Confirmação de sucesso da implantação.
8. Acesso à URL pública para verificar a resposta da API.

Após o deploy, a aplicação respondeu à requisição HTTP na rota principal (`/`), retornando informações do projeto em formato JSON.

## 6. Validação da aplicação

A API foi acessada por meio do domínio público disponibilizado pelo Azure App Service.

**URL pública:** [inserir aqui o domínio completo fornecido pela Azure]

A rota principal (`/`) respondeu com as informações da Biblioteca Comunitária e do Cloud Challenge 06.

Esse teste confirmou que a aplicação foi publicada e estava respondendo no ambiente Azure.

Também foi acessado o **Fluxo de log (Log stream)** para inspecionar informações do ambiente de execução.

## 7. Integração com PostgreSQL

A aplicação possui um módulo de conexão com PostgreSQL, que utiliza a variável de ambiente `DATABASE_URL`.

A configuração dessa variável no Azure App Service ainda está pendente, pois o banco de dados está disponível apenas no ambiente local da equipe.

Para concluir a integração, será necessário disponibilizar um PostgreSQL acessível pela aplicação hospedada na Azure e configurar a variável de conexão de forma segura, sem expor credenciais no repositório.

Após essa etapa, deverá ser validada a rota:

```http
GET /health
```

O resultado esperado é uma resposta HTTP 200 indicando que a conexão com o banco foi estabelecida.

**Status atual:** implantação da API concluída; integração com PostgreSQL pendente.

## 8. Evidências da implantação

Foram registradas as seguintes evidências na pasta `evidencias/`:

| Arquivo | Descrição |
|---|---|
| `01-ambiente-azure.png` | Configuração e informações do App Service |
| `02-api-azure-funcionando.png` | Resposta da API pela URL pública |
| `03-configuracao-gunicorn-azure.png` | Configuração do comando de inicialização |
| `04-variaveis-ambiente-azure.png` | Variável de ambiente utilizada no processo de build |
| `05-logs-aplicacao-azure.png` | Fluxo de logs do Azure App Service |

As evidências documentam a configuração e a publicação inicial da API na nuvem.

## 9. Considerações finais

A implantação inicial da API Biblioteca Comunitária no Microsoft Azure foi realizada com sucesso, permitindo o acesso à aplicação por meio de uma URL pública.

O processo envolveu a preparação do ambiente, a configuração do servidor Gunicorn, o gerenciamento de variáveis de ambiente e a publicação pelo Visual Studio Code.

A principal etapa pendente é a integração com o PostgreSQL, necessária para validar a persistência dos dados e o funcionamento completo das rotas da aplicação.

Após a disponibilização do banco de dados, serão realizados os testes de conexão e a atualização das evidências de implantação.