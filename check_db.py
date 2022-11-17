import mysql.connector


# db = mysql.connector.connect(
#     host="192.168.128.2",
#     port=6033,
#     user="sysbench",
#     password="sysbench",
#     db="app_db"
# )

# cursor = db.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255), address VARCHAR(255))")
# cursor.execute("SHOW TABLES")
# res = cursor.fetchall()
# cursor.close()
# print(res)

db2 = mysql.connector.connect(
    host="192.168.96.2",
    port=6033,
    # port=3306,
    user="sysbench",
    # user="root",
    password="sysbench",
    # password="secret",
    db="crypto_db"
)
cursor2 = db2.cursor()
# cursor2.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255), address VARCHAR(255))")
cursor2.execute("CREATE TABLE IF NOT EXISTS customers2 (name VARCHAR(255), address VARCHAR(255))")
cursor2.execute("SHOW TABLES")
res2 = cursor2.fetchall()
print(res2)
