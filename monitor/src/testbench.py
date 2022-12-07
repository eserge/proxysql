import logging
import sys
import time

import mysql.connector
from mysql.connector.errors import DatabaseError, InterfaceError

logger = logging.getLogger("proxysql")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

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
    while True:
        try:
            connection = connect(HOST, PORT, USER, PASS)
        except (DatabaseError, InterfaceError):
            logger.exception("Couldn't connect")
            return 1
        logger.info(connection)

        hostname = select_hostname(connection)
        print(hostname)
        time.sleep(0.5)

    return 0


if __name__ == "__main__":
    sys.exit(main())
