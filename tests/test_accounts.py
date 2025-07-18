def test_create_account(client):
    response = client.post("/api/v1/accounts/", json={
        "name": "Alejandro",
        "balance": 100
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data