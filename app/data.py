
from typing import Dict
from .model import Product

db: Dict[int, Product] = {}

db[1] = Product(id=1, name="Mouse", price=12.5, in_stock=True, cantidad=100)
db[2] = Product(id=2, name="Teclado", price=25.0, in_stock=True, cantidad=150)

def next_id() -> int:
    return (max(db.keys()) + 1) if db else 1