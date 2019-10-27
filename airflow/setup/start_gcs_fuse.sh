echo mounting FUSE of GCS bucket airflow-fuse-investing -- logs and dags
gcsfuse airflow-fuse-logs gs_logs
gcsfuse airflow-fuse-dags gs_dags
