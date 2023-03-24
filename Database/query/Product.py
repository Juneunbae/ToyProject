DeleteList = """
    DELETE FROM CHECKBOX.Product WHERE Shop = 'MarketKurly';
"""

InsertList = """
    INSERT INTO Product
    (ProductId, ProductName, Price, Seller, Picture, Shop, Created) 
    VALUES
    (%s, %s, %s, "마켓컬리", %s, "MarketKurly", Now())
"""

SelectDetail = """
    SELECT * FROM CHECKBOX.Product WHERE Shop = 'MarketKurly';
"""