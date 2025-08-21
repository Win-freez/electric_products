from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DECIMAL,
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from src.warehouses.models import Warehouse


class Product(Base):
    __tablename__ = "products"

    code: Mapped[str] = mapped_column(String(20), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    article: Mapped[str | None] = mapped_column(String(100))
    base_unit: Mapped[str] = mapped_column(String(20), default="шт")
    main_unit: Mapped[str] = mapped_column(String(20), default="шт")
    full_name: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="Активный")

    description: Mapped["ProductDescription"] = relationship(
        "ProductDescription",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    online_info: Mapped["ProductOnline"] = relationship(
        "ProductOnline",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    dimensions: Mapped["ProductDimensions"] = relationship(
        "ProductDimensions",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    barcodes: Mapped[list["ProductBarcode"]] = relationship(
        "ProductBarcode", back_populates="product", cascade="all, delete-orphan"
    )
    prices: Mapped["ProductPrices"] = relationship(
        "ProductPrices",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    stocks: Mapped[list["ProductStock"]] = relationship(
        "ProductStock",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductDescription(Base):
    __tablename__ = "product_descriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(
        ForeignKey("products.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    comment: Mapped[str | None] = mapped_column(Text)
    main_property: Mapped[str | None] = mapped_column(String(200))

    product: Mapped["Product"] = relationship(
        "Product", back_populates="description", uselist=False
    )


class ProductOnline(Base):
    __tablename__ = "product_online"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(
        ForeignKey("products.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    export_to_online_store: Mapped[bool] = mapped_column(Boolean, default=False)
    online_store_name: Mapped[str | None] = mapped_column(String(500))
    block_discount: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped["Product"] = relationship(
        "Product", back_populates="online_info", uselist=False
    )


class ProductDimensions(Base):
    __tablename__ = "product_dimensions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(
        ForeignKey("products.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    length: Mapped[float | None] = mapped_column(Numeric(10, 2))
    width: Mapped[float | None] = mapped_column(Numeric(10, 2))
    height: Mapped[float | None] = mapped_column(Numeric(10, 2))
    volume: Mapped[float | None] = mapped_column(Numeric(10, 2))

    product: Mapped["Product"] = relationship(
        "Product", back_populates="dimensions", uselist=False
    )


class ProductBarcode(Base):
    __tablename__ = "product_barcodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(
        ForeignKey("products.code", onupdate="CASCADE", ondelete="CASCADE")
    )
    barcode: Mapped[str] = mapped_column(String(50))

    product: Mapped["Product"] = relationship("Product", back_populates="barcodes")


class ProductPrices(Base):
    __tablename__ = "products_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(
        ForeignKey("products.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Цены по статусам
    opt_card: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    opt_card_plus: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    opt: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    retail: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    gold: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    platinum: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))

    product: Mapped["Product"] = relationship(
        "Product", back_populates="prices", uselist=False
    )


class ProductStock(Base):
    __tablename__ = "product_stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(
        ForeignKey("products.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    reserved: Mapped[int] = mapped_column(default=0, server_default=text("0"))

    product: Mapped["Product"] = relationship("Product", back_populates="stocks")

    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="stocks")

    __table_args__ = (
        UniqueConstraint("product_code", "warehouse_id", name="uq_product_warehouse"),
    )
