#!/usr/bin/env python
import sys
import mysql.connector

args_list = sys.argv

try:
    HOST = args_list[1]
except IndexError:
    HOST = "192.168.96.2"
try:
    PORT = int(args_list[2])
except IndexError:
    PORT =  6033
try:
    USER = args_list[3]
except IndexError:
    USER = "sysbench"
try:
    PASSWORD = args_list[4]
except IndexError:
    PASSWORD = "sysbench"
try:
    DB = args_list[5]
except IndexError:
    DB = "sysbench"


print(f"Trying to connect to {USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
db2 = mysql.connector.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    db=DB,
)

cursor2 = db2.cursor()
cursor2.execute("SHOW TABLES")
res2 = cursor2.fetchall()
print(res2)
