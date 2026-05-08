
from Internal import usersService

# NOTA: Ya no importamos TestClient, app ni client. 
# Pytest los inyecta automáticamente desde conftest.py

def test_users_router_registered(client_test):
    """Verifica que el router de usuarios esté cargado"""
    registered_paths = [route.path for route in client_test.app.routes if hasattr(route, "path")]
    assert "/api/v1/users/" in registered_paths

def test_user_full_lifecycle(client_test, db_available):
    """
    Ciclo completo: POST -> GET -> DELETE
    (Puedes añadir el PUT aquí si decides implementarlo)
    """
    
    # 1. PREPARAR
    new_user = {
        "username": "test_user_refactor",
        "email": "refactor@example.com",
        "password": "strongpassword123",
        "age": 28,
    }

    # 2. CREAR (POST)
    # Nota: Aquí enviamos el objeto directo, ya que tu router de users 
    # probablemente no recibe una lista como el de products.
    create_res = client_test.post("/api/v1/users/", json=new_user)
    assert create_res.status_code == 201
    user_id = create_res.json()["_id"]

    # 3. LEER (GET by ID)
    get_res = client_test.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["_id"] == user_id

    # 4. ELIMINAR (DELETE)
    del_res = client_test.delete(f"/api/v1/users/{user_id}")
    assert del_res.status_code == 204

    # 5. VERIFICAR
    assert usersService.get_user_by_id(user_id) is None