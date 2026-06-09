from fastapi import FastAPI, HTTPException, Response, status
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

app = FastAPI(
    title="Sistema de Inventario",
    description="API para administrar productos de una tienda",
    version="1.1.0"
)

inventory: list[dict] = []
current_id = 1

@app.get(
    "/products",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK
)
def obtener_productos(min_stock: int = 0):
    return [item for item in inventory if item["stock"] >= min_stock]


@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK
)
def buscar_producto(product_id: int):
    for item in inventory:
        if item["id"] == product_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No existe un producto con ese ID"
    )


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_producto(payload: ProductCreate):
    global current_id

    nuevo_producto = {
        "id": current_id,
        "name": payload.name,
        "category": payload.category,
        "price": payload.price,
        "stock": payload.stock
    }

    inventory.append(nuevo_producto)
    current_id += 1

    return nuevo_producto


@app.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK
)
def actualizar_producto(product_id: int, payload: ProductUpdate):
    for item in inventory:
        if item["id"] == product_id:
            item["name"] = payload.name
            item["category"] = payload.category
            item["price"] = payload.price
            item["stock"] = payload.stock

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_producto(product_id: int):
    for index, item in enumerate(inventory):
        if item["id"] == product_id:
            del inventory[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado"
    )