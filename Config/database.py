# config/database.py
# config/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URI de conexión y el nombre de la BD desde las variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "miapi")

# Crear el cliente de MongoDB (se conecta automáticamente al ser usado)
client = MongoClient(MONGODB_URI)

# Seleccionar la base de datos
database = client[DB_NAME]

# Función auxiliar para obtener una colección específica
def get_collection(collection_name: str):
    """Retorna una colección de la base de datos."""
    return database[collection_name]