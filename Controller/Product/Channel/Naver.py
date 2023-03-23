import json
import urllib.request
import ssl
import requests

from fastapi import HTTPException


class Naver:
    def __init__(self):
        self.client_id = "sAArpAJVGBAtGDwkHpDo"
        self.client_secret = "k7db8QphAv"

    def Search(self, product_name):

        ssl._create_default_https_context = ssl._create_unverified_context

        Product = urllib.parse.quote(f"{product_name}")

        # start = page,
        # display = 한번에 표시할 검색 결과 개수
        # sort - sim : 정확도 순 내림차순,
        # sort - date : 날짜 순 내림차순
        url = f"https://openapi.naver.com/v1/search/shop?query={Product}&start=1&display=100"  # JSON 결과

        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)

        response = urllib.request.urlopen(request)

        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            json_object = json.loads(response_body.decode('utf-8'))

            return json_object
        else:
            raise HTTPException(status_code=404, detail="잘못된 경로 입니다.")

    def Detail(self, product_name, product_id):
        ssl._create_default_https_context = ssl._create_unverified_context

        Product = urllib.parse.quote(f"{product_name}")

        # start = page
        # display = 한번에 표시할 검색 결과 개수
        # sort - sim : 정확도 순 내림차순
        # sort - date : 날짜 순 내림차순
        url = f"https://openapi.naver.com/v1/search/shop?query={Product}&start=1&display=100"  # JSON 결과

        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)

        response = urllib.request.urlopen(request)

        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            json_object = json.loads(response_body.decode('utf-8'))

            result = json_object['items'][product_id]
            
            return result
        else:
            raise HTTPException(status_code=404, detail="잘못된 경로입니다.")