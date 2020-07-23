#rm -rf $KYLIN_HOME/spark_jars
mkdir -p $KYLIN_HOME/spark_jars
cp /usr/lib/spark/jars/*.jar $KYLIN_HOME/spark_jars
cp -f /usr/lib/hbase/lib/*.jar $KYLIN_HOME/spark_jars

rm -f netty-3.9.9.Final.jar 
rm -f netty-all-4.1.8.Final.jar

jar cv0f spark-libs.jar -C $KYLIN_HOME/spark_jars .
##aws s3 cp spark-libs.jar s3://{YOUR_BUCKET}/kylin/package/  # You choose s3 as your working-dir

# if you use HDFS
sudo -u hadoop hadoop fs -mkdir /kylin/package 
sudo -u hadoop hadoop fs -put spark-libs.jar /kylin/package/

