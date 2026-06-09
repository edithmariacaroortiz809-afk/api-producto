from fastapi import FastAPI, HTTPException, Response, status
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

app = FastAPI(title="API de productos", description ="Una API para gestionar productos", version="1.0.0")

products: list[dict] = []

next_id = 1

@app.get("/products", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def list_products(min_stock: int = 0) -> list[dict]:
    return [product for product in products if product["stock"] >= min_stock]

@app.get("/products/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate) -> dict:
    global next_id
    product = {
        "id": next_id,
        "name": payload.name,
        "price": payload.price,
        "stock": payload.stock
    }
    products.append(product)
    next_id += 1
    return product

@app.put("/products/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: int, payload: ProductUpdate) -> dict:
    for product in products:
        if product["id"] == product_id:
            product["name"] = payload.name
            product["price"] = payload.price
            product["stock"] = payload.stock
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int) -> Response:
    for index, product in enumerate(products):
        if product["id"] == product_id:
            del products[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")