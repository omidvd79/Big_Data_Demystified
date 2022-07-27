import sys
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

now = datetime.now()
current_time =  (now.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    query = "CALL demo.system.expire_snapshots('transformation.impressions_iceberg',TIMESTAMP '"+current_time +"',1)"
    print(len(sys.argv))
    spark = SparkSession\
        .builder\
        .appName("SparkETL")\
        .getOrCreate()
    spark.sql(query).show()
       print("done")
