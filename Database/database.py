import pymysql

def Connect() :
    conn = pymysql.connect(

    )
    return conn
