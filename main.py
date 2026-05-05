from fastapi import FastAPI
from pydantic import BaseModel

#para iniciar el servidor 
#  se ejecuta el siguente comando en la terminal: uvicorn main:app --reload 
# en caso de que sea otro numbre de archivo se cambia main por el
#  nombre del archivo sin la extension .py   


# Definimos un modelo de datos para el usuario utilizando Pydantic
# Esto nos permite validar y documentar automáticamente los datos de entrada
#asi definie los modelos de datos que se esperan recibir en las solicitudes HTTP, 
# lo que facilita la validación y el manejo de errores.
#definiendo los campos con su respectoivo tipo de dato, 
# esto nos permite asegurarnos de que los datos recibidos sean del tipo correcto 
# y cumplan con las restricciones definidas.

class User(BaseModel):
    id: int
    name: str
    surnemame: str
    age: int
    email: str

app = FastAPI()
 

 # Creamos una lista para almacenar los usuarios en memoria
 #

users_list = [
    User(id=1, name="John", surnemame="Doe", age=30, email="john.doe@example.com"),
    User(id=2, name="Jane", surnemame="Smith", age=25, email="jane.smith@example.com"),
    User(id=3, name="Alice", surnemame="Johnson", age=28, email="alice@example.com"),] 


@app.post("/users")
async def create_user(user: User):
    users_list.append(user)
    return users_list

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users_list:
        if user.id == user_id:
            return list(user)
    return {"error": "User not found"}
