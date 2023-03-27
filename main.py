from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
# domain -> route
from route.Detail import DetailProduct
from route.Search import SearchProduct


description = """
ToyProject - API 🚀

## 기능 목록

1. Search
   : 쇼핑몰 내 상품 검색

2. Detail
   : 상품 상세정보

"""

tags_metadata = [
    {
        "name": "Detail",
        "description": "쇼핑몰 상품 상세정보 API",
    },
    {
        "name": "Search",
        "description": "쇼핑몰 내 상품 검색 API",
    },
]

app = FastAPI(
    title = "Toy Project",
    description=description,
    openapi_tags=tags_metadata
);

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(DetailProduct.router, tags=["Detail"])
app.include_router(SearchProduct.router, tags=["Search"])
