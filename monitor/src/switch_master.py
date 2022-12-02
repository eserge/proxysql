import sys
import os

import mysql.connector
from mysql.connector.errors import DatabaseError, InterfaceError
from dotenv import load_dotenv

load_dotenv()

old_master_host = sys.argv[1]
new_master_host = sys.argv[2]
replica_host = sys.argv[3]
slavepass = os.getenv('SLAVEPASS')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')

# Minimal timeout make switchover faster
# If we are in this script, DB should be dead anyway
CONNECTION_TIMEOUT = 0.5


def connect_db(host, port, user, password):
    db = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    return db


try:
    db_old_master = connect_db(old_master_host, db_port, db_user, db_pass, connection_timeout=CONNECTION_TIMEOUT)
except (DatabaseError, InterfaceError):
    print('---Master is dead---')
else:
    cursor_old_master = db_old_master.cursor()
    print('---Setting old master to slave status---')
    cursor_old_master.execute("STOP SLAVE;")
    cursor_old_master.execute(f"CHANGE MASTER TO MASTER_HOST='{new_master_host}', MASTER_USER='repl', MASTER_PASSWORD='{slavepass}';")
    cursor_old_master.execute("START SLAVE;")
    cursor_old_master.execute("FLUSH TABLES WITH READ LOCK;")
    cursor_old_master.execute("SET GLOBAL read_only=ON;")
    cursor_old_master.execute("UNLOCK TABLES;")
    cursor_old_master.execute(r"SHOW SLAVE status;")
    res = cursor_old_master.fetchall()
    print('---Slave status---')
    print(res)


db_new_master = connect_db(new_master_host, db_port, db_user, db_pass)
db_replica = connect_db(replica_host, db_port, db_user, db_pass)


cursor_new_master = db_new_master.cursor()
cursor_replica = db_replica.cursor()
print('---Starting set up a new master---')
cursor_new_master.execute("STOP SLAVE;")
cursor_new_master.execute("RESET MASTER;")
cursor_new_master.execute(f"CREATE USER repl@'{old_master_host}' IDENTIFIED VIA mysql_native_password USING PASSWORD('{slavepass}');")
cursor_new_master.execute(f"GRANT REPLICATION SLAVE ON *.* TO repl@'{old_master_host}';")
cursor_new_master.execute("FLUSH PRIVILEGES;")
cursor_new_master.execute("FLUSH TABLES WITH READ LOCK;")
cursor_new_master.execute("SET GLOBAL read_only=OFF;")
cursor_new_master.execute("UNLOCK TABLES;")
cursor_new_master.execute("SHOW MASTER status;")
res = cursor_new_master.fetchall()
print('---Master status---')
print(res)
print('---Indicating replica to a new master---')
cursor_replica.execute("STOP SLAVE;")
cursor_replica.execute(f"CHANGE MASTER TO MASTER_HOST='{new_master_host}', MASTER_USER='repl', MASTER_PASSWORD='{slavepass}';")
cursor_replica.execute("START SLAVE;")
cursor_replica.execute(r"SHOW SLAVE status;")
res = cursor_replica.fetchall()
print('---Slave status---')
print(res)
