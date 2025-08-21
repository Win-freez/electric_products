import asyncio
import os
import traceback

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.base import async_session
from src.products.models import (
    Product,
    ProductBarcode,
    ProductDescription,
    ProductDimensions,
    ProductOnline,
    ProductPrices,
    ProductStock,
)
from src.products.schemas import ProductPricesSchema, ProductStockSchema
from src.utils.parsing_data.data_parser import DataParser
from src.utils.parsing_data.read_data_from_csv import make_dict_from_csv

dp = DataParser()


async def add_data_products() -> None:
    # Правильный путь к файлу внутри контейнера
    csv_path = "/app/csv_files/Справочник электрика.csv"

    # Проверяем существование файла
    if not os.path.exists(csv_path):
        print(f"❌ Файл не найден: {csv_path}")
        print("📁 Доступные файлы в /app:")
        for root, _dirs, files in os.walk("/app"):
            print(f"  {root}: {files}")
        return

    print(f"📖 Чтение файла: {csv_path}")

    async with async_session() as session:
        try:
            count = 0
            for item in make_dict_from_csv(csv_path):
                all_data = dp.parse_product_data(item)

                # Проверяем, есть ли уже продукт с таким кодом
                existing_product = await session.execute(
                    select(Product).where(Product.code == all_data["product"]["code"])
                )
                if existing_product.scalar():
                    print(
                        f"⚠️  Пропускаем существующий продукт:"
                        f" {all_data['product']['code']}"
                    )
                    continue

                product_data = Product(**all_data["product"])
                session.add(product_data)
                await session.flush()

                product_code = product_data.code
                objects_to_add = []

                description_data = ProductDescription(
                    product_code=product_code, **all_data["description"]
                )
                online_data = ProductOnline(
                    product_code=product_code, **all_data["online_info"]
                )
                dimensions_data = ProductDimensions(
                    product_code=product_code, **all_data["dimensions"]
                )

                objects_to_add.extend([description_data, online_data, dimensions_data])

                for barcode_data in all_data["barcodes"]:
                    barcode_obj = ProductBarcode(
                        product_code=product_code, **barcode_data
                    )
                    objects_to_add.append(barcode_obj)

                session.add_all(objects_to_add)
                count += 1

                if count % 100 == 0:
                    print(f"✅ Обработано {count} продуктов")
                    await session.commit()  # Периодический коммит

            await session.commit()
            print(f"🎉 Импорт завершен! Добавлено {count} продуктов")

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при импорте: {e}")
            traceback.print_exc()


async def add_data_prices() -> None:
    csv_path = r"/app/csv_files/цены электрика.csv"

    async with async_session() as session:
        try:
            counter = 0
            for item in make_dict_from_csv(csv_path):
                all_data = dp.parse_price_data(item)

                prices_data = ProductPricesSchema(**all_data)
                stocks_data = ProductStockSchema(**all_data)

                stock_dict = stocks_data.model_dump(exclude_unset=True)
                prices_dict = prices_data.model_dump(exclude_unset=True)

                stmt_stock = (
                    insert(ProductStock)
                    .values(**stock_dict)
                    .on_conflict_do_update(
                        index_elements=["product_code"], set_=stock_dict
                    )
                )

                stmt_prices = (
                    insert(ProductPrices)
                    .values(**prices_dict)
                    .on_conflict_do_update(
                        index_elements=["product_code"], set_=prices_dict
                    )
                )

                await session.execute(stmt_stock)
                await session.execute(stmt_prices)

                if counter % 100 == 0:
                    await session.commit()

                counter += 1

            await session.commit()
            print(f"✅ Данные цен успешно обновлены! {counter}")

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при обновлении цен: {e}")
            traceback.print_exc()


async def main() -> None:
    await add_data_products()
    await add_data_prices()


asyncio.run(main())
