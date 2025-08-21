import logging

import uvicorn
from fastapi import FastAPI

from src.products.routers import router as product_router

app = FastAPI()
app.include_router(product_router)

logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d"
    " %(levelname)-7s - %(message)s",
    handlers=[logging.StreamHandler()],
)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
