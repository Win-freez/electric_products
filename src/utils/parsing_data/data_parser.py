import re
from decimal import Decimal, InvalidOperation
from typing import Any


class DataParser:
    """Класс для парсинга данных из CSV в структуры для моделей"""

    @staticmethod
    def _clean_str(value: Any) -> str:
        """Очищает строку от лишних пробелов"""
        if value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def _parse_bool(value: Any) -> bool:
        """Парсит boolean значения"""
        if value is None:
            return False
        str_value = str(value).strip().lower()
        return str_value in ("1", "true", "yes", "y", "да")

    @staticmethod
    def _parse_int(value: Any) -> int | None:
        """Парсит integer значения"""
        if value is None or value == "":
            return None
        try:
            # Удаляем все нецифровые символы кроме минуса
            cleaned = re.sub(r"[^\d\-]", "", str(value))
            if not cleaned:
                return None
            return int(cleaned)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_decimal(value: Any) -> Decimal | None:
        """Парсит decimal значения из различных форматов"""
        if value is None or value == "":
            return None

        try:
            str_value = str(value).strip()

            # Заменяем запятые на точки и удаляем пробелы
            str_value = str_value.replace(",", ".").replace(" ", "")

            # Обрабатываем научную нотацию
            if "e" in str_value.lower():
                return Decimal(float(str_value))

            return Decimal(str_value)

        except (ValueError, TypeError, InvalidOperation):
            return None

    @staticmethod
    def _parse_barcodes(barcodes_str: str) -> list[dict[str, str]]:
        """Парсит штрихкоды из строки"""
        if not barcodes_str:
            return []

        barcodes = []

        # Разделяем по разным разделителям
        for barcode in re.split(r"[\n\r,;]+", str(barcodes_str)):
            cleaned_barcode = barcode.strip()
            if cleaned_barcode and cleaned_barcode.lower() != "nan":
                # Очищаем от лишних символов, оставляем только цифры
                cleaned_barcode = re.sub(r"[^\d]", "", barcode)
                if cleaned_barcode:
                    barcodes.append({"barcode": cleaned_barcode})

        return barcodes

    def parse_product_data(self, data: dict[str, Any]) -> dict:
        """Парсит сырые данные товара в структуру для моделей"""

        # Основной продукт
        product_data = {
            "code": self._clean_str(data.get("Код", "")),
            "name": self._clean_str(data.get("Наименование", "")),
            "article": self._clean_str(data.get("Артикул")) or None,
            "base_unit": self._clean_str(data.get("Базовая единица измерения", "шт")),
            "main_unit": self._clean_str(data.get("Основная единица измерения", "шт")),
            "full_name": self._clean_str(data.get("Полное наименование", "")),
            "status": self._clean_str(data.get("Статус товара", "Активный")),
        }

        # Описание
        description_data = {
            "comment": self._clean_str(data.get("Комментарий")) or None,
            "main_property": self._clean_str(data.get("Основное свойство")) or None,
        }

        # Онлайн информация
        online_data = {
            "export_to_online_store": self._parse_bool(
                data.get("ВыгружатьВИнтернетМагазин")
            ),
            "online_store_name": self._clean_str(data.get("НаименованиеИМ")) or None,
            "block_discount": self._parse_bool(data.get("Блокировать скидку по карте")),
        }

        # Габариты
        dimensions_data = {
            "length": self._parse_decimal(data.get("Длинна")),
            "width": self._parse_decimal(data.get("Ширина")),
            "height": self._parse_decimal(data.get("Высота")),
            "volume": self._parse_decimal(data.get("Объем")),
        }

        # Штрихкоды
        barcodes_data = self._parse_barcodes(data.get("Штрихкоды номенклатуры", ""))

        return {
            "product": product_data,
            "description": description_data,
            "online_info": online_data,
            "dimensions": dimensions_data,
            "barcodes": barcodes_data,
        }

    def parse_price_data(self, data: dict[str, Any]) -> dict:
        """Парсит данные цен"""
        return {
            "product_code": self._clean_str(data.get("Код\nноменклатуры", "")),
            "quantity": self._parse_int(data.get("Кол-во\nна складах")),
            "max_purchase": self._parse_decimal(data.get("Макс.\nзакупка")),
            "opt_card": self._parse_decimal(data.get("Опт Карта Рубин")),
            "opt_card_plus": self._parse_decimal(data.get("Опт Карта Рубин +")),
            "opt": self._parse_decimal(data.get("Оптовая цена")),
            "retail": self._parse_decimal(data.get("Розничная цена")),
            "gold": self._parse_decimal(data.get("gold")),
            "platinum": self._parse_decimal(data.get("platinum")),
        }

    # Дополнительные методы для других типов данных
    def parse_stock_data(self, data: dict[str, Any]) -> dict:
        """Парсит данные остатков"""
        return {
            "product_code": self._clean_str(data.get("Код", "")),
            "quantity": self._parse_int(data.get("Количество", 0)),
            "warehouse": self._clean_str(data.get("Склад", "")),
        }
