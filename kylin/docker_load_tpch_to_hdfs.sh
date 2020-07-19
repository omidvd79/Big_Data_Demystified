echo "docker name is :"+$1

sudo docker cp  /home/kylin/tpch-dbgen/lineitem.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/nation.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/region.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/part.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/supplier.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/customer.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/orders.tbl  $1:/home/admin

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/lineitem/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/nation/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/region/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/part/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/supplier/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/customer/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/orders/



docker exec -it $1 hadoop fs -put /home/admin/lineitem.tbl /user/hive/warehouse/tpch/lineitem/

docker exec -it $1 hadoop fs -put /home/admin/nation.tbl /user/hive/warehouse/tpch/nation/

docker exec -it $1 hadoop fs -put /home/admin/region.tbl /user/hive/warehouse/tpch/region/

docker exec -it $1 hadoop fs -put /home/admin/part.tbl /user/hive/warehouse/tpch/part/

docker exec -it $1 hadoop fs -put /home/admin/supplier.tbl /user/hive/warehouse/tpch/supplier/

docker exec -it $1 hadoop fs -put /home/admin/customer.tbl /user/hive/warehouse/tpch/customer/

docker exec -it $1 hadoop fs -put /home/admin/orders.tbl /user/hive/warehouse/tpch/orders/


