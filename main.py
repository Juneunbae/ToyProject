from fastapi import FastAPI

# domain -> route
from route.Detail import DetailProduct
from route.Search import SearchProduct

app = FastAPI();

app.include_router(DetailProduct.router, prefix = "/search" ,tags=["Search"])
app.include_router(SearchProduct.router, prefix="/detail", tags=["Detail"])
