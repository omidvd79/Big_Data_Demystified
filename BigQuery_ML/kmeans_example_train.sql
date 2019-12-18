CREATE OR REPLACE MODEL
  BQ_ML.users_clusters OPTIONS (model_type='kmeans',
    num_clusters=4,
    standardize_features = TRUE) AS (
  SELECT
    SUM(PVs)AS pvs,
    SUM(sessions) AS sessions,
    COUNT(*) AS visits
  FROM
    `MyProject.DATA.Daily_Stats`
  WHERE
    date < '2019-12-01'
    AND date > '2019-11-01'
  GROUP BY
    users )
