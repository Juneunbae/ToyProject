from fastapi import APIRouter, status

from typing import Optional

from Controller.Product.Channel.Naver import Naver
from Controller.Product.Channel.MarketKurly import MarketKurly

router = APIRouter(
    prefix="/detail"
)


@router.get("/naver/{product_name}/{product_id}", status_code=status.HTTP_200_OK, description="네이버 쇼핑 상품 상세정보")
def NaverDetail(product_name : str, product_id : int) :
    return Naver().Detail(product_name=product_name, product_id=product_id)


@router.get("/market/{product_id}/{item_num}", status_code=status.HTTP_200_OK, description="마켓컬리 상품 상세정보")
def KurlyDetail(item_num : int, product_name : str) :
    return MarketKurly().Detail(item_num=item_num, product_name=product_name)