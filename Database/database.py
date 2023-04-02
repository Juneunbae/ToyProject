import pymysql

def Connect() :
    conn = pymysql.connect(
        host='3.37.57.131',
        user = 'anasa',
        password='anasa@1',
        db='CHECKBOX',
        port=3306,
        charset='utf8'
    )
    return conn
