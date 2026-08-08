import base64
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_pokemon.db"
os.environ.setdefault("API_USERNAME", "kauan")
os.environ.setdefault("API_PASSWORD", "admin")

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    token = base64.b64encode(
        f"{os.environ['API_USERNAME']}:{os.environ['API_PASSWORD']}".encode()
    ).decode()
    return {"Authorization": f"Basic {token}"}
