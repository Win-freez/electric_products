import logging
import os
import traceback

from asyncpg.exceptions import PostgresError
from sqlalchemy import select
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError

from database.base import session_maker
from src.products.models import (
    Product,
    ProductBarcode,
    ProductDescription,
    ProductDimensions,
    ProductOnline,
)
from src.utils.parsing_data.data_parser import DataParser
from src.utils.parsing_data.read_data_from_csv import make_dict_from_csv

logger = logging.getLogger(__name__)


async def add_data_products(dp: DataParser) -> None:
    csv_path = "/app/csv_files/Справочник электрика.csv"
    BATCH_SIZE = 50  # Размер батча для коммита

    # Проверяем существование файла
    if not os.path.exists(csv_path):
        logger.exception(f"Файл не найден: {csv_path}")
        logger.info("Доступные файлы в /app:")
        for root, _dirs, files in os.walk("/app"):
            if files:
                logger.info(f"  {root}: {files}")
        return

    logger.info(f"Начат импорт из файла: {csv_path}")

    async with session_maker() as session:
        try:
            total_count = 0
            success_count = 0
            skipped_count = 0
            error_count = 0

            for item in make_dict_from_csv(csv_path):
                try:
                    all_data = dp.parse_product_data(item)
                    if not all_data or "product" not in all_data:
                        logger.warning("Пропускаем item с пустыми данными")
                        continue

                    product_code = all_data["product"].get("code")
                    if not product_code:
                        logger.warning("Пропускаем item без product code")
                        continue

                    # Проверяем, есть ли уже продукт с таким кодом
                    existing_product = await session.execute(
                        select(Product).where(Product.code == product_code)
                    )
                    if existing_product.scalar_one_or_none():
                        skipped_count += 1
                        if skipped_count % 100 == 0:
                            logger.debug(
                                f"Пропущено {skipped_count} существующих продуктов"
                            )
                        continue

                    # Создаем продукт и связанные объекты
                    product_data = Product(**all_data["product"])
                    session.add(product_data)
                    await session.flush()  # Получаем ID для связей

                    objects_to_add = []

                    # Description
                    if all_data.get("description"):
                        description_data = ProductDescription(
                            product_code=product_code, **all_data["description"]
                        )
                        objects_to_add.append(description_data)

                    # Online info
                    if all_data.get("online_info"):
                        online_data = ProductOnline(
                            product_code=product_code, **all_data["online_info"]
                        )
                        objects_to_add.append(online_data)

                    # Dimensions
                    if all_data.get("dimensions"):
                        dimensions_data = ProductDimensions(
                            product_code=product_code, **all_data["dimensions"]
                        )
                        objects_to_add.append(dimensions_data)

                    # Barcodes
                    if "barcodes" in all_data:
                        for barcode_data in all_data["barcodes"]:
                            if barcode_data:  # Проверяем не пустой ли словарь
                                barcode_obj = ProductBarcode(
                                    product_code=product_code, **barcode_data
                                )
                                objects_to_add.append(barcode_obj)

                    if objects_to_add:
                        session.add_all(objects_to_add)

                    total_count += 1
                    success_count += 1

                    # Периодический коммит
                    if total_count % BATCH_SIZE == 0:
                        await session.commit()
                        logger.info(
                            f"Обработано {total_count} продуктов (Успешно: {success_count}, Ошибок: {error_count})"
                        )

                except IntegrityError as e:
                    error_count += 1
                    await session.rollback()
                    logger.warning(
                        f"Ошибка целостности для продукта {product_code}: {e}"
                    )
                    continue

                except DataError as e:
                    error_count += 1
                    await session.rollback()
                    logger.exception(f"Ошибка данных для продукта {product_code}: {e}")
                    continue

                except ValueError as e:
                    error_count += 1
                    logger.exception(f"Ошибка валидации для item: {e}")
                    continue

                except Exception as e:
                    error_count += 1
                    await session.rollback()
                    logger.exception(
                        f"Неожиданная ошибка для продукта {product_code}: {e}"
                    )
                    continue

            # Финальный коммит
            await session.commit()
            logger.info(
                f"Импорт завершен! "
                f"Всего: {total_count}, "
                f"Успешно: {success_count}, "
                f"Пропущено: {skipped_count}, "
                f"Ошибок: {error_count}"
            )

        except SQLAlchemyError as e:
            await session.rollback()
            logger.exception(f"Ошибка SQLAlchemy при импорте: {e}")
            traceback.print_exc()

        except PostgresError as e:
            await session.rollback()
            logger.exception(f"Ошибка PostgreSQL при импорте: {e}")
            traceback.print_exc()

        except Exception as e:
            await session.rollback()
            logger.exception(f"Критическая ошибка при импорте: {e}")
            traceback.print_exc()
