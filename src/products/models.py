from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Product(Base):
    __tablename__ = "products"

    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    article: Mapped[str | None] = mapped_column(String(100))
    base_unit: Mapped[str] = mapped_column(String(20), default="шт")
    main_unit: Mapped[str] = mapped_column(String(20), default="шт")
    full_name: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="Активный")

    description: Mapped["ProductDescription"] = relationship(
        "ProductDescription", back_populates="product", uselist=False
    )
    online_info: Mapped["ProductOnline"] = relationship(
        "ProductOnline", back_populates="product", uselist=False
    )
    dimensions: Mapped["ProductDimensions"] = relationship(
        "ProductDimensions", back_populates="product", uselist=False
    )
    barcodes: Mapped[list["ProductBarcode"]] = relationship(
        "ProductBarcode", back_populates="product"
    )
    prices: Mapped["ProductPrices"] = relationship(
        "ProductPrices", back_populates="product", uselist=False
    )
    stock: Mapped["ProductStock"] = relationship(
        "ProductStock", back_populates="product", uselist=False
    )


class ProductDescription(Base):
    __tablename__ = "product_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(ForeignKey("products.code"))
    comment: Mapped[str | None] = mapped_column(Text)
    main_property: Mapped[str | None] = mapped_column(String(200))

    product: Mapped["Product"] = relationship("Product", back_populates="description")


class ProductOnline(Base):
    __tablename__ = "product_online"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(ForeignKey("products.code"))
    export_to_online_store: Mapped[bool] = mapped_column(Boolean, default=False)
    online_store_name: Mapped[str | None] = mapped_column(String(500))
    block_discount: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped["Product"] = relationship("Product", back_populates="online_info")


class ProductDimensions(Base):
    __tablename__ = "product_dimensions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(ForeignKey("products.code"))
    length: Mapped[float | None] = mapped_column(Numeric(10, 2))
    width: Mapped[float | None] = mapped_column(Numeric(10, 2))
    height: Mapped[float | None] = mapped_column(Numeric(10, 2))
    volume: Mapped[float | None] = mapped_column(Numeric(10, 2))

    product: Mapped["Product"] = relationship("Product", back_populates="dimensions")


class ProductBarcode(Base):
    __tablename__ = "product_barcodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(ForeignKey("products.code"))
    barcode: Mapped[str] = mapped_column(String(50), unique=True)

    product: Mapped["Product"] = relationship("Product", back_populates="barcodes")


class ProductPrices(Base):
    __tablename__ = "products_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        ForeignKey("products.code"), nullable=False, unique=True, index=True
    )

    # Цены по статусам
    opt_card: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    opt_card_plus: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    opt: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    retail: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    gold: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    platinum: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    product: Mapped["Product"] = relationship(
        "Product", back_populates="prices", uselist=False
    )


class ProductStock(Base):
    __tablename__ = "product_stocks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_code: Mapped[str] = mapped_column(ForeignKey("products.code"))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    max_purchase: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, default_factory=func.now, onupdate=datetime.now
    )

    product: Mapped["Product"] = relationship("Product", back_populates="stock")
