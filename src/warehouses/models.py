from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from src.products.models import ProductStock


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    address: Mapped[str | None] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    stocks: Mapped[list["ProductStock"]] = relationship(
        back_populates="warehouse",
        cascade="all, delete-orphan",
    )
