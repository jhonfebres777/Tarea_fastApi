# internal/productsService.py
from bson import ObjectId
from Config.database import get_collection

# Conectar a la colección "products"
collection = get_collection("products")

def get_all_products():
    """Retorna todos los productos de la colección."""
    products_cursor = collection.find()
    products_list = []
    for product in products_cursor:
        product["_id"] = str(product["_id"])  # Convertir ObjectId a string
        products_list.append(product)
    return products_list

def get_product_by_id(product_id: str):
    """Busca un producto por su ID. Retorna None si no existe."""
    try:
        product = collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
            return product
        return None
    except Exception:
        return None

def create_product(product_data: dict):
    """Inserta un producto nuevo y retorna el documento con ID."""
    result = collection.insert_one(product_data)
    # Recuperar el documento creado
    new_product = collection.find_one({"_id": result.inserted_id})
    new_product["_id"] = str(new_product["_id"])
    return new_product

def update_product(product_id: str, update_data: dict):
    """Actualiza un producto existente y retorna el documento actualizado."""
    try:
        object_id = ObjectId(product_id)
        # Asegurarse de no actualizar el _id
        if "_id" in update_data:
            del update_data["_id"]
            
        result = collection.update_one({"_id": object_id}, {"$set": update_data})
        
        # Corrección: verificamos si se encontró el documento (matched_count)
        if result.matched_count > 0:
            updated = collection.find_one({"_id": object_id})
            updated["_id"] = str(updated["_id"])
            return updated
        return None
    except Exception:
        return None

def delete_product(product_id: str):
    """Elimina un producto por su ID. Retorna True si se eliminó."""
    try:
        result = collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
    except Exception:
        return False