from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# Base schemas
class ProductBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    code: str = Field(..., max_length=20, examples=["78962"])
    name: str = Field(..., max_length=500, examples=["Выключатель автоматический"])
    article: str | None = Field(None, max_length=100, examples=["SH201C16"])
    base_unit: str = Field(default="шт", max_length=20)
    main_unit: str = Field(default="шт", max_length=20)
    full_name: str = Field(..., max_length=500)
    status: str = Field(default="Активный", max_length=50)


class ProductDescriptionBase(BaseModel):
    comment: str | None = None
    main_property: str | None = Field(None, max_length=200)


class ProductOnlineBase(BaseModel):
    export_to_online_store: bool = False
    online_store_name: str | None = Field(None, max_length=500)
    block_discount: bool = False


class ProductDimensionsBase(BaseModel):
    length: Decimal | None = None
    width: Decimal | None = None
    height: Decimal | None = None
    volume: Decimal | None = None


class ProductBarcodeBase(BaseModel):
    barcode: str = Field(..., max_length=50, examples=["3606480586842"])


class ProductPricesBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    product_code: str = Field(..., max_length=20, examples=["00078962"])
    opt_card: Decimal | None = Field(None, ge=0, examples=[4500.00])
    opt_card_plus: Decimal | None = Field(None, ge=0, examples=[4250.00])
    opt: Decimal | None = Field(None, ge=0, examples=[3650.00])
    retail: Decimal | None = Field(None, ge=0, examples=[4500.00])
    gold: Decimal | None = Field(None, ge=0, examples=[4275.00])
    platinum: Decimal | None = Field(None, ge=0, examples=[4050.00])


class ProductStockBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    product_code: str = Field(..., max_length=20, examples=["00078962"])
    quantity: int = Field(default=0, ge=0)
    max_purchase: Decimal | None = Field(None, ge=0)


# Create schemas
class ProductDescriptionCreate(ProductDescriptionBase):
    pass


class ProductOnlineCreate(ProductOnlineBase):
    pass


class ProductDimensionsCreate(ProductDimensionsBase):
    pass


class ProductBarcodeCreate(ProductBarcodeBase):
    pass


class ProductPricesCreate(ProductPricesBase):
    pass


class ProductStockCreate(ProductStockBase):
    pass


class ProductCreate(ProductBase):
    description: ProductDescriptionCreate | None = None
    online_info: ProductOnlineCreate | None = None
    dimensions: ProductDimensionsCreate | None = None
    barcodes: list[ProductBarcodeCreate] | None = None
    prices: ProductPricesCreate | None = None
    stock: ProductStockCreate | None = None


# Response schemas
class ProductBarcodeResponse(ProductBarcodeBase):
    id: int
    product_code: str

    model_config = ConfigDict(from_attributes=True)


class ProductDescriptionResponse(ProductDescriptionBase):
    id: int
    product_code: str

    model_config = ConfigDict(from_attributes=True)


class ProductOnlineResponse(ProductOnlineBase):
    id: int
    product_code: str

    model_config = ConfigDict(from_attributes=True)


class ProductDimensionsResponse(ProductDimensionsBase):
    id: int
    product_code: str

    model_config = ConfigDict(from_attributes=True)


class ProductPricesResponse(ProductPricesBase):
    id: int
    code: str

    model_config = ConfigDict(from_attributes=True)


class ProductStockResponse(ProductStockBase):
    id: int
    product_code: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(ProductBase):
    description: ProductDescriptionResponse | None = None
    online_info: ProductOnlineResponse | None = None
    dimensions: ProductDimensionsResponse | None = None
    barcodes: list[ProductBarcodeResponse] = []
    prices: ProductPricesResponse | None = None
    stock: ProductStockResponse | None = None

    model_config = ConfigDict(from_attributes=True)


# Update schemas
class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=500)
    article: str | None = Field(None, max_length=100)
    base_unit: str | None = Field(None, max_length=20)
    main_unit: str | None = Field(None, max_length=20)
    full_name: str | None = Field(None, max_length=500)
    status: str | None = Field(None, max_length=50)


class ProductDescriptionUpdate(ProductDescriptionBase):
    pass


class ProductOnlineUpdate(ProductOnlineBase):
    pass


class ProductDimensionsUpdate(ProductDimensionsBase):
    pass


class ProductPricesUpdate(ProductPricesBase):
    pass


class ProductStockUpdate(ProductStockBase):
    pass


# Simplified schemas for lists
class ProductListItem(BaseModel):
    code: str
    name: str
    article: str | None
    status: str
    retail_price: Decimal | None
    quantity: int | None

    model_config = ConfigDict(from_attributes=True)


# Utility schemas
class ProductSearchResponse(BaseModel):
    products: list[ProductListItem]
    total_count: int
    page: int
    page_size: int


class BulkCreateResponse(BaseModel):
    created: int
    updated: int
    errors: list[str] = []
