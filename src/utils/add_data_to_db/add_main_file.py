import asyncio

from files.warehouses_data import warehouses
from src.utils.add_data_to_db.add_product_stocks import add_stock_data

asyncio.run(add_stock_data(data=warehouses))
