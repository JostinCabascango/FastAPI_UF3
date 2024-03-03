from fastapi import FastAPI

from routers import products, categories, subcategories

app = FastAPI()

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(subcategories.router)
