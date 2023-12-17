import sqlite3

conn = sqlite3.connect('data_mvideo.db')

sql = "CREATE TABLE iphone(name TEXT, price TEXT, url TEXT, screen TEXT, tech TEXT, proc TEXT)"
sql = "SELECT * FROM iphone"
cur = conn.cursor()

cur.execute(sql)

res = cur.fetchall()
conn.close()