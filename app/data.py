#(resetea al reiniciar)
from typing import Dict
from .models import Product # pyright: ignore[reportMissingImports]

db: Dict[int, Product] = {}

db[1] = Product(id=1, name="Mouse", price=12.5, in_stock=True)
db[2] = Product(id=2, name="Teclado", price=25.0, in_stock=True)

def next_id() -> int:
    return (max(db.keys()) + 1) if db else 1
