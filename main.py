from fastapi import FastAPI

# domain -> route
from route.Detail import DetailProduct
from route.Search import SearchProduct

app = FastAPI();

app.include_router(DetailProduct.router ,tags=["Detail"])
app.include_router(SearchProduct.router, tags=["Search"])
