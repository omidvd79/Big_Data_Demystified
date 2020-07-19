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


#run hive create lineitme
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
location '/user/hive/warehouse/tpch/lineitem/';"

#hiver create nation
docker exec -it $1 hive -e "CREATE TABLE nation
(
   n_nationkey  INT  ,
   n_name       CHAR(25) ,
   n_regionkey  INT   ,
   n_comment    VARCHAR(152)
)
row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/nation/';"

#hive create region
docker exec -it $1 hive -e "CREATE TABLE region
(
   r_regionkey  INT  ,
   r_name       CHAR(25)  ,
   r_comment    VARCHAR(152)
)row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/region/'"

#hive create part
docker exec -it $1 hive -e "CREATE TABLE part
(
   p_partkey     BIGINT  ,
   p_name        VARCHAR(55)  ,
   p_mfgr        CHAR(25)  ,
   p_brand       CHAR(10)  ,
   p_type        VARCHAR(25)  ,
   p_size        INT ,
   p_container   CHAR(10)  ,
   p_retailprice DOUBLE  ,
   p_comment     VARCHAR(23)  
)row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/part/';"

#hive create supplier
docker exec -it $1 hive -e "CREATE TABLE supplier
(
   s_suppkey     BIGINT  ,
   s_name        CHAR(25)  ,
   s_address     VARCHAR(40) ,
   s_nationkey   INT   ,
   s_phone       CHAR(15)  ,
   s_acctbal     DOUBLE  ,
   s_comment     VARCHAR(101) 
)row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/supplier/';"

#hive create customer
docker exec -it $1 hive -e " CREATE TABLE customer
(
   c_custkey     BIGINT  ,
   c_name        VARCHAR(25)  ,
   c_address     VARCHAR(40)  ,
   c_nationkey   INT ,
   c_phone       CHAR(15)  ,
   c_acctbal     DOUBLE  ,
   c_mktsegment  CHAR(10)  ,
   c_comment     VARCHAR(117) 
)row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/customer/'"

#hive create orders
docker exec -it $1 hive -e "CREATE TABLE orders
(
   o_orderkey       BIGINT  ,
   o_custkey        BIGINT  ,
   o_orderstatus    CHAR(1)  ,
   o_totalprice     DOUBLE  ,
   o_orderdate      DATE  ,
   o_orderpriority  CHAR(15)  , 
   o_clerk          CHAR(15)  ,
   o_shippriority   INT ,
   o_comment        VARCHAR(79)  
)row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
location '/user/hive/warehouse/tpch/orders/'"

