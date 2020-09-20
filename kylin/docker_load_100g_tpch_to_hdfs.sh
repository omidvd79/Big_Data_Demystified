#user must provide docker name 
echo "docker name is :"+$1

#################################
#copy files from host to docker
sudo docker cp  ~/Big_Data_Demystified/kylin/tpch-dbgen/lineitem100g.tbl  $1:/home/admin/lineitem100g.tbl

############################
#create folder in HDFS in docker
docker exec -it $1 hadoop fs -mkdir /user/hive/warehouse/tpch/lineitem_100g/

#######################################
# copy files to HDFS in docker
docker exec -it $1 hadoop fs -put /home/admin/lineitem100g.tbl /user/hive/warehouse/tpch/lineitem_100g/

###############################
# hive inside docker - create table
###############################
#run hive create lineitem
docker exec -it $1 hive -e "create table lineitem_100g (
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
location '/user/hive/warehouse/tpch/lineitem_100g/';"

