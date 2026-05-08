# internal/usersService.py
from bson import ObjectId
from Config.database import get_collection

# Conectar a la colección "users"
collection = get_collection("users")
def get_all_users():
    """Retorna todos los usuarios de la colección."""
    users_cursor = collection.find()
    users_list = []
    for user in users_cursor:
        user["_id"] = str(user["_id"])  # Convertir ObjectId a string
        users_list.append(user)
    return users_list

def get_user_by_id(user_id: str):
    """Busca un usuario por su ID. Retorna None si no existe."""
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None
    except Exception:
        return None
    
def create_user(user_data: dict):
    """Inserta un usuario nuevo y retorna el documento con ID."""
    result = collection.insert_one(user_data)
    # Recuperar el documento creado
    new_user = collection.find_one({"_id": result.inserted_id})
    new_user["_id"] = str(new_user["_id"])
    return new_user



def update_user(user_id: str, update_data: dict):
    """Actualiza un usuario existente y retorna el documento actualizado."""
    try:
        object_id = ObjectId(user_id)
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
    

def delete_user(user_id: str):
    """Elimina un usuario por su ID. Retorna True si se eliminó."""
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception:
        return False