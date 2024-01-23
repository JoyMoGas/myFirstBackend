from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message" : "No encontrado"}})

products_list = ["Producto 1", "Producto 2","Producto 3", "Producto 4", "Producto 5"]

# Motrar los productos
@router.get("/")
async def get_products():
    return products_list

# Mostrar los productos con Index
@router.get("/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def get_products_by_id(id: int):
    if id < 0 or id >= len(products_list):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return products_list[id]
