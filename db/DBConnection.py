import pymysql

db = pymysql.connect("127.0.0.1", "root", "impossble", "DATA")
cursor = db.cursor()
