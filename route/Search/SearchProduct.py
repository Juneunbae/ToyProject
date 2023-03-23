from fastapi import APIRouter

from typing import Optional

from Controller.Product.Search.Naver import Naver
from Controller.Product.Search.MarketKurly import MarKetKurly

router = APIRouter(
    prefix="/search"
)


@router.get("/naver/{product_name}", description="네이버 쇼핑 상품 검색") # description
def NaverSearch(product_name : str) :
    Naver(product_name=product_name)


@router.get("/market/{product_name}", description="마켓 컬리 상품 검색")
def KurlySearch(product_name : str, page_num : Optional[int] = 1) :
    MarKetKurly(product_name=product_name, page_num=page_num)