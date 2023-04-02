InsertList = """
    INSERT INTO Products
    (PRODUCT_ID, PRODUCT_NAME, PRICE, SELLER, IMAGE, SHOP, CREATED) 
    VALUES
    (%s, %s, %s, "마켓컬리", %s, "Kurly", Now())
    ON DUPLICATE KEY UPDATE 
    PRODUCT_NAME = %s, PRICE = %s, SELLER = "마켓컬리", IMAGE = %s, SHOP = "Kurly", UPDATED = NOW();
"""

InsertLog = """
    INSERT INTO LOG (CONTENT, RECIPIENT, SENDER, PRODUCT_ID, PRODUCT_NAME, CREATED)
                VALUES (%s, NULL, "Discord", %s, %s, NOW());
"""

InsertNoLog = """
    INSERT INTO LOG (CONTENT, RECIPIENT, SENDER, PRODUCT_ID, PRODUCT_NAME, CREATED)
                VALUES (%s, NULL, "Discord", NULL, NULL, NOW());
"""

INSERTLog_HP = f"""
    INSERT INTO LOG (CONTENT, RECIPIENT, SENDER, PRODUCT_ID, PRODUCT_NAME, CREATED)
    VALUES ("DB X, 홈페이지 내 조회 성공", NULL, "Discord", NULL, %s, NOW())
"""