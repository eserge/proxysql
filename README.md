

# run db containers
```bash
./run.sh
```
## enter to the master DB shell
```bash
docker exec -it db-master mysql -uroot -psecret
```

## stop db containers
```bash
./down-db.sh
```

## Enter to proxymysql dbshell
```bash
docker exec -it proxysql mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
```


## Configure Backends
```sql
INSERT INTO mysql_servers(hostgroup_id,hostname,port) VALUES (0,'192.168.128.3',3306);
INSERT INTO mysql_servers(hostgroup_id,hostname,port) VALUES (1,'192.168.128.4',3306);
INSERT INTO mysql_servers(hostgroup_id,hostname,port) VALUES (1,'192.168.128.5',3306);
INSERT INTO  mysql_replication_hostgroups VALUES (0,1,'read_only','production');
UPDATE mysql_servers SET weight=200 WHERE hostgroup_id=1 AND hostname='%';
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```
## Configure user
```sql
UPDATE global_variables SET variable_value='monitor' WHERE variable_name='mysql-monitor_password';
LOAD MYSQL VARIABLES TO RUNTIME;
SAVE MYSQL VARIABLES TO DISK;
```
## Configure monitoring
```sql
UPDATE global_variables SET variable_value=2000 WHERE variable_name IN ('mysql-monitor_connect_interval','mysql-monitor_ping_interval','mysql-monitor_read_only_interval');
UPDATE global_variables SET variable_value = 1000 where variable_name = 'mysql-monitor_connect_timeout';
UPDATE global_variables SET variable_value = 500 where variable_name = 'mysql-monitor_ping_timeout';
LOAD MYSQL VARIABLES TO RUNTIME;
SAVE MYSQL VARIABLES TO DISK;
```
## Configure Query Rules
```sql
INSERT INTO mysql_query_rules (active, match_digest, destination_hostgroup, apply) VALUES (1, '^SELECT.*', 1, 0);
INSERT INTO mysql_query_rules (active, match_digest, destination_hostgroup, apply) VALUES (1, '^SELECT.*FOR UPDATE', 0, 1);
LOAD MYSQL QUERY RULES TO RUNTIME;
SAVE MYSQL QUERY RULES TO DISK;
```