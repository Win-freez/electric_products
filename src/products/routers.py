from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db
from src.products.schemas import ProductResponseSchema
from src.products.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{product_code}", status_code=status.HTTP_200_OK)
async def get_product(
    product_code: Annotated[str, Path()],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ProductResponseSchema:
    product = await ProductService.get_product(
        session=session, product_code=product_code
    )

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ProductResponseSchema.model_validate(product)
