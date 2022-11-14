

# run db containers
```bash
./run-fwd.sh
./run-merch.sh
```
## enter to the master DB shell
```bash
docker exec -it db-master-fwd mysql -uroot -psecret app_db
docker exec -it db-master-merch mysql -uroot -psecret crypto_db
```
The same for slave1 and slave2


## stop db containers
```bash
./down-db-fwd.sh
./down-db-merch.sh
```

## Enter to proxymysql dbshell
```bash
docker exec -it proxysql-fwd mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
```