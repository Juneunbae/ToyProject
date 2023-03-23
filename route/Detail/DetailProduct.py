from fastapi import APIRouter, status

from typing import Optional

from Controller.Product.Detail.Naver import Naver
from Controller.Product.Detail.MarketKurly import MarketKurly

router = APIRouter(
    prefix="/detail"
)


@router.get("/naver/{product_name}/{product_id}", status_code=status.HTTP_200_OK, description="네이버 쇼핑 상품 상세정보")
def NaverDetail(product_name : str, product_id : int) :
    Naver(product_name=product_name, product_id=product_id)


@router.get("/market/{product_name}/{item_num}", status_code=status.HTTP_200_OK, description="마켓컬리 상품 상세정보")
def KurlyDetail(product_name : str, item_num : int, page_num : Optional[int] = 1) :
    MarketKurly(product_name=product_name, item_num=item_num, page_num=page_num)