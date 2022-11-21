import mysql.connector


db2 = mysql.connector.connect(
    host="192.168.96.2",
    port=6033,
    user="sysbench",
    password="sysbench",
    db="crypto_db"
)

cursor2 = db2.cursor()
cursor2.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255), address VARCHAR(255))")
cursor2.execute("SHOW TABLES")
res2 = cursor2.fetchall()
print(res2)
