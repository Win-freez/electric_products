import logging
from typing import Any

from sqlalchemy import select

from database.base import session_maker
from src.products.models import ProductStock
from src.warehouses.models import Warehouse

logger = logging.getLogger(__name__)


async def add_stock_data(data: list[dict[str, Any]]) -> None:
    async with session_maker() as session:
        result = await session.execute(select(Warehouse))
        warehouses = result.scalars().all()
        warehouses_mapping = {warehouse.name: warehouse.id for warehouse in warehouses}

        logger.info("Найдено складов: %d", len(warehouses_mapping))

        for index, item in enumerate(data):
            try:
                product_code = item.get("Код", "").strip()
                reserved_str = item.get("Выписано но не выдано", "").strip()
                reserved = int(reserved_str) if reserved_str.isdigit() else 0
                for k, v in item.items():
                    if k in warehouses_mapping:
                        warehouse_id = warehouses_mapping[k]
                        quantity = int(v.strip()) if v.strip().isdigit() else 0

                        session.add(
                            ProductStock(
                                product_code=product_code,
                                warehouse_id=warehouse_id,
                                quantity=quantity,
                                reserved=reserved,
                            )
                        )

                        logger.info(
                            "Добавлен в очередь: product_code=%s, warehouse_id=%d, quantity=%d, reserved=%d",
                            product_code,
                            warehouse_id,
                            quantity,
                            reserved,
                        )

                if index % 100 == 0:
                    await session.commit()
            except Exception as e:
                logger.exception("Произошла ошибка %s", e)

        await session.commit()
