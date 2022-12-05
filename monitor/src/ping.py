#!/usr/bin/env python
import subprocess
import sys
from time import sleep
import os

import mysql.connector
from mysql.connector.errors import DatabaseError, InterfaceError

CONNECTION_TIMEOUT = float(os.getenv("CONNECTION_TIMEOUT", 3.0))


def ping(user, password, port, current_master, new_master, replica):
    print(f"Trying to connect to {user}:{password}@{current_master}:{db_port}")
    while True:
        try:
            sys.stdout.write("Connecting... ")
            mysql.connector.connect(
                host=current_master,
                port=port,
                user=user,
                password=password,
                connection_timeout=CONNECTION_TIMEOUT,
            )
        except (DatabaseError, InterfaceError):
            sys.stdout.write("Oops, master is dead, switching to another DB.\n")
            sys.stdout.flush()
            subprocess.run(["./proxysql.py", current_master, new_master, replica])
            break
        else:
            sys.stdout.write("It is OK till now!\n")
            sys.stdout.flush()
            sleep(5)


if __name__ == "__main__":
    args_list = sys.argv

    if len(args_list) > 1 and args_list[1] == "-h":
        print("ping.py [current_master_host] [next_master_host] [replica_host]")
        exit()

    try:
        current_master = args_list[1]
    except IndexError:
        current_master = "192.168.128.3"

    try:
        new_master = args_list[2]
    except IndexError:
        new_master = "192.168.128.4"

    try:
        second_replica = args_list[3]
    except IndexError:
        second_replica = "192.168.128.5"

    db_port = os.getenv("DB_PORT", 3306)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    print("Starting ping.py")

    # print(os.environ)
    ping(db_user, db_password, db_port, current_master, new_master, second_replica)
