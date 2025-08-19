import uvicorn
from fastapi import FastAPI

from src.products.router import router as product_router

app = FastAPI()
app.include_router(product_router)



if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)