#!/usr/bin/env python
import logging
import os
import subprocess
import sys
import time

import mysql.connector

logger = logging.getLogger("proxysql")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


if len(sys.argv) < 3:
    print("proxysql.py [old_master] [new_master] [replica]")
    exit()

# PROXYSQL_HOST = sys.argv[1]
# PROXYSQL_PORT = sys.argv[2]

PROXYSQL_HOST = os.getenv("PROXYSQL_HOST")
PROXYSQL_PORT = os.getenv("PROXYSQL_PORT")
PROXYSQL_USER = "radmin"
PROXYSQL_PASSWORD = "radmin"


OldMaster = sys.argv[1]  # "192.168.128.3"
NewMaster = sys.argv[2]  # "192.168.128.4"
Replica = sys.argv[3]  # "192.168.128.5"
try:
    Switch = sys.argv[4]  # "yes"
except IndexError:
    Switch = "yes"

logger.debug("Arguments: %s, %s, %s, %s", (OldMaster, NewMaster, Replica, Switch))

def proxysql_update_servers(cursor):
    logger.info("MySQL servers to disk and runtime")
    cursor.execute("LOAD MYSQL SERVERS TO RUNTIME;")
    cursor.execute("SAVE MYSQL SERVERS TO DISK;")


logger.info(
    "Trying to connect to ProxySQL admin on"
    f" {PROXYSQL_USER}:{PROXYSQL_PASSWORD}@{PROXYSQL_HOST}:{PROXYSQL_PORT}"
)
proxysql = mysql.connector.connect(
    host=PROXYSQL_HOST,
    port=PROXYSQL_PORT,
    user=PROXYSQL_USER,
    password=PROXYSQL_PASSWORD,
)
logger.debug(proxysql)

ps_cursor = proxysql.cursor()
ps_cursor.execute("SELECT * FROM mysql_servers;")
logger.debug(ps_cursor.fetchall())

logger.info("Change read-write status for old master")
logger.info("Setting master status OFFLINE_SOFT")
sql = "UPDATE mysql_servers SET status='OFFLINE_SOFT' WHERE hostname='%(hostname)s'" % {'hostname': OldMaster}
logger.debug(sql)
ps_cursor.execute(sql)
proxysql_update_servers(ps_cursor)
# exit()

time.sleep(1)
logger.info("Here python script changes master and slave")
# run python switch_master.py $OldMaster $NewMaster $Replica
# subprocess.run(["python", "switch_master.py", OldMaster, NewMaster, Replica])
logger.info("Python script is finished working")

logger.info("Delete write old master")
sql = "DELETE FROM mysql_servers where hostgroup_id=0 and hostname='%(hostname)s'" % {'hostname': OldMaster}
logger.debug(sql)
ps_cursor.execute(sql)
proxysql_update_servers(ps_cursor)



time.sleep(1)
logger.info("Change status read old master")
if Switch == "yes":
    logger.info("Setting master status ONLINE")
    sql = "UPDATE mysql_servers SET status='ONLINE' WHERE hostgroup_id=1 AND hostname='%(hostname)s'" % {'hostname': OldMaster}
    logger.debug(sql)
    ps_cursor.execute(sql)
else:
    logger.info("Setting master status SHUNNED")
    sql = "UPDATE mysql_servers SET status='SHUNNED' WHERE hostgroup_id=1 AND hostname='%(hostname)s'" % {'hostname': OldMaster}
    logger.debug(sql)
    ps_cursor.execute(sql)
proxysql_update_servers(ps_cursor)

ps_cursor.execute("SELECT * FROM mysql_servers;")
logger.info(ps_cursor.fetchall())






# sleep 1
# echo "Change status read old master"
# if [[ $Switch = "yes" ]]; then
#   echo "Setting master status ONLINE"
#   docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "UPDATE mysql_servers SET status='ONLINE' WHERE hostgroup_id=1 AND hostname=\"$OldMaster\";"
# else
# echo "Setting master status SHUNNED"
#   docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "UPDATE mysql_servers SET status='SHUNNED' WHERE hostgroup_id=1 AND hostname=\"$OldMaster\";"
# fi
# docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "LOAD MYSQL SERVERS TO RUNTIME;"
# docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "SAVE MYSQL SERVERS TO DISK;"

# sleep 1
# echo "---New tables---"
# docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "SELECT * from mysql_servers;"
