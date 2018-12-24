import MySQLdb

conn = MySQLdb.connect("localhost", "butler", "Zer045kin!", "agc_butler")
cursor = conn.cursor()

cursor.execute("SHOW TABLES")
data=cursor.fetchone()

print(data)