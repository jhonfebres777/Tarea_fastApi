import pytest
from fastapi.testclient import TestClient
from main import app
from Config.database import client

# Esta fixture ahora estará disponible para TODOS tus archivos de test automáticamente
@pytest.fixture(scope="session") # 'session' para que solo se conecte una vez al iniciar todo
def db_available():
    try:
        client.admin.command("ping")
    except Exception as exc:
        pytest.skip(f"MongoDB no disponible: {exc}")
    yield

@pytest.fixture(scope="session")
def client_test():
    return TestClient(app)