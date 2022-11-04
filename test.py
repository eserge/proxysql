import mysql.connector


db = mysql.connector.connect(
    host="192.168.128.2",
    port=6033,
    user="sysbench",
    password="sysbench",
    db="app_db"
)

cursor = db.cursor()

# cursor.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255), address VARCHAR(255))")

cursor.execute("SHOW TABLES")

res = cursor.fetchall()

print(res)
