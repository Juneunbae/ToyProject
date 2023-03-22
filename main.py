from fastapi import FastAPI

from domain.Detail import DetailProduct
from domain.Search import SearchProduct

app = FastAPI();

app.include_router(SearchProduct.router)
app.include_router(DetailProduct.router)
