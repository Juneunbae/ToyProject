DeleteList = """
    DELETE FROM CHECKBOX.Product WHERE Shop = 'MarketKurly';
"""

InsertList = """
    INSERT INTO Product
    (PRODUCT_ID, PRODUCT_NAME, PRICE, SELLER, IMAGE, SHOP, CREATED) 
    VALUES
    (%s, %s, %s, "마켓컬리", %s, "MarketKurly", Now())
"""

SelectDetail = """
    SELECT * FROM CHECKBOX.Product WHERE Shop = 'MarketKurly';
"""