SELECT
  dataset_id,
  count(*) AS tables,
  SUM(row_count) AS total_rows,
  SUM(size_bytes) AS size_bytes
FROM ( 
  SELECT * FROM `dataset1.__TABLES__` UNION ALL
  SELECT * FROM `dataset2.__TABLES__` UNION ALL
)
GROUP BY 1
ORDER BY size_bytes DESC
