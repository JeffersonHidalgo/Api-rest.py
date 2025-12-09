from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: int = Field(..., description="Identificador único del producto")
    name: str = Field(..., min_length=2, description="Nombre del producto")
    price: float = Field(..., ge=0, description="Precio del producto")
    in_stock: bool = Field(default=True, description="Disponibilidad")

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., ge=0)
    in_stock: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[bool] = None