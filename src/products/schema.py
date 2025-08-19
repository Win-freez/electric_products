from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductPrice(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    opt_card: Decimal
    opt_card_plus: Decimal
    opt: Decimal
    retail: Decimal
    gold: Decimal
    platinum: Decimal


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    article: str | None
    base_measure: str | None
    to_block_discount: bool | None
    upload_to_online_shop: bool | None
    high: int | float | None
    length: int | float | None
    code: str
    comment: str | None
    name: str
    name_for_online_shop: str | None
    capacity: int | float | None
    main_measure: str
    status: str | None
    width: int | float | None
    barcode: str
    price: ProductPrice
    total_quantity: int
