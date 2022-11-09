echo "---Starting merchant master DB"
docker compose -f merchant_db_master/docker-compose.yml up --build -d
echo "---Starting merchant slave1 DB"
docker compose -f merchant_db_slave1/docker-compose.yml up --build -d
echo "---Starting merchant slave2 DB"
docker compose -f merchant_db_slave2/docker-compose.yml up --build -d
echo "---Starting proxysql"
docker compose -f proxy_sql_merch/docker-compose.yml up --build -d
echo "---Checking status all services"
docker ps