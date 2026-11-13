# Implantação da API Biblioteca Comunitária no Microsoft Azure

## 1. Objetivo

Este documento apresenta as etapas realizadas para configurar, implantar e validar a API do projeto **Biblioteca Comunitária — Cloud Challenge 06**, desenvolvido na disciplina de Cloud Computing da Faculdade Senac.

A implantação foi realizada utilizando o Microsoft Azure App Service, com o objetivo de disponibilizar a API Flask em um ambiente de nuvem acessível por meio de uma URL pública.

Também foi realizada a integração com um banco de dados PostgreSQL hospedado na plataforma Render, permitindo a comunicação entre a aplicação e o banco de dados em ambientes de nuvem.

**Responsável:** Julliane Valentin  
**Papel:** NUVEM — Configuração, Implantação e Integração

## 2. Tecnologias utilizadas

- **Microsoft Azure:** plataforma de computação em nuvem.
- **Azure App Service:** serviço utilizado para hospedar a API.
- **Azure for Students:** assinatura utilizada para configurar o ambiente.
- **Python 3.12:** linguagem de programação utilizada pela aplicação.
- **Flask:** framework utilizado no desenvolvimento da API.
- **Gunicorn:** servidor responsável pela execução da aplicação Flask.
- **PostgreSQL:** sistema gerenciador de banco de dados relacional.
- **Render:** plataforma utilizada para hospedar o banco PostgreSQL.
- **Visual Studio Code:** ambiente utilizado para desenvolvimento e implantação.
- **Git e GitHub:** ferramentas de versionamento e colaboração.

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
| Framework da aplicação | Flask |
| Servidor de aplicação | Gunicorn |

O plano Free F1 foi escolhido para utilizar a camada gratuita do Azure App Service.

A aplicação foi configurada para ser executada em um ambiente Linux, utilizando Python 3.12.

## 4. Configuração da inicialização

Para executar a API Flask no ambiente Azure, foi configurado o seguinte comando de inicialização:

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

### Etapas executadas

1. Autenticação na assinatura Azure for Students.
2. Criação e configuração do Azure App Service.
3. Seleção do ambiente Linux com Python 3.12.
4. Configuração do comando de inicialização utilizando Gunicorn.
5. Configuração da variável de ambiente para o processo de build.
6. Seleção da pasta principal do projeto no Visual Studio Code.
7. Publicação da aplicação por meio da opção **Deploy to Web App**.
8. Confirmação de sucesso da implantação.
9. Acesso à URL pública para verificar a resposta da API.

Após o deploy, a aplicação respondeu à requisição HTTP na rota principal (`/`), retornando informações do projeto em formato JSON.

Isso confirmou que a API Flask estava publicada e acessível no ambiente Azure.

## 6. Validação da aplicação

A API foi acessada por meio do domínio público disponibilizado pelo Azure App Service.

**URL pública:** [INSERIR AQUI A URL PÚBLICA DA APLICAÇÃO]

### 6.1 Teste da rota principal

Foi realizada uma requisição HTTP para a rota:

```http
GET /
```

A aplicação respondeu com informações da Biblioteca Comunitária e do Cloud Challenge 06 em formato JSON.

Esse teste confirmou que a aplicação estava publicada e respondendo no ambiente Azure.

### 6.2 Verificação dos logs

Também foi utilizado o recurso **Log stream (Fluxo de log)** do Azure App Service para acompanhar informações do ambiente de execução.

A verificação permitiu observar a conexão com o fluxo de logs e informações relacionadas à execução da aplicação.

## 7. Integração com PostgreSQL

A API Biblioteca Comunitária foi integrada a um banco de dados PostgreSQL hospedado na plataforma Render.

O banco de dados foi disponibilizado pela integrante responsável pela infraestrutura de dados, enquanto a configuração da conexão com a aplicação foi realizada no Microsoft Azure App Service.

### 7.1 Configuração da conexão

Para estabelecer a comunicação entre a API Flask e o PostgreSQL, foi configurada a variável de ambiente `DATABASE_URL` diretamente nas configurações do Azure App Service.

Essa variável contém as informações necessárias para a conexão com o banco de dados, incluindo:

- Endereço do servidor PostgreSQL.
- Nome do banco de dados.
- Usuário de acesso.
- Senha de autenticação.

