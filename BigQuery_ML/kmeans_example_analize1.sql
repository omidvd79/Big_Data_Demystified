SELECT
  CENTROID_ID,
  #min(pvs) as min_pvs,
  CAST (AVG(pvs)AS int64) AS avg_pvs,
  #max(pvs) as max_pvs,
  #min(sessions) as min_sessions,
  CAST(AVG(sessions) AS int64) AS avg_sessions,
  #max(sessions) as max_sessions
  CAST(AVG(visits) AS int64) AS avg_visits
FROM
  BQ_ML.test3
GROUP BY
  CENTROID_ID
