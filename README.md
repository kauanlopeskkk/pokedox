# Pokedox

API REST para gerenciamento de Pokémons, construída com **FastAPI** e **SQLAlchemy**, inspirada na PokéAPI. Projeto final do módulo de Python back-end.

## Stack

- **FastAPI** — framework web e documentação automática (Swagger/Redoc)
- **SQLAlchemy** — ORM para acesso ao banco relacional
- **SQLite** (padrão local) / **PostgreSQL** (via Docker)
- **pytest** + **httpx** — testes automatizados
- **Docker** / **docker-compose** — orquestração de containers

## Estrutura do projeto

```
app/
  main.py          # instância do FastAPI, middlewares e inclusão das rotas
  config.py        # leitura das variáveis de ambiente
  database.py       # engine, sessão e dependência get_db
  models.py          # modelo SQLAlchemy (Pokemon)
  schemas.py           # schemas Pydantic (entrada/saída)
  crud.py                # funções de acesso ao banco
  auth.py                 # autenticação HTTP Basic
  routers/pokemons.py      # endpoints de Pokémons
tests/
  conftest.py        # fixtures (client, banco de teste isolado, autenticação)
  test_api.py          # testes dos endpoints da API
  test_pokemon_utils.py  # testes das funções utilitárias em pokemon.py
pokemon.py            # funções utilitárias simples (cálculo de ataque, evolução)
Dockerfile
docker-compose.yml
.env.example
```

## Endpoints

Todos os endpoints de `/pokemons` exigem **HTTP Basic Auth** (usuário/senha definidos em `API_USERNAME`/`API_PASSWORD`).

| Método | Rota                | Descrição                          |
|--------|----------------------|-------------------------------------|
| GET    | `/`                   | Mensagem de boas-vindas             |
| POST   | `/pokemons`            | Cria um novo Pokémon                |
| GET    | `/pokemons`             | Lista os Pokémons (`skip`, `limit`) |
| GET    | `/pokemons/{id}`         | Busca um Pokémon pelo id            |
| PUT    | `/pokemons/{id}`          | Atualiza um Pokémon existente       |
| DELETE | `/pokemons/{id}`           | Remove um Pokémon                   |

A documentação interativa fica disponível em `/docs` (Swagger UI) e `/redoc`.

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário:

| Variável         | Descrição                                          | Padrão                     |
|------------------|-----------------------------------------------------|-----------------------------|
| `DATABASE_URL`   | URL de conexão do SQLAlchemy                         | `sqlite:///./pokemon.db`    |
| `API_USERNAME`   | Usuário do HTTP Basic Auth                            | `kauan`                     |
| `API_PASSWORD`   | Senha do HTTP Basic Auth                                | `admin`                     |
| `POSTGRES_USER`     | Usuário do Postgres (apenas docker-compose)             | `pokedox`                   |
| `POSTGRES_PASSWORD` | Senha do Postgres (apenas docker-compose)                 | `pokedox`                   |
| `POSTGRES_DB`        | Nome do banco Postgres (apenas docker-compose)               | `pokedox`                   |

## Rodando localmente

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`, usando SQLite por padrão.

## Rodando com Docker

```bash
docker-compose up --build
```

Sobe dois containers: `api` (FastAPI) e `db` (PostgreSQL), com a URL de conexão montada automaticamente a partir das variáveis `POSTGRES_*`.

## Testes

```bash
poetry run pytest -v
```

Os testes de API usam um banco SQLite isolado (`test_pokemon.db`, recriado a cada teste) e o `TestClient` do FastAPI, sem depender de um servidor rodando ou do Postgres.
