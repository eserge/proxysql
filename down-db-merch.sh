# echo "Stop ProxySQL"
# docker-compose -f proxy_sql/docker-compose.yml stop
# echo "Stop forwarder master DB"
# docker-compose -f forwarder_db_master/docker-compose.yml stop
# echo "Stop forwarder slave1 DB"
# docker-compose -f forwarder_db_slave1/docker-compose.yml stop
# echo "Stop forwarder slave2 DB"
# docker-compose -f forwarder_db_slave2/docker-compose.yml stop
# echo "Removing network"
# docker network rm crypto-network
echo "---Removing ProxySQL"
docker compose -f proxy_sql_merch/docker-compose.yml down -v
echo "---Removing merchant master DB"
docker compose -f merchant_db_master/docker-compose.yml down -v
echo "---Removing merchant slave1 DB"
docker compose -f merchant_db_slave1/docker-compose.yml down -v
echo "---Removing merchant slave2 DB"
docker compose -f merchant_db_slave2/docker-compose.yml down -v
