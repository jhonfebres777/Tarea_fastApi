
from Internal import productsService

# NOTA: No definas client_test aquí, deja que Pytest lo inyecte desde conftest.py

def test_products_router_registered(client_test):
    """Verifica que el router esté cargado en la app"""
    registered_paths = [route.path for route in client_test.app.routes if hasattr(route, "path")]
    assert "/api/v1/products/" in registered_paths

def test_product_full_lifecycle(client_test, db_available):
    """
    Ciclo completo: POST -> GET -> PUT -> DELETE
    """
    
    # 1. PREPARAR (Datos de prueba)
    new_products = [{
        "name": "Laptop Pro 14",
        "price": 1500.0,
        "description": "Chip M1",
        "category": "Computadoras"
    }]

    # 2. CREAR (POST) - Enviamos lista porque tu router la requiere
    create_res = client_test.post("/api/v1/products/", json=new_products)
    assert create_res.status_code == 201
    product_id = create_res.json()[0]["_id"]

    # 3. LEER (GET by ID)
    get_res = client_test.get(f"/api/v1/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["_id"] == product_id

    # 4. ACTUALIZAR (PUT)
    update_data = {
        "name": "Laptop Pro 14",
        "price": 1450.0,
        "description": "Chip M1 - Oferta",
        "category": "Computadoras"
    }
    put_res = client_test.put(f"/api/v1/products/{product_id}", json=update_data)
    assert put_res.status_code == 200
    assert put_res.json()["price"] == 1450.0

    # 5. ELIMINAR (DELETE)
    del_res = client_test.delete(f"/api/v1/products/{product_id}")
    assert del_res.status_code == 204

    # 6. VERIFICAR (Inexistencia final en el Service)
    assert productsService.get_product_by_id(product_id) is None