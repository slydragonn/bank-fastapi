import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_database
import os

@pytest.fixture(scope="module", autouse=True)
def set_test_env():
    os.environ["TESTING"] = "1"


@pytest.fixture(autouse=True)
def clear_accounts():
    db = get_database()
    collection = db["accounts"]
    collection.delete_many({})  # Clear accounts before each test
    

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c