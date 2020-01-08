CREATE OR REPLACE VIEW
  `MyProject.DATA_LAKE.similar_web_desktop_transformed` AS
SELECT
  avg_visits,
  date,
  device,
  r.country AS country,
  r.domain AS domain,
  r.granularity AS granularity
FROM (
  SELECT
    CAST(visits[
    OFFSET
      (0)].visits AS int64) AS avg_visits,
    # array of struct
    visits[
  OFFSET
    (0)].date AS date,
    # array of struct
    meta.device AS device,
    #   struct
    meta.request AS r,
    #struct of struct
    #meta.status as status
  FROM
    `MyProject.DATA_LAKE.similar_web_desktop` )

  
 
