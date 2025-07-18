def test_create_account(client):
    response = client.post("/api/v1/accounts/", json={
        "name": "Alejandro",
        "balance": 100
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data

def test_create_account_missing_fields(client):
    response = client.post("/api/v1/accounts/", json={})
    assert response.status_code == 422

def test_get_account(client):
    # Primero creamos una cuenta
    response = client.post("/api/v1/accounts/", json={
        "name": "Carlos",
        "balance": 200
    })
    account_id = response.json()["id"]

    # Ahora, recuperamos la cuenta
    response = client.get(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == account_id
    assert data["name"] == "Carlos"
    assert data["balance"] == 200

def test_get_account_not_found(client):
    response = client.get("/api/v1/accounts/99999")
    assert response.status_code == 404

def test_update_account_balance(client):
    # Primero creamos una cuenta
    response = client.post("/api/v1/accounts/", json={
        "name": "Laura",
        "balance": 300
    })
    account_id = response.json()["id"]

    # Actualizamos el balance con un valor positivo
    response = client.patch(f"/api/v1/accounts/{account_id}", json={
        "amount": 350
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laura"
    assert data["balance"] == 650

    # Actualizamos el balance con un valor negativo
    response = client.patch(f"/api/v1/accounts/{account_id}", json={
        "amount": -1000
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laura"
    assert data["balance"] == -350

def test_delete_account(client):
    # Primero creamos una cuenta
    response = client.post("/api/v1/accounts/", json={
        "name": "Miguel",
        "balance": 400
    })
    account_id = response.json()["id"]

    # Eliminar la cuenta
    response = client.delete(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 204

    # Intentar obtener la cuenta eliminada
    response = client.get(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 404

def test_list_accounts(client):
    # Primero creamos dos cuentas
    client.post("/api/v1/accounts/", json={"name": "A", "balance": 10})
    client.post("/api/v1/accounts/", json={"name": "B", "balance": 20})

    response = client.get("/api/v1/accounts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2