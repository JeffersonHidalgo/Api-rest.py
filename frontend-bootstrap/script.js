
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
                    <button class="btn btn-danger btn-sm delete-btn" onclick="deleteProduct(${p.id})">Eliminar</button>
                    <h6>${p.name}</h6>
                    <p>ID: ${p.id}</p>
                    <p>Precio: $${p.price}</p>
                    <p>${p.in_stock ? "Disponible" : "Agotado"}</p>
                </div>
            </div>
        `;
    });
}

// Agregar producto y mostrar ID
async function addProduct() {
    const name = document.getElementById("name").value;
    const price = parseFloat(document.getElementById("price").value);
    const in_stock = document.getElementById("in_stock").checked;

    if (!name || isNaN(price)) {
        Swal.fire("Error", "Por favor, completa todos los campos correctamente.", "error");
        return;
    }

    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price, in_stock })
    });

    if (res.ok) {
        const data = await res.json();
        Swal.fire("Éxito", `Producto agregado con ID: ${data.id}`, "success");
        document.getElementById("name").value = "";
        document.getElementById("price").value = "";
        document.getElementById("in_stock").checked = true;
        loadProducts();
    } else {
        Swal.fire("Error", "No se pudo agregar el producto.", "error");
    }
}

// Eliminar producto con SweetAlert2
async function deleteProduct(id) {
    Swal.fire({
        title: "¿Eliminar producto?",
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then(async (result) => {
        if (result.isConfirmed) {
            const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
            if (res.status === 204) {
                Swal.fire("Eliminado", "Producto eliminado correctamente.", "success");
                loadProducts();
            } else {
                Swal.fire("Error", "No se pudo eliminar el producto.", "error");
            }
        }
    });
}

// Inicializar
loadProducts();
