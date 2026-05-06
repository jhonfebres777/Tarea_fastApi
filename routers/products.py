# routers/products.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from Internal import productsService
from typing import List

router = APIRouter()

# ---------------------------
# SCHEMAS (Modelos de Datos)
# ---------------------------

class ProductBase(BaseModel):
    name: str = Field(..., example="Laptop Gamer")
    price: float = Field(..., gt=0, example=1299.99)
    description: Optional[str] = None
    category: str = Field(..., example="Electrónica")

class ProductCreate(ProductBase):
    """Schema para crear un producto (se usa en POST)."""
    pass

class ProductResponse(ProductBase):
    """Schema para respuesta, incluye el _id de MongoDB."""
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True  # Permitir usar alias
        json_schema_extra = {
            "example": {
                "_id": "60d5f9f8d4b0c8a1f0c8f3b2",
                "name": "Laptop Gamer",
                "price": 1299.99,
                "description": "Una laptop potente",
                "category": "Electrónica"
            }
        }

# ---------------------------
# ENDPOINTS
# ---------------------------

@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_products():
    """Obtiene todos los productos."""
    products = productsService.get_all_products()
    return products

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: str):
    """Obtiene un producto por ID."""
    product = productsService.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=List[ProductResponse], status_code=status.HTTP_201_CREATED)
def create_multiple_product(products: list[ProductCreate]):
    """Crea múltiples nuevos productos."""
    created_products = []
    
    for product in products:
        product_dict = product.model_dump()
        created = productsService.create_product(product_dict)
        created_products.append(created)
        
    return created_products

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: str, product: ProductCreate):
    """Actualiza un producto existente."""
    update_data = product.model_dump()
    updated = productsService.update_product(product_id, update_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    """Elimina un producto."""
    deleted = productsService.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None  # 204 No Content no debe retornar cuerpo