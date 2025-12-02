import pymysql


class Config:
    DB_HOST = "trolley.proxy.rlwy.net"
    DB_PORT = 43980
    DB_USER = "root"
    DB_PASSWORD = "dNhGVaRJlttKciMpQQhmJNsXyAhBeMos"
    DB_NAME = "railway"



def get_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
