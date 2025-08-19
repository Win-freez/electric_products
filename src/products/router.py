from fastapi import APIRouter, status

router = APIRouter(prefix='/products', tags=['products'])

@router.get('/', status_code=status.HTTP_200_OK)
async def get_products():
    return [1, 2, 3]


@router.get('/{slug}', status_code=status.HTTP_200_OK)
async def get_product(slug: str):
    return slug