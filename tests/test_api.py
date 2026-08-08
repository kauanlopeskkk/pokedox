def test_bem_vindo(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "mensagem" in resposta.json()


def test_endpoints_exigem_autenticacao(client):
    resposta = client.get("/pokemons")
    assert resposta.status_code == 401


def test_criar_e_buscar_pokemon(client, auth_headers):
    payload = {"nome": "Pikachu", "tipo": "Elétrico", "nivel": 5, "captura": 0.5}
    resposta_criacao = client.post("/pokemons", json=payload, headers=auth_headers)
    assert resposta_criacao.status_code == 201
    criado = resposta_criacao.json()
    assert criado["nome"] == "Pikachu"
    assert "id" in criado

    resposta_busca = client.get(f"/pokemons/{criado['id']}", headers=auth_headers)
    assert resposta_busca.status_code == 200
    assert resposta_busca.json()["nome"] == "Pikachu"


def test_criar_pokemon_duplicado_falha(client, auth_headers):
    payload = {"nome": "Charmander", "tipo": "Fogo", "nivel": 5, "captura": 0.4}
    client.post("/pokemons", json=payload, headers=auth_headers)
    resposta = client.post("/pokemons", json=payload, headers=auth_headers)
    assert resposta.status_code == 400


def test_buscar_pokemon_inexistente(client, auth_headers):
    resposta = client.get("/pokemons/9999", headers=auth_headers)
    assert resposta.status_code == 404


def test_listar_pokemons(client, auth_headers):
    client.post(
        "/pokemons",
        json={"nome": "Squirtle", "tipo": "Água", "nivel": 5, "captura": 0.4},
        headers=auth_headers,
    )
    resposta = client.get("/pokemons", headers=auth_headers)
    assert resposta.status_code == 200
    nomes = [p["nome"] for p in resposta.json()]
    assert "Squirtle" in nomes


def test_atualizar_pokemon(client, auth_headers):
    criado = client.post(
        "/pokemons",
        json={"nome": "Bulbasaur", "tipo": "Planta", "nivel": 5, "captura": 0.4},
        headers=auth_headers,
    ).json()

    resposta = client.put(
        f"/pokemons/{criado['id']}", json={"nivel": 10}, headers=auth_headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["nivel"] == 10
    assert resposta.json()["nome"] == "Bulbasaur"


def test_atualizar_pokemon_inexistente(client, auth_headers):
    resposta = client.put("/pokemons/9999", json={"nivel": 10}, headers=auth_headers)
    assert resposta.status_code == 404


def test_deletar_pokemon(client, auth_headers):
    criado = client.post(
        "/pokemons",
        json={"nome": "Eevee", "tipo": "Normal", "nivel": 5, "captura": 0.4},
        headers=auth_headers,
    ).json()

    resposta = client.delete(f"/pokemons/{criado['id']}", headers=auth_headers)
    assert resposta.status_code == 200

    resposta_busca = client.get(f"/pokemons/{criado['id']}", headers=auth_headers)
    assert resposta_busca.status_code == 404


def test_deletar_pokemon_inexistente(client, auth_headers):
    resposta = client.delete("/pokemons/9999", headers=auth_headers)
    assert resposta.status_code == 404
