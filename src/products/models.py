from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )

    prices: Mapped["ProductPrices"] = relationship(
        "ProductPrices", back_populates="product", uselist=False
    )


class ProductPrices(Base):
    __tablename__ = "products_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        ForeignKey("products.code"), nullable=False, unique=True, index=True
    )
    opt_card: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    opt_card_plus: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    opt: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    retail: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    gold: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    platinum: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    product: Mapped["Product"] = relationship(
        "Product", back_populates="prices", uselist=False
    )
