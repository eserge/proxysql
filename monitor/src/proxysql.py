#!/usr/bin/env python
import logging
import json
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


old_master = sys.argv[1]  # "192.168.128.3"
new_master = sys.argv[2]  # "192.168.128.4"
replica = sys.argv[3]  # "192.168.128.5"
try:
    sys.argv[4]  # "no" or any other value
    is_switchover = True
except IndexError:
    is_switchover = False

SLEEP_TIME = 5.0


logger.debug("Arguments: %s, %s, %s, %s", old_master, new_master, replica, is_switchover)


def proxysql_update_servers(cursor):
    logger.info("MySQL servers to disk and runtime")
    cursor.execute("LOAD MYSQL SERVERS TO RUNTIME;")
    cursor.execute("SAVE MYSQL SERVERS TO DISK;")


def get_conn(dry_run=False):
    if dry_run:
        class FakeCursor:
            def execute(*args, **kwargs):
                return

            def fetchall(*args, **kwargs):
                return []

        return FakeCursor()

    logger.info(
        "Trying to connect to ProxySQL admin on"
        f" {PROXYSQL_USER}:{PROXYSQL_PASSWORD}@{PROXYSQL_HOST}:{PROXYSQL_PORT}"
    )
    ps_connection = mysql.connector.connect(
        host=PROXYSQL_HOST,
        port=PROXYSQL_PORT,
        user=PROXYSQL_USER,
        password=PROXYSQL_PASSWORD,
    )
    logger.debug(ps_connection)
    return ps_connection


def put_to_offline_soft(hostname, connection):
    cursor = connection.cursor()
    logger.info("Change read-write status for old master")
    logger.info("Setting master status OFFLINE_SOFT")
    sql = "UPDATE mysql_servers SET status='OFFLINE_SOFT' WHERE hostname='%(hostname)s'" % {'hostname': hostname}
    logger.debug(sql)
    cursor.execute(sql)
    proxysql_update_servers(cursor)
    time.sleep(SLEEP_TIME)


def reconfiure_replication():
    # time.sleep(SLEEP_TIME)
    logger.info("Here python script changes master and slave")
    # run python switch_master.py $OldMaster $NewMaster $Replica
    subprocess.run(["python", "switch_master.py", old_master, new_master, replica])
    logger.info("Python script has finished working")


def delete_old_master(hostname, connection, is_switchover):
    cursor = connection.cursor()
    logger.info("Delete write old master")
    if is_switchover:
        sql = "DELETE FROM mysql_servers WHERE hostgroup_id=0 AND hostname='%(hostname)s'" % {'hostname': hostname}
    else:  # consider it a failover
        sql = "DELETE FROM mysql_servers WHERE hostname='%(hostname)s'" % {'hostname': hostname}

    logger.debug(sql)
    cursor.execute(sql)
    proxysql_update_servers(cursor)
    time.sleep(SLEEP_TIME)


def set_new_master(hostname, connection):
    cursor = connection.cursor()
    logger.info("Add new master")
    sql = (
        "INSERT INTO mysql_servers (hostgroup_id, hostname, port, status, weight) VALUES (0, '%(hostname)s', 3306, 'ONLINE', 1000)" % {
            'hostname': hostname,
        }
    )
    logger.debug(sql)
    cursor.execute(sql)
    # proxysql_update_servers(cursor)
    time.sleep(SLEEP_TIME)


def old_master_for_reading(hostname, connection, is_switchover):
    cursor = connection.cursor()
    logger.info("Change status read old master")
    if is_switchover:
        logger.info("Setting master status ONLINE")
        sql = "UPDATE mysql_servers SET status='ONLINE' WHERE hostgroup_id=1 AND hostname='%(hostname)s'" % {'hostname': hostname}
        logger.debug(sql)
    else:
        logger.info("Setting master status SHUNNED")
        sql = "UPDATE mysql_servers SET status='SHUNNED' WHERE hostgroup_id=1 AND hostname='%(hostname)s'" % {'hostname': hostname}
        logger.debug(sql)
    cursor.execute(sql)
    proxysql_update_servers(cursor)
    time.sleep(SLEEP_TIME)


def main():
    ps_connection = get_conn(dry_run=False)
    ps_cursor = ps_connection.cursor()
    ps_cursor.execute("SELECT * FROM mysql_servers;")
    logger.info(ps_cursor.fetchall())

    put_to_offline_soft(old_master, ps_connection)
    reconfiure_replication()
    delete_old_master(old_master, ps_connection, is_switchover)
    old_master_for_reading(old_master, ps_connection, is_switchover)
    set_new_master(new_master, ps_connection)



if __name__ == "__main__":
    sys.exit(main())
