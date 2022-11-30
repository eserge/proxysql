import sys
import mysql.connector

args_list = sys.argv

try:
    HOST = args_list[1]
except IndexError:
    HOST = "192.168.96.2"
try:
    PORT = args_list[2]
except IndexError:
    PORT =  6033


db2 = mysql.connector.connect(
    host=HOST,
    port=PORT,
    user="sysbench",
    password="sysbench",
    db="crypto_db"
)

cursor2 = db2.cursor()
cursor2.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255), address VARCHAR(255))")
cursor2.execute("SHOW TABLES")
res2 = cursor2.fetchall()
print(res2)
