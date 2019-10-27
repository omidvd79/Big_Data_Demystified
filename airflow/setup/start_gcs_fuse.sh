echo mounting FUSE of GCS bucket airflow-fuse-* -- logs and dags
gcsfuse airflow-fuse-logs gs_logs
gcsfuse airflow-fuse-dags gs_dags
