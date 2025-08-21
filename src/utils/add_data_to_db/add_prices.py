import logging
import traceback

from asyncpg.exceptions import PostgresError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError

from database.base import session_maker
from src.products.models import ProductPrices
from src.products.schemas import ProductPricesSchema
from src.utils.parsing_data.data_parser import DataParser
from src.utils.parsing_data.read_data_from_csv import make_dict_from_csv

logger = logging.getLogger(__name__)


async def add_data_prices(dp: DataParser) -> None:
    csv_path = r"/app/csv_files/цены электрика.csv"
    BATCH_SIZE = 100  # Размер батча для коммита

    async with session_maker() as session:
        try:
            counter = 0
            success_count = 0
            error_count = 0

            for item in make_dict_from_csv(csv_path):
                try:
                    all_data = dp.parse_price_data(item)
                    if not all_data:
                        logger.warning("Пустые данные для цен, пропускаем")
                        continue

                    prices_data = ProductPricesSchema(**all_data)
                    prices_dict = prices_data.model_dump(exclude_unset=True)

                    if not prices_dict.get("product_code"):
                        logger.warning(f"Отсутствует product_code в данных: {all_data}")
                        continue

                    stmt_prices = (
                        insert(ProductPrices)
                        .values(**prices_dict)
                        .on_conflict_do_update(
                            index_elements=["product_code"], set_=prices_dict
                        )
                    )

                    await session.execute(stmt_prices)
                    success_count += 1

                    # Коммитим батчами
                    if counter % BATCH_SIZE == 0 and counter > 0:
                        await session.commit()
                        logger.debug(f"Коммит батча: {counter} записей")

                    counter += 1

                except IntegrityError as e:
                    error_count += 1
                    logger.warning(
                        f"Ошибка целостности для {all_data.get('product_code')}: {e}"
                    )
                    await session.rollback()
                    continue

                except DataError as e:
                    error_count += 1
                    logger.exception(
                        f"Ошибка данных для {all_data.get('product_code')}: {e}"
                    )
                    await session.rollback()
                    continue

                except ValueError as e:
                    error_count += 1
                    logger.exception(f"Ошибка валидации для item {item}: {e}")
                    continue

                except Exception as e:
                    error_count += 1
                    logger.exception(
                        f"Неожиданная ошибка для {all_data.get('product_code')}: {e}"
                    )
                    await session.rollback()
                    continue

            # Финальный коммит
            await session.commit()
            logger.info(
                f"✅ Данные цен успешно обновлены! Обработано: {counter}, Успешно: {success_count}, Ошибок: {error_count}"
            )

        except SQLAlchemyError as e:
            await session.rollback()
            logger.exception(f"❌ Ошибка SQLAlchemy при обновлении цен: {e}")
            traceback.print_exc()

        except PostgresError as e:
            await session.rollback()
            logger.exception(f"❌ Ошибка PostgreSQL при обновлении цен: {e}")
            traceback.print_exc()

        except Exception as e:
            await session.rollback()
            logger.exception(f"❌ Критическая ошибка при обновлении цен: {e}")
            traceback.print_exc()
