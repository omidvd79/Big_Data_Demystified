ALTER TABLE iceberg_table ADD COLUMNS (points_int int);
ALTER TABLE iceberg_table CHANGE points_int points_int bigint;

