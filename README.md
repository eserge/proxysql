
## Activate python libs
```bash
source venv/bin/activate
pip install -r requirements.txt
```
## run db containers
```bash
./run.sh
```
## enter to the master DB shell
```bash
docker exec -it db-master-fwd mysql -uroot -psecret app_db
docker exec -it db-master-merch mysql -uroot -psecret crypto_db
```
The same for slave1 and slave2


## stop db containers
```bash
./down.sh
```

## Enter to proxymysql dbshell
```bash
docker exec -it proxysql-fwd mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
docker exec -it proxysql-merch mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
```

## Switch between DB nodes
```bash
./switchover.sh 192.168.96.3 192.168.96.4 192.168.96.5 yes
```
## Ping DB
```bash
python ping.py
```
Then stop DB container
