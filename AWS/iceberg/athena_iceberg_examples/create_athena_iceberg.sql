CREATE TABLE iceberg_table (id bigint, data string, category string)
  PARTITIONED BY (category, bucket(16, id))
  LOCATION 's3://shneior/iceberg_table/'
  TBLPROPERTIES ( 'table_type' = 'ICEBERG' )
