
const API_URL = "http://127.0.0.1:8000/products";

// Cargar productos
async function loadProducts() {
    const res = await fetch(API_URL);
    const products = await res.json();
    const container = document.getElementById("product-list");
    container.innerHTML = "";
    products.forEach(p => {
        container.innerHTML += `
            <div class="col-md-4">
                <div class="product-card">
                    <h6>${p.name}</h6>
                    <p>Precio: $${p.price}</p>
                    <p>${p.in_stock ? "Disponible" : "Agotado"}</p>
                </div>
            </div>
        `;
    });
}

// Agregar producto
async function addProduct() {
    const name = document.getElementById("name").value;
    const price = parseFloat(document.getElementById("price").value);
    const in_stock = document.getElementById("in_stock").checked;

    if (!name || isNaN(price)) {
        alert("Por favor, completa todos los campos correctamente.");
        return;
    }

    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price, in_stock })
    });

    if (res.ok) {
        alert("Producto agregado correctamente.");
        document.getElementById("name").value = "";
        document.getElementById("price").value = "";
        document.getElementById("in_stock").checked = true;
        loadProducts();
    } else {
        alert("Error al agregar producto.");
    }
}

// Inicializar
loadProducts();
