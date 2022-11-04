echo "---Starting forwarder master DB"
docker-compose -f forwarder_db_master/docker-compose.yml up --build -d
echo "---Starting forwarder slave1 DB"
docker-compose -f forwarder_db_slave1/docker-compose.yml up --build -d
echo "---Starting forwarder slave2 DB"
docker-compose -f forwarder_db_slave2/docker-compose.yml up --build -d
echo "---Starting proxysql"
docker-compose -f proxy_sql/docker-compose.yml up --build -d
echo "---Checking status all services"
docker ps