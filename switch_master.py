import sys

import mysql.connector
from mysql.connector.errors import DatabaseError

old_master_host = sys.argv[1]
new_master_host = sys.argv[2]
replica_host = "192.168.96.5"
slavepass = "slavepass"
db_user = "root"
db_pass = "secret"
db_port = 3306


def connect_db(host, port, user, password):
    db = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    return db


try:
    db_old_master = connect_db(old_master_host, db_port, db_user, db_pass)
except DatabaseError:
    print('---Master is dead---')
else:
    cursor = db_old_master.cursor()
    print('---Setting old master to slave status---')
    cursor.execute("STOP SLAVE;")
    cursor.execute(f"CHANGE MASTER TO MASTER_HOST='{new_master_host}', MASTER_USER='repl', MASTER_PASSWORD='{slavepass}';")
    cursor.execute("START SLAVE;")
    cursor.execute("FLUSH TABLES WITH READ LOCK;")
    cursor.execute("SET GLOBAL read_only=ON;")
    cursor.execute("UNLOCK TABLES;")
    cursor.execute(r"SHOW SLAVE status;")
    res = cursor.fetchall()
    print('---Slave status---')
    print(res)


db_new_master = connect_db(new_master_host, db_port, db_user, db_pass)
db_replica = connect_db(replica_host, db_port, db_user, db_pass)


cursor2 = db_new_master.cursor()
cursor3 = db_replica.cursor()
print('---Starting set up a new master---')
cursor2.execute("STOP SLAVE;")
cursor2.execute("RESET MASTER;")
cursor2.execute(f"CREATE USER repl@'{old_master_host}' IDENTIFIED VIA mysql_native_password USING PASSWORD('{slavepass}');")
cursor2.execute(f"GRANT REPLICATION SLAVE ON *.* TO repl@'{old_master_host}';")
cursor2.execute("FLUSH PRIVILEGES;")
cursor2.execute("FLUSH TABLES WITH READ LOCK;")
cursor2.execute("SET GLOBAL read_only=OFF;")
cursor2.execute("UNLOCK TABLES;")
cursor2.execute("SHOW MASTER status;")
res = cursor2.fetchall()
print('---Master status---')
print(res)
print('---Indicating replica to a new master---')
cursor3.execute("STOP SLAVE;")
cursor3.execute(f"CHANGE MASTER TO MASTER_HOST='{new_master_host}', MASTER_USER='repl', MASTER_PASSWORD='{slavepass}';")
cursor3.execute("START SLAVE;")
cursor3.execute(r"SHOW SLAVE status;")
res = cursor3.fetchall()
print('---Slave status---')
print(res)
