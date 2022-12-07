import logging
import sys
import time

from collections import Counter

import mysql.connector
from mysql.connector.errors import DatabaseError, InterfaceError

logger = logging.getLogger("proxysql")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

args_list = sys.argv
try:
    HOST = args_list[1]
except IndexError:
    HOST = "192.168.128.2"
try:
    PORT = int(args_list[2])
except IndexError:
    PORT =  6033


USER = "sysbench"
PASS = "sysbench"

hosts = Counter()


def connect(host, port, user, password):
    logger.debug(f"Trying to connect to {user}:{password}@{host}:{port}")
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    return connection


def select_hostname(connection):
    c = connection.cursor()
    c.execute("SELECT @@hostname")
    hostname = c.fetchone()[0]
    return hostname


def main():
    try:
        while True:
            try:
                connection = connect(HOST, PORT, USER, PASS)
            except (DatabaseError, InterfaceError):
                logger.exception("Couldn't connect. Sleeping")
                time.sleep(10)
                continue

            logger.debug(connection)
            hostname = select_hostname(connection)
            hosts[hostname] += 1
            logger.info(f"Hostname: {hostname} : {hosts[hostname]} times")
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info(hosts)

    return 0


if __name__ == "__main__":
    sys.exit(main())
