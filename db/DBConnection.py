import pymysql

db = pymysql.connect("192.168.1.6", "root", "impossble", "DATA")
cursor = db.cursor()
