SELECT

(SELECT distinct value FROM h.customDimensions where index=4) as cd_4

FROM
  `MyProject.MyDataSEt.ga_sessions_*` t, t.hits h
