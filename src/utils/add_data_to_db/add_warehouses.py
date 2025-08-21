import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.base import session_maker
from files.warehouses_data import warehouses
from src.warehouses.models import Warehouse

logger = logging.getLogger(__name__)


async def add_warehouses():
    try:
        async with session_maker() as session:
            warehouses_to_add = []
            for warehouse in warehouses:
                warehouses_to_add.append(Warehouse(**warehouse))

            session.add_all(warehouses_to_add)
            await session.commit()

            logger.info(f"Успешно добавлено {len(warehouses_to_add)} складов")
            return True

    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
            logger.warning("Некоторые склады уже существуют (нарушение уникальности)")

    except SQLAlchemyError as e:
        await session.rollback()
        logger.exception(f"Ошибка SQLAlchemy: {e}")
        return False

    except Exception as e:
        await session.rollback()
        logger.exception(f"Неожиданная ошибка: {e}")
        return False
