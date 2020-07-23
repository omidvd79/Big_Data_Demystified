#install hadoop

#if using s3
#hadoop fs -mkdir s3://jutomate-kylin-hbase/kylin

#if using HDFS
hadoop fs -mkdir /kylin 

#Remove joda.jar
mv $HIVE_HOME/lib/jackson-datatype-joda-2.4.6.jar $HIVE_HOME/lib/jackson-datatype-joda-2.4.6.jar.backup

# some more setting
rm -rf $KYLIN_HOME/spark_jars
mkdir -p $KYLIN_HOME/spark_jars
cp /usr/lib/spark/jars/*.jar $KYLIN_HOME/spark_jars
cp -f /usr/lib/hbase/lib/*.jar $KYLIN_HOME/spark_jars

rm -f netty-3.9.9.Final.jar 
rm -f netty-all-4.1.8.Final.jar

jar cv0f spark-libs.jar -C $KYLIN_HOME/spark_jars .
aws s3 cp spark-libs.jar s3://jutomate-kylin-hbase/kylin/package/  # You choose s3 as your working-dir
#hadoop fs -put spark-libs.jar hdfs://kylin/package/  # You choose hdfs as your working-dir