Por questões de segurança, o valor completo da variável não foi incluído no código-fonte nem na documentação pública do projeto.

A utilização de variáveis de ambiente permite separar as credenciais de acesso das configurações presentes no código da aplicação.

### 7.2 Arquitetura da integração

A arquitetura utilizada consiste em dois serviços hospedados em plataformas de nuvem diferentes:

**Microsoft Azure App Service**
- Hospedagem da API Flask.
- Execução da aplicação utilizando Gunicorn.
- Configuração da variável `DATABASE_URL`.
- Disponibilização dos endpoints por meio de uma URL pública.

**Render — PostgreSQL**
- Hospedagem do banco de dados relacional.
- Disponibilização de um endereço de conexão para a aplicação.
- Gerenciamento do serviço de banco de dados utilizado pela equipe.

A comunicação entre os serviços ocorre por meio da conexão PostgreSQL configurada na aplicação.

### 7.3 Teste de conectividade

Após configurar e salvar a variável `DATABASE_URL` no Azure App Service, foi realizado um teste utilizando a rota:

```http
GET /health
```

A requisição foi executada diretamente pelo navegador, utilizando o endereço público da aplicação hospedada na Azure.

A API retornou a seguinte resposta:

```json
{
  "banco": "conectado",
  "iniciado_em": "2026-11-13T17:26:02.236207+00:00",
  "status": "ok"
}
```

O resultado confirmou que a API Flask hospedada no Microsoft Azure conseguiu estabelecer conexão com o PostgreSQL hospedado na Render.

O campo `"banco": "conectado"` indica que a verificação de conectividade foi realizada com sucesso.

O campo `"status": "ok"` indica o resultado positivo da verificação de saúde da aplicação.

### 7.4 Resultado da integração

**Status: conexão com o PostgreSQL concluída e validada em 13/11/2026.**

A integração entre o Azure App Service e o banco de dados PostgreSQL da Render foi confirmada por meio da rota `/health`.

Esse teste comprova a conectividade entre a API e o banco de dados, mas não substitui os testes funcionais das operações de cadastro, consulta, empréstimo e devolução de livros.

A validação dessas funcionalidades e da persistência dos dados será realizada separadamente pela equipe.

## 8. Evidências da implantação

Foram registradas as seguintes evidências na pasta `evidencias/`:

| Arquivo | Descrição |
|---|---|
| `01-AmbienteAzure.png.png` | Configuração e informações do Azure App Service |
| `02-API-Azure-Funcionando.png.png` | Resposta da API pela URL pública |
| `03-configuracao-gunicorn-azure.png.png` | Configuração do comando de inicialização |
| `04-variaveis-ambiente-azure.png.png` | Variável de ambiente utilizada no processo de build |
| `05-logs-aplicacao-azure.png.png` | Fluxo de logs do Azure App Service |
| `06-health-banco-conectado.png` | Teste da rota `/health` confirmando a conexão entre a API na Azure e o PostgreSQL na Render |

As evidências documentam a configuração do ambiente, a implantação da API e a validação da conectividade com o banco de dados.

Os registros foram organizados para facilitar a avaliação da infraestrutura de nuvem utilizada no projeto.

## 9. Considerações finais

A implantação da API Biblioteca Comunitária no Microsoft Azure foi realizada com sucesso, permitindo o acesso à aplicação por meio de uma URL pública.

O processo envolveu a preparação do ambiente, a configuração do Azure App Service, a utilização do servidor Gunicorn, o gerenciamento de variáveis de ambiente e a publicação da API Flask pelo Visual Studio Code.

Também foi concluída a integração com o banco de dados PostgreSQL hospedado na Render.

A conectividade foi validada por meio da rota `/health`, que retornou o status `ok` e confirmou a comunicação entre a aplicação hospedada na Azure e o banco de dados.

Com isso, a infraestrutura de nuvem da aplicação encontra-se configurada e com a conectividade validada.

Os testes funcionais das operações da biblioteca e a comprovação da persistência dos dados serão documentados conforme a conclusão das atividades da equipe.

A experiência permitiu aplicar conceitos de computação em nuvem, implantação de aplicações, configuração de serviços, integração entre plataformas e gerenciamento de variáveis de ambiente em um projeto prático.