from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .model import Product, ProductCreate, ProductUpdate
from .data import db, next_id

app = FastAPI(
    title=" REST API de Productos",
    version="1.0.0",
    description="API CRUD simple para  GitHub."
)

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["util"])
def health():
    return {"status": "ok"}



@app.get("/products", response_model=List[Product], tags=["products"])
def list_products():
    return list(db.values())

@app.get("/products/{product_id}", response_model=Product, tags=["products"])
def get_product(product_id: int):
    product = db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.post("/products", response_model=Product, status_code=201, tags=["products"])
def create_product(payload: ProductCreate):
    new_id = next_id()
    product = Product(id=new_id, **payload.model_dump())
    db[new_id] = product
    return product

@app.post("/products", response_model=Product, status_code=201, tags=["products"])
def create_product(payload: ProductCreate):
    new_id = next_id()
    product = Product(id=new_id, **payload.model_dump())
    db[new_id] = product
    return product
    
@app.put("/products/{product_id}", response_model=Product, tags=["products"])
def update_product(product_id: int, payload: ProductUpdate):
    existing = db.get(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
    db[product_id] = updated
    return updated

@app.delete("/products/{product_id}", status_code=204, tags=["products"])
def delete_product(product_id: int):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del db[product_id]
    return