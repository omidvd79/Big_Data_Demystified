WITH
  T AS (
  SELECT
    centroid_id,
    ARRAY_AGG(STRUCT(feature AS name,
        ROUND(numerical_value,1) AS value)
    ORDER BY
      centroid_id) AS cluster
  FROM
    ML.CENTROIDS(MODEL BQ_ML.users_clusters)
  GROUP BY
    centroid_id )
SELECT
  CONCAT('Cluster#', CAST(centroid_id AS STRING)) AS centroid,
  (
  SELECT
    value
  FROM
    UNNEST(cluster)
  WHERE
    name = 'pvs') AS pvs,
  (
  SELECT
    value
  FROM
    UNNEST(cluster)
  WHERE
    name = 'sessions') AS sessions,
  (
  SELECT
    value
  FROM
    UNNEST(cluster)
  WHERE
    name = 'visits') AS visits
FROM
  T
ORDER BY
  centroid
