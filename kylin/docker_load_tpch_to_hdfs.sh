echo "docker name is :"+$1

#copy files from host to docker
sudo docker cp  /home/kylin/tpch-dbgen/lineitem.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/nation.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/region.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/part.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/supplier.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/customer.tbl  $1:/home/admin
sudo docker cp  /home/kylin/tpch-dbgen/orders.tbl  $1:/home/admin

#create folder in HDFS
docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/lineitem/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/nation/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/region/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/part/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/supplier/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/customer/

docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/orders/


# copy files to HDFS
docker exec -it $1 hadoop fs -put /home/admin/lineitem.tbl /user/hive/warehouse/tpch/lineitem/

docker exec -it $1 hadoop fs -put /home/admin/nation.tbl /user/hive/warehouse/tpch/nation/

docker exec -it $1 hadoop fs -put /home/admin/region.tbl /user/hive/warehouse/tpch/region/

docker exec -it $1 hadoop fs -put /home/admin/part.tbl /user/hive/warehouse/tpch/part/

docker exec -it $1 hadoop fs -put /home/admin/supplier.tbl /user/hive/warehouse/tpch/supplier/

docker exec -it $1 hadoop fs -put /home/admin/customer.tbl /user/hive/warehouse/tpch/customer/

docker exec -it $1 hadoop fs -put /home/admin/orders.tbl /user/hive/warehouse/tpch/orders/


#run hive create
docker exec -it $1 hive -e "create table lineitem (
    l_orderkey    BIGINT ,
    l_partkey     BIGINT ,
    l_suppkey     BIGINT ,
    l_linenumber  BIGINT ,
    l_quantity    DOUBLE ,
    l_extendedprice  DOUBLE ,
    l_discount    DOUBLE ,
    l_tax         DOUBLE ,
    l_returnflag  CHAR(1) ,
    l_linestatus  CHAR(1) ,
    l_shipdate    DATE ,
    l_commitdate  DATE ,
    l_receiptdate DATE,
    l_shipinstruct CHAR(25) ,
    l_shipmode     CHAR(10) ,
    l_comment      VARCHAR(44) 
)
row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/lineitem/'
tblproperties ("skip.header.line.count"="1");"

