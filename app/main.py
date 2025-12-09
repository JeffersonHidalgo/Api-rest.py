
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from sqlmodel import select # pyright: ignore[reportMissingImports]
from .db import init_db, get_session # pyright: ignore[reportMissingImports]
from .model import Product

app = FastAPI(title="Products API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products", response_model=List[Product])
def list_products(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    name: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    in_stock: Optional[bool] = None,
):
    with get_session() as session:
        stmt = select(Product)
        if name:
            stmt = stmt.where(Product.name.contains(name))
        if price_min is not None:
            stmt = stmt.where(Product.price >= price_min)
        if price_max is not None:
            stmt = stmt.where(Product.price <= price_max)
        if in_stock is not None:
            stmt = stmt.where(Product.in_stock == in_stock)
        return session.exec(stmt.offset(offset).limit(limit)).all()

@app.get("/products/{id}", response_model=Product)
def get_product(id: int):
    with get_session() as session:
        p = session.get(Product, id)
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")
        return p

@app.post("/products", response_model=Product, status_code=201)
def create_product(body: Product):
    with get_session() as session:
        session.add(body)
        session.commit()
        session.refresh(body)
        return body

@app.put("/products/{id}", response_model=Product)
def update_product(id: int, patch: Product):
    with get_session() as session:
        p = session.get(Product, id)
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")
        for field in ["name", "price", "in_stock"]:
            val = getattr(patch, field, None)
            if val is not None:
                setattr(p, field, val)
        session.add(p)
        session.commit()
        session.refresh(p)
        return p

@app.delete("/products/{id}", status_code=204)
def delete_product(id: int):
    with get_session() as session:
        p = session.get(Product, id)
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(p)
        session.commit()
        return
