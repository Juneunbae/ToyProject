import pymysql

def Connect() :
    # conn = pymysql.connect(host = f"{DB['host']}", user = f"{DB['user']}", password=f"{DB['password']}", db=f"{DB['database']}", charset='utf8')
    conn = pymysql.connect(

    )
    # cur = conn.cursor()
    return conn
