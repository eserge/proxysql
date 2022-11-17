import sys

import mysql.connector

old_master_host = sys.argv[1]
new_master_host = sys.argv[2]
replica_host = "192.168.96.5"
slavepass = "slavepass"


merch_db_old_master = mysql.connector.connect(
    host=old_master_host,
    port=3306,
    user="root",
    password="secret",
)

merch_db_new_master = mysql.connector.connect(
    host="192.168.96.4",
    port=3306,
    user="root",
    password="secret",
)
merch_db_replica = mysql.connector.connect(
    host=replica_host,
    port=3306,
    user="root",
    password="secret",
)

merch_cursor = merch_db_old_master.cursor()
merch_cursor2 = merch_db_new_master.cursor()
merch_cursor3 = merch_db_replica.cursor()
print('---Starting set up a new master---')
merch_cursor2.execute("STOP SLAVE;")
merch_cursor2.execute("RESET MASTER;")
merch_cursor2.execute(f"CREATE USER repl@'{old_master_host}' IDENTIFIED VIA mysql_native_password USING PASSWORD('{slavepass}');")
merch_cursor2.execute(f"GRANT REPLICATION SLAVE ON *.* TO repl@'{old_master_host}';")
merch_cursor2.execute("FLUSH PRIVILEGES;")
merch_cursor2.execute("FLUSH TABLES WITH READ LOCK;")
merch_cursor2.execute("SET GLOBAL read_only=OFF;")
merch_cursor2.execute("UNLOCK TABLES;")
merch_cursor2.execute("SHOW MASTER status;")
res = merch_cursor2.fetchall()
print('---Master status---')
print(res)
print('---Setting old master to slave status---')
merch_cursor.execute("STOP SLAVE;")
merch_cursor.execute(f"CHANGE MASTER TO MASTER_HOST='{new_master_host}', MASTER_USER='repl', MASTER_PASSWORD='{slavepass}';")
merch_cursor.execute("START SLAVE;")
merch_cursor.execute("FLUSH TABLES WITH READ LOCK;")
merch_cursor.execute("SET GLOBAL read_only=ON;")
merch_cursor.execute("UNLOCK TABLES;")
merch_cursor.execute(r"SHOW SLAVE status;")
res = merch_cursor.fetchall()
print('---Slave status---')
print(res)
print('---Indicating replica to a new master---')
merch_cursor3.execute("STOP SLAVE;")
merch_cursor3.execute(f"CHANGE MASTER TO MASTER_HOST='{new_master_host}', MASTER_USER='repl', MASTER_PASSWORD='{slavepass}';")
merch_cursor3.execute("START SLAVE;")
merch_cursor3.execute(r"SHOW SLAVE status;")
res = merch_cursor3.fetchall()
print('---Slave status---')
print(res)
