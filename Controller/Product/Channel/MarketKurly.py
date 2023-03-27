from fastapi import HTTPException

import requests

from Database.database import Connect
from Database.query.Product import DeleteList, InsertList, SelectDetail

import time


class MarketKurly :
    def __init__(self):
        self.conn = Connect()
        self.cur = self.conn.cursor()

    def Detail(self, item_num):
        start = time.time()
        i = item_num - 1

        self.cur.execute(SelectDetail)
        result = self.cur.fetchall()

        DetailData = [{
            "PRODUCT_ID" : result[i][1],
            "PRODUCT_NAME" : result[i][2],
            "PRICE" : result[i][3],
            "SELLER" : result[i][4],
            "OPTION" : " ",
            "IMAGE" : result[i][5],
            # "Shop" : result[i][6],
            # "Created" : result[i][7],
        }]
        end = time.time()

        print(f"수행 시간 : {end - start}")

        return DetailData

    def Search(self, product_name, page_num):
        start = time.time()
        self.cur.execute(DeleteList)

        SessionURL = "https://www.kurly.com/nx/api/session"

        header = {
            "baggage": "sentry-environment=production,sentry-release=6201597e10ad3e5fcdbca79f4233f870d4e5f70c,sentry-transaction=/main,sentry-public_key=85c17d02a54d4d19a97d45bf142467a9,sentry-trace_id=0eb57706ddf44b79b4126aba47a9826b,sentry-sample_rate=1",
            "cookie": "PHPSESSID=8kih11umha03373dsdg9cfcm4raf1anbbtjsj145djc0nm9ihkt1; cookie_check=0; shop_authenticate=Y; Xtime=1679465643; __cfruid=bfec21dd288ca16d5891ab78b3c22d543f6f9c0f-1679465643; _ga=GA1.1.604851465.1679465649; amp_65bebb=sgxZNhjsNBv7ZBQiH1cQ3k.bnVsbA==..1gs429hnu.1gs43ojnu.c.1.d; _ga_BJ5N3PD9QG=GS1.1.1679468842.2.1.1679470872.60.0.0",
            "referer": "https://www.kurly.com/main",
            "sentry-trace": "0eb57706ddf44b79b4126aba47a9826b-973bbc0b66246190-1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44"
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


        if res.status_code == 200:
            # http status 포함
            datas = res.json()

            result = datas['data']

            ResultList = []

            for i in range(len(datas['data'])) :
                self.cur.execute(InsertList, (str(result[i].get("no")), str(result[i].get("name")), str(result[i].get("sales_price")), str(result[i].get("list_image_url"))))
                self.conn.commit()

                ResultList.append(
                    {
                        "PRODUCT_ID" : str(result[i].get("no")),
                        "PRODUCT_NAME" : str(result[i].get("name")),
                        "SELLER" : "마켓컬리",
                        "PRICE" : str(result[i].get("sales_price")),
                        "OPTION" : " ",
                        "IMAGE" : str(result[i].get("list_image_url")),
                    }
                )

            end = time.time()
            print(f"수행 시간 : {end - start}")
            return ResultList

        else:
            raise HTTPException(status_code=404, detail="잘못된 경로 입니다.")