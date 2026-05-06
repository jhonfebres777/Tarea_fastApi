# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Config.database import client
from routers import products  # Importaremos el router que crearemos luego 


# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Mi API",
    description="API de ejemplo con FastAPI y MongoDB",
    version="0.1.0"
)

# Configurar CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:3000",  # Permitir frontend en React (ejemplo)
    "http://localhost:5173",  # Permitir frontend en Vite/Svelte (ejemplo)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de los routers
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])

# Endpoint de salud ("health check")
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "El servicio está funcionando correctamente"}

# Manejo de eventos (startup y shutdown) - Bueno para conexiones
@app.on_event("startup")
async def startup_event():
    # Verificar conexión a la BD al iniciar
    try:
        client.admin.command('ping')
        print("¡Conectado a MongoDB exitosamente!")
    except Exception as e:
        print(f"Error al conectar a MongoDB:{e}")

@app.on_event("shutdown")
async def shutdown_event():
    client.close()
    print("Conexión a MongoDB cerrada.")