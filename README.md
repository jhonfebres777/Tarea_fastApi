# Nombre del Proyecto



## Requisitos

- Python 3.14.4
- MongoDB 4.0+

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python3 -m venv env`
3. Activarlo: `source env/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`

## Ejecución

uvicorn app:app --reload

Optimizing tool selection...

### Guía de Aprendizaje Estructurada: Proyecto CRUD con FastAPI, MongoDB, Postman y Bitbucket

 desarrollador junior full-stack, esta guía te ayudará a entender el ecosistema del proyecto paso a paso. Se enfoca en la arquitectura de FastAPI, patrones de Python, manejo de MongoDB, herramientas como Postman y Bitbucket, y flujos de trabajo. El proyecto es un CRUD básico para productos, usando FastAPI (framework asíncrono para APIs REST), MongoDB (base de datos NoSQL), y estructura modular.

#### 1. **Introducción a FastAPI y Arquitectura de Python**
   - **FastAPI**: Framework moderno para APIs REST en Python. Usa ASGI (asíncrono), Pydantic para validación de datos, y genera documentación automática (Swagger/OpenAPI). Es rápido, con tipado fuerte y soporte para dependencias.
   - **Arquitectura del Proyecto**: Sigue el patrón **MVC-like** (Model-View-Controller) adaptado a APIs:
     - **Routers**: Manejan rutas/endpoints (controladores).
     - **Services**: Lógica de negocio (modelos y operaciones).
     - **Config**: Configuraciones (e.g., base de datos).
     - **Main App**: Punto de entrada, configura middleware y rutas.
   - **Patrones Usados**:
     - **Separación de Concerns**: Cada carpeta tiene una responsabilidad (e.g., routers para APIs, Internal para lógica).
     - **Dependency Injection**: FastAPI inyecta dependencias automáticamente.
     - **Async/Await**: Para operaciones no bloqueantes (e.g., DB queries).
   - **Ecosistema Python**: Usa `uvicorn` (servidor ASGI), `pymongo` (driver MongoDB), `motor` (async MongoDB). Instala con `pip install -r requirements.txt`.

#### 2. **Estructura del Proyecto y Conexiones entre Carpetas**
   - **Raíz**:
     - main.py (o `app.py`): Archivo principal. Crea la app FastAPI, configura CORS (para frontends), incluye routers, y maneja eventos de startup/shutdown.
     - requirements.txt: Lista de dependencias (e.g., `fastapi`, `motor` para MongoDB async).
     - README.md: Documentación básica (instalación, ejecución).
   - **Config/**: Configuraciones globales.
     - database.py: Conexión a MongoDB. Usa variables de entorno (.env) para URI y DB name. Crea cliente y función para obtener colecciones.
   - **Internal/**: Lógica de negocio (services).
     - productsService.py: Funciones CRUD para productos. Conecta a colección "products" via database.py.
   - **routers/**: Endpoints de API.
     - products.py: Define rutas (GET, POST, PUT, DELETE). Usa productsService.py para operaciones y Pydantic para validación.
   - **Flujos de Conexión**:
     - main.py → Incluye products.py → Llama a productsService.py → Usa database.py para DB.
     - Datos fluyen: Request → Router (valida con Pydantic) → Service (opera DB) → Response.

#### 3. **Explicación Detallada del Código**
   - **main.py** (Punto de Entrada):
     - **Variables/Clases**:
       - `app`: Instancia FastAPI (título, versión, descripción).
       - `origins`: Lista de URLs permitidas para CORS (evita errores de origen cruzado en frontends).
       - `client`: Cliente MongoDB de database.py.
     - **Funciones**:
       - `health_check()`: Endpoint GET `/health` para verificar si la app funciona.
       - `startup_event()`: Al iniciar, verifica conexión a MongoDB (ping).
       - `shutdown_event()`: Al cerrar, desconecta MongoDB.
     - **Propósito**: Configura la app, maneja CORS, incluye routers, y asegura DB conectada.

   - **database.py** (Configuración DB):
     - **Variables**:
       - `MONGODB_URI`: URL de conexión (de .env, default localhost).
       - `DB_NAME`: Nombre de la DB (de .env, default "miapi").
       - `client`: Cliente pymongo (conecta automáticamente).
       - `database`: Referencia a la DB.
     - **Funciones**:
       - `get_collection(collection_name)`: Retorna una colección específica (e.g., "products").
     - **Propósito**: Centraliza configuración DB. Usa dotenv para seguridad (no hardcodear credenciales).

   - **productsService.py** (Lógica de Negocio):
     - **Variables**:
       - `collection`: Referencia a colección "products" via `get_collection`.
     - **Funciones** (CRUD):
       - `get_all_products()`: Busca todos los documentos, convierte `_id` (ObjectId) a string para JSON.
       - `get_product_by_id(product_id)`: Busca por ID, maneja errores.
       - `create_product(product_data)`: Inserta nuevo documento, retorna con ID.
       - `update_product(product_id, update_data)`: Actualiza documento, verifica si existe.
       - `delete_product(product_id)`: Elimina por ID, retorna éxito.
     - **Propósito**: Abstrae operaciones DB. Maneja conversión ObjectId (MongoDB usa ObjectId, APIs usan strings).

   - **products.py** (Endpoints API):
     - **Clases (Pydantic Models)**:
       - `ProductBase`: Campos base (name, price, description, category). Usa Field para validación (e.g., price > 0).
       - `ProductCreate`: Hereda de ProductBase (para POST).
       - `ProductResponse`: Agrega `id` (alias `_id`), configura para JSON.
     - **Funciones (Endpoints)**:
       - `get_products()`: GET `/` - Lista todos los productos.
       - `get_product(product_id)`: GET `/{id}` - Obtiene uno, lanza 404 si no existe.
       - `create_multiple_product(products)`: POST `/` - Crea múltiples productos (lista).
       - `update_product(product_id, product)`: PUT `/{id}` - Actualiza uno.
       - `delete_product(product_id)`: DELETE `/{id}` - Elimina uno.
     - **Propósito**: Define rutas, valida inputs con Pydantic, llama a services, maneja errores HTTP.

#### 4. **Manejo de MongoDB**
   - **Conceptos**: NoSQL, documentos JSON-like. Usa colecciones (tablas) y documentos (registros).
   - **Integración**: `pymongo` para sync, `motor` para async. Conecta via URI (e.g., `mongodb://localhost:27017`).
   - **Operaciones**: CRUD básico. Maneja ObjectId (convierte a string para APIs).
   - **Mejores Prácticas**: Usa variables de entorno para credenciales. Verifica conexión en startup.

#### 5. **Postman para Testing APIs**
   - **Herramienta**: Cliente para probar APIs REST. Crea requests (GET, POST, etc.) y ve responses.
   - **Flujo**: 
     1. Ejecuta la app (`uvicorn app:app --reload`).
     2. En Postman, crea colección para endpoints (e.g., GET `http://localhost:8000/api/v1/products`).
     3. Envía requests, verifica status codes (200, 404), y datos JSON.
   - **Aprendizaje**: Usa para validar CRUD. Prueba errores (e.g., ID inválido).

