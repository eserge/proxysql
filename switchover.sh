#!/bin/sh

OldMaster=$1
NewMaster=$2

echo "Change status old master"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "UPDATE mysql_servers SET status='OFFLINE_SOFT' WHERE hostname=\"$OldMaster\";"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "LOAD MYSQL SERVERS TO RUNTIME;"

sleep 1
echo "Here python script changes master and slave"
python switch_master.py $OldMaster $NewMaster

sleep 1
echo "Delete write old master"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "DELETE FROM mysql_servers where hostgroup_id=0 and hostname=\"$OldMaster\";"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "LOAD MYSQL SERVERS TO RUNTIME;"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "SAVE MYSQL SERVERS TO DISK;"
sleep 1
echo "Change status read old master"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "UPDATE mysql_servers SET status='ONLINE' WHERE hostgroup_id=1 AND hostname=\"$OldMaster\";"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "LOAD MYSQL SERVERS TO RUNTIME;"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "SAVE MYSQL SERVERS TO DISK;"
sleep 1
echo "---New tables---"
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 -e "SELECT * from mysql_servers;"
