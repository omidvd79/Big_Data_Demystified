SELECT
  CENTROID_ID,
  pvs,
  sessions,
  visits
FROM
  ML.PREDICT( MODEL BQ_ML.users_clusters,
    (
    SELECT
      SUM(PVs)AS pvs,
      SUM(sessions) AS sessions,
      COUNT(*) AS visits
    FROM
      `MyProject.DATA.Daily_Stats`
    WHERE
      date < '2019-11-01'
      AND date > '2019-10-01'
    GROUP BY
      users
    LIMIT
      100000000 ) )
