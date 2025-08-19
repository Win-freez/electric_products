import uvicorn
from fastapi import FastAPI

from src.products.routers import router as product_router

app = FastAPI()
app.include_router(product_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
