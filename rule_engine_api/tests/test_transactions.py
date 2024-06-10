from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_check_transaction_approved():
    """
    Test the check_transaction endpoint with an approved transaction.
    """
    transaction_data = {
        "transaction_id": "123",
        "transaction_amount": "100",
        "merchant_id": "456",
        "client_id": "789",
        "phone_number": "1234567890",
        "ip_address": "127.0.0.1",
        "email_address": "test@example.ci",
        "amount": 100,
    }

    response = client.post("/v0/check-transaction", json=transaction_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "approved",
        "status_code": 200,
        "message": "Transaction approved",
    }


def test_check_transaction_rejected():
    """
    Test the check_transaction endpoint with a rejected transaction.
    """
    transaction_data = {
        "transaction_id": "123",
        "transaction_amount": "1500001",
        "merchant_id": "456",
        "client_id": "789",
        "phone_number": "1234567890",
        "ip_address": "127.0.0.1",
        "email_address": "test@example.com",
        "amount": 1500001,
    }

    response = client.post("/v0/check-transaction", json=transaction_data)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json["status"] == "rejected"
    assert response_json["statustatus_codes"] == 400
