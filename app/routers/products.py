from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   responses={404: {"description": "Not found"}},
                   tags=["products"]
                   )


@router.get("/")
async def get_products():
    products = ['product1', 'product2', 'product3']
    return {'products': products}
