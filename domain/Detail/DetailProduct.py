from fastapi import APIRouter

import json
import urllib.request
import ssl
import requests

from typing import Optional

from domain.Search.SearchProduct import search

router = APIRouter(
    prefix="/detail"
)


@router.get("/naver/{product_name}/{product_id}")
def detail(product_name : str, product_id : int) :
    client_id = "sAArpAJVGBAtGDwkHpDo"
    client_secret = "k7db8QphAv"

    ssl._create_default_https_context = ssl._create_unverified_context

    Product = urllib.parse.quote(f"{product_name}")

    # start = page,
    # display = 한번에 표시할 검색 결과 개수
    # sort - sim : 정확도 순 내림차순,
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
        return {"Error" : f"{rescode} - 잘못된 경로입니다."}


@router.get("/market/{product_name}/{item_num}")
def MarketDetail(product_name : str, item_num : int, page_num : Optional[int] = 1) :
    SessionURL = "https://www.kurly.com/nx/api/session"

    header = {
        "baggage": "sentry-environment=production,sentry-release=6201597e10ad3e5fcdbca79f4233f870d4e5f70c,sentry-transaction=/main,sentry-public_key=85c17d02a54d4d19a97d45bf142467a9,sentry-trace_id=0eb57706ddf44b79b4126aba47a9826b,sentry-sample_rate=1",
        "cookie": "PHPSESSID=8kih11umha03373dsdg9cfcm4raf1anbbtjsj145djc0nm9ihkt1; cookie_check=0; shop_authenticate=Y; Xtime=1679465643; __cfruid=bfec21dd288ca16d5891ab78b3c22d543f6f9c0f-1679465643; _ga=GA1.1.604851465.1679465649; amp_65bebb=sgxZNhjsNBv7ZBQiH1cQ3k.bnVsbA==..1gs429hnu.1gs43ojnu.c.1.d; _ga_BJ5N3PD9QG=GS1.1.1679468842.2.1.1679470872.60.0.0",
        "referer": "https://www.kurly.com/main",
        "sentry-trace": "0eb57706ddf44b79b4126aba47a9826b-973bbc0b66246190-1",
        "uger-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44"
    }

    SessionRes = requests.get(SessionURL, headers=header)

    SessionJson = SessionRes.json()

    accessToken = SessionJson['accessToken']

    url = f"https://api.kurly.com/search/v3/sites/market/normal-search?keyword={product_name}&sort_type=&page={page_num}&per_page=20&filters="

    header = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
        'authorization': f'Bearer {accessToken}',
        'origin': "https://www.kurly.com"
    }

    data = {
        'keyword': product_name,
        "sort_type": '',
        'page': page_num,
        'per_page': 20,
        'filters': ''
    }

    res = requests.get(url, headers=header, json=data)

    datas = res.json()

    no = datas['data'][item_num]['no']

    ProductURL = f"https://www.kurly.com/_next/data/qYp9ATa15A-VuV5Z2OJxN/goods/{no}.json?productCode={no}"

    ProductHeader = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
        'authority': "www.kurly.com"
    }

    ProductData = {
        'productCode': f"{no}"
    }

    ProductRes = requests.get(ProductURL, headers=ProductHeader, json=ProductData)


    ProJson = ProductRes.json()

    return ProJson["pageProps"]['product']