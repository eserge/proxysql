import subprocess
from time import sleep
import os

import mysql.connector
from mysql.connector.errors import DatabaseError
from dotenv import load_dotenv

load_dotenv()


check_host = '192.168.128.3'
new_master = '192.168.128.4'
replica = '192.168.128.5'
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


def ping(check_host, new_master, replica):
    while True:
        try:
            mysql.connector.connect(
                host=check_host,
                port=db_port,
                user=db_user,
                password=db_password,
            )
        except DatabaseError:
            print("Oops, master is dead, switching to another DB.")
            subprocess.run(['./switchover.sh', check_host, new_master, replica])
            break
        else:
            print('It is OK till now!')
            sleep(5)


if __name__ == '__main__':
    print(os.environ)
    ping(check_host, new_master, replica)
