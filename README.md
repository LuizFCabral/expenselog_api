# 💰 ExpenseLog API

Uma API robusta para gerenciamento de despesas, construída com **FastAPI**, **SQLAlchemy** (Async) e **PostgreSQL**.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Gerenciador de Pacotes:** [Poetry](https://python-poetry.org/)
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Banco de Dados:** PostgreSQL (via Docker)
* **Migrações:** Alembic
* **QA/Lint:** Ruff & Pytest

---

## 🚀 Como Configurar o Projeto

### 1. Pré-requisitos
Certifique-se de ter instalado:
* [Python 3.12+](https://www.python.org/)
* [Docker & Docker Compose](https://www.docker.com/)
* [Poetry](https://python-poetry.org/docs/#installation)

### 2. Instalando o Poetry (Caso não tenha)
O Poetry gerencia o ambiente virtual e as bibliotecas automaticamente.
* **Windows (PowerShell):**
    ```powershell
    (Invoke-WebRequest -Uri [https://install.python-poetry.org](https://install.python-poetry.org) -UseBasicParsing).Content | py -
    ```
* **Linux/macOS:**
    ```bash
    curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
    ```

### 3. Instalação das Dependências
Dentro da pasta do projeto, execute:
```bash
poetry install

```
Isso criará um ambiente virtual isolado com tudo o que o projeto precisa (FastAPI, Ruff, Pytest, etc).

---

## 🗄️ Banco de Dados e Migrações
Este projeto utiliza **PostgreSQL** rodando dentro de um container Docker para facilitar a configuração.

**Passo A: Subir o Banco de Dados**
Antes de rodar a API, você precisa iniciar o container do banco:

```bash
poetry run task run-compose-db
```

**Passo B: Rodar as Migrações (Alembic)**
Com o banco rodando, precisamos criar as tabelas. O Alembic cuida disso:

```bash
poetry run alembic upgrade head
```

---

## 💻 Comandos Úteis (Taskipy)
Para facilitar o dia a dia, configuramos atalhos (tasks). Use sempre ``poetry run task <comando>``:
Comando | Descrição
-|-
``run``| Inicia a API FastAPI em modo de desenvolvimento
``run-compose`` | Sobe todos os serviços (App + DB) via Docker
``run-compose-db`` | Sobe apenas o banco de dados no Docker
``format`` | Formata o código automaticamente seguindo o padrão Ruff
``lint`` | Verifica se existem erros ou más práticas no código
``test`` | Executa os testes automatizados com cobertura de código

---

## 🧪 Testes e Qualidade
Para garantir que tudo está funcionando e o código está limpo:

1. **Rodar Testes:** poetry run task test (Gera um relatório HTML na pasta ``htmlcov``)

2. **Formatar Código:** ``poetry run task format``

---

## 🛣️ Endpoints Principais (Swagger)
Com a aplicação rodando (``task run``), você pode acessar a documentação interativa em:

* **Swagger UI**: http://127.0.0.1:8000/docs 


