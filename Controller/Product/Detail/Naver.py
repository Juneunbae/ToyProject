from fastapi import HTTPException

import json
import urllib.request
import ssl


def Naver(product_name, product_id) :
    client_id = "sAArpAJVGBAtGDwkHpDo"
    client_secret = "k7db8QphAv"

    ssl._create_default_https_context = ssl._create_unverified_context

    Product = urllib.parse.quote(f"{product_name}")

    # start = page
    # display = 한번에 표시할 검색 결과 개수
    # sort - sim : 정확도 순 내림차순
    # sort - date : 날짜 순 내림차순
    url = f"https://openapi.naver.com/v1/search/shop?query={Product}&start=1&display=100"  # JSON 결과

    request = urllib.request.Request(url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        json_object = json.loads(response_body.decode('utf-8'))

        return json_object['items'][product_id]
    else:
        raise HTTPException(status_code=404, detail="잘못된 경로입니다.")