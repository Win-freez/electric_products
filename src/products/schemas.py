from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# Base schemas
class ProductSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    code: str = Field(..., max_length=20, examples=["00078962"])
    name: str = Field(..., max_length=500, examples=["Выключатель автоматический"])
    article: str | None = Field(None, max_length=100, examples=["SH201C16"])
    base_unit: str = Field(default="шт", max_length=20)
    main_unit: str = Field(default="шт", max_length=20)
    full_name: str = Field(..., max_length=500)
    status: str = Field(default="Активный", max_length=50)


class ProductDescriptionSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    comment: str | None = None
    main_property: str | None = Field(None, max_length=200)


class ProductOnlineSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    export_to_online_store: bool = False
    online_store_name: str | None = Field(None, max_length=500)
    block_discount: bool = False


class ProductDimensionsSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    length: Decimal | None = None
    width: Decimal | None = None
    height: Decimal | None = None
    volume: Decimal | None = None


class ProductBarcodeSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    barcode: str = Field(..., max_length=50, examples=["3606480586842"])


class ProductPricesSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    product_code: str = Field(..., max_length=20, examples=["00078962"])
    opt_card: Decimal | None = Field(None, ge=0, examples=[4500.00])
    opt_card_plus: Decimal | None = Field(None, ge=0, examples=[4250.00])
    opt: Decimal | None = Field(None, ge=0, examples=[3650.00])
    retail: Decimal | None = Field(None, ge=0, examples=[4500.00])
    gold: Decimal | None = Field(None, ge=0, examples=[4275.00])
    platinum: Decimal | None = Field(None, ge=0, examples=[4050.00])


class ProductStockSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    product_code: str = Field(..., max_length=20, examples=["00078962"])
    quantity: int = Field(default=0, ge=0)
    max_purchase: Decimal | None = Field(None, ge=0, exclude=True)


class ProductResponseSchema(ProductSchema):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    description: ProductDescriptionSchema | None = None
    dimensions: ProductDimensionsSchema | None = None
    prices: ProductPricesSchema | None = None
    stock: ProductStockSchema | None = None
