from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.products.models import Product


class ProductService:
    @classmethod
    async def get_product(
        cls,
        session: AsyncSession,
        product_code: str,
    ) -> Product | None:
        stmt = (
            select(Product)
            .options(
                joinedload(Product.description),
                joinedload(Product.dimensions),
                joinedload(Product.prices),
                joinedload(Product.stock),
            )
            .where(Product.code == product_code)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()
