echo "Stop ProxySQL"
docker-compose -f proxy_sql_merch/docker-compose.yml stop
echo "Stop merchant master DB"
docker-compose -f merchant_db_master/docker-compose.yml stop
echo "Stop merchant slave1 DB"
docker-compose -f merchant_db_slave1/docker-compose.yml stop
echo "Stop merchant slave2 DB"
docker-compose -f merchant_db_slave2/docker-compose.yml stop
echo "Removing merchant-network"
docker network rm merchant-network
echo "---Removing ProxySQL"
docker-compose -f proxy_sql_merch/docker-compose.yml down -v
echo "---Removing merchant master DB"
docker-compose -f merchant_db_master/docker-compose.yml down -v
echo "---Removing merchant slave1 DB"
docker-compose -f merchant_db_slave1/docker-compose.yml down -v
echo "---Removing merchant slave2 DB"
docker-compose -f merchant_db_slave2/docker-compose.yml down -v
