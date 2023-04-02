from math import prod
from fastapi import HTTPException

import requests

from Database.database import Connect
from Database.query.Product import InsertList, InsertLog, InsertNoLog, INSERTLog_HP
from Kurly import Kurly
from webhook import Webhook_basic, Webhook_embed

from datetime import datetime

import time


class MarketKurly :
    def __init__(self):
        self.conn = Connect()
        self.cur = self.conn.cursor()

    def Detail(self, item_num, product_name):
        start = time.time()

        i = item_num - 1
        
        PRO_NAME = product_name

        self.cur.execute(
            f"""
                SELECT *
                FROM CHECKBOX.Products
                WHERE Shop = 'Kurly' AND PRODUCT_NAME LIKE '%{PRO_NAME}%';
            """
        )
        # product_id 검색
        result = self.cur.fetchall()
        
        # DB 내 검색 결과가 있을 경우, DB 내 검색 결과 반환
        if len(result) >= 1 :
            PRODUCT_ID = result[i][0]
            PRODUCT_NAME = result[i][1]
            PRICE = result[i][2]
            SELLER = result[i][3]
            IMAGE = result[i][4]
            SHOP = result[i][5]
            Created = result[i][6]
            # item_num으로 인덱스 파싱 완료

            DetailData = [{
                "PRODUCT_ID" : PRODUCT_ID,
                "PRODUCT_NAME" : PRODUCT_NAME,
                "PRICE" : PRICE,
                "SELLER" : SELLER,
                "OPTION" : " ",
                "IMAGE" : IMAGE,
                # "Shop" : SHOP,
                "Created" : Created,
            }]
            print(DetailData)
            end = time.time()

            print(f"수행 시간 : {end - start}")

            self.cur.execute(InsertLog, (f"'{PRODUCT_NAME} 조회 성공", PRODUCT_ID, PRODUCT_NAME))
            self.conn.commit()

            msg = f"""
                \n
                상품 ID : {PRODUCT_ID}
                \n
                [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
            """

            set_url = f"https://www.kurly.com/goods/{PRODUCT_ID}"

            Webhook_embed(title = f"{PRODUCT_NAME}", description = msg, thumbnail_image = IMAGE, set_url=set_url)

            return DetailData

        # DB 내 검색 결과가 없고, 홈페이지 내 검색 결과가 있을 경우 상품 5개 반환
        elif len(result) == 0 :
            Webhook_basic(f"홈페이지 검색 시도....")
            try :
                KurlyResult = Kurly(product_name)
                
                for z in range(0, 5) :
                    KurlyResult_PRO_ID = KurlyResult[z].get("PRODUCT_ID")
                    KurlyResult_PRO_NAME = KurlyResult[z].get("PRODUCT_NAME")
                    KurlyResult_PRO_IMAGE = KurlyResult[z].get("IMAGE")
                    
                    self.cur.execute(
                        f"""
                            INSERT INTO LOG (CONTENT, RECIPIENT, SENDER, PRODUCT_ID, PRODUCT_NAME, CREATED)
                            VALUES ("DB X, 홈페이지 내 {product_name} 조회 성공", NULL, "Discord", %s, %s, NOW())
                        """, (KurlyResult_PRO_ID, KurlyResult_PRO_NAME))
                    
                    self.conn.commit()
                    
                    KurlyMSG = f"""
                        \n
                        상품 ID : {KurlyResult_PRO_ID}
                        \n
                        [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
                    """
                    
                    set_url = f"https://www.kurly.com/goods/{KurlyResult_PRO_ID}"
                    
                    Webhook_embed(title = f"{KurlyResult_PRO_NAME}", description = KurlyMSG, thumbnail_image = KurlyResult_PRO_IMAGE, set_url=set_url)
                
                Webhook_basic(f"홈페이지 검색 완료")
                return KurlyResult
            
            # DB + 홈페이지 모두 검색 결과가 없을 경우
            except :
                self.cur.execute(InsertNoLog, "조회 실패")
                self.conn.commit()

                msg = "검색결과가 없습니다. 조회를 실패하였습니다."

                Webhook_embed(title="조회 실패 알림", description=msg, thumbnail_image='', set_url = None)

                raise HTTPException(status_code=404, detail="검색결과가 없습니다.")


    def Search(self, product_name, page_num):
        start = time.time()

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
        Webhook_basic(f"{product_name} 검색 시도..")

        res = requests.get(url, headers=header, json=data)

        if res.status_code == 200:
            # http status 포함
            datas = res.json()

            result = datas['data']

            ResultList = []

            for i in range(len(datas['data'])) :
                self.cur.execute(InsertList, (str(result[i].get("no")), str(result[i].get("name")), str(result[i].get("sales_price")), str(result[i].get("list_image_url")), \
                                              str(result[i].get("name")), str(result[i].get("sales_price")), str(result[i].get("list_image_url"))))
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

            Webhook_basic(f"{product_name} 검색 완료")

            end = time.time()
            print(f"수행 시간 : {end - start}")
            return ResultList

        else:
            Webhook_basic(f"{product_name} 검색 실패")
            raise HTTPException(status_code=404, detail="잘못된 경로 입니다.")