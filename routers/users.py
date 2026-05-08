from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from Internal import usersService
from pydantic import EmailStr as emailStr


router = APIRouter()

# ---------------------------
# SCHEMAS (Modelos de Datos)
# ---------------------------

class userBase(BaseModel):
    username: str = Field(..., example="john_doe")
    email: emailStr = Field(..., example="john.doe@example.com")
    age: Optional[int] = Field(None, example=30)

class UserCreate(userBase):
    password: str = Field(..., min_length=8)

class Response(userBase):
    """Schema para respuesta, incluye el _id de MongoDB."""
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True  # Permitir usar alias
        json_schema_extra = {
            "example": {
                "_id": "60d5f9f8d4b0c8a1f0c8f3b2",
                "username": "John Doe",
                "email": "john.doe@example.com",
                "age": 30,

            }
        }

   
# ---------------------------
# ENDPOINTS
# ---------------------------


@router.get("/", response_model=list[Response], status_code=status.HTTP_200_OK)
def get_users():
    """Obtiene todos los users."""
    users = usersService.get_all_users()
    return users

@router.get("/{user_id}", response_model=Response, status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    """Obtiene un user por ID."""
    user = usersService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User no encontrado")
    return user

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Crea un nuevo user."""
    created_user = usersService.create_user(user.model_dump())

    return created_user 

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    """Elimina un user por ID."""
    user = usersService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User no encontrado")
    usersService.delete_user(user_id)
    return {"message": "User eliminado correctamente"}