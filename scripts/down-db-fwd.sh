echo "Stop ProxySQL"
docker-compose -f proxy_sql_fwd/docker-compose.yml stop
echo "Stop forwarder master DB"
docker-compose -f forwarder_db_master/docker-compose.yml stop
echo "Stop forwarder slave1 DB"
docker-compose -f forwarder_db_slave1/docker-compose.yml stop
echo "Stop forwarder slave2 DB"
docker-compose -f forwarder_db_slave2/docker-compose.yml stop
echo "Removing forwarder-network"
docker network rm forwarder-network
echo "---Removing forwarder master DB"
docker-compose -f forwarder_db_master/docker-compose.yml down -v
echo "---Removing forwarder slave1 DB"
docker-compose -f forwarder_db_slave1/docker-compose.yml down -v
echo "---Removing forwarder slave2 DB"
docker-compose -f forwarder_db_slave2/docker-compose.yml down -v
echo "Removing forwarder ProxySQL"
docker-compose -f proxy_sql_fwd/docker-compose.yml down -v
